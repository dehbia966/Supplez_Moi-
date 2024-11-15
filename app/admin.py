import csv
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import User, Cours, Suppleant,Demande

#déconnexion  souci 
admin.site.logout_url = '/LogIn/'

# Définir une classe d'administration personnalisée pour le modèle utilisateur personnalisé
class CustomUserAdmin(UserAdmin):
    # Spécifier les champs que vous souhaitez afficher et éditer dans l'interface d'administration
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'bio', 'location', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Spécifier la liste des champs qui seront affichés dans la liste des utilisateurs dans l'interface d'administration
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Spécifier les champs de recherche pour faciliter la recherche d'utilisateurs dans l'interface d'administration
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Enregistrer le modèle utilisateur personnalisé avec l'administration personnalisée
admin.site.register(User, CustomUserAdmin)

#admin.site.register(Cours)

class CoursPersonnalise(admin.ModelAdmin):
    list_display=('code','intitule','option','programme','get_enseignants')
    def get_enseignants(self, obj):
        return ", ".join([enseignant.username for enseignant in obj.enseignants.all()])    
admin.site.register(Cours, CoursPersonnalise)

@admin.register(Suppleant)
class SuppleantPersonnalise(admin.ModelAdmin):
    list_display=('suppleant_nom','suppleant_prenom')


class DemandePersonnalise(admin.ModelAdmin):
    list_display=('id','motif','accord_suppleant','inputation_salaire','cpo','remarque','accord_cf','utilisateur','cours','supleant','salaire' )
    list_filter=['inputation_salaire']
    search_fields=('utilisateur',)
    actions = ['export_to_csv'] 


    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('id', 'utilisateur', 'cours', 'supleant')
     # Ajoutez l'action d'exportation CSV

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="demandes.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Motif', 'Accord Suppleant', 'Inputation Salaire', 'CPO', 'Remarque', 'Accord CF', 'Utilisateur', 'Cours', 'Suppleant', 'Salaire'])

        for demande in queryset:
            writer.writerow([demande.id, demande.motif, demande.accord_suppleant, demande.inputation_salaire, demande.cpo, demande.remarque, demande.accord_cf, demande.utilisateur, demande.cours, demande.supleant, demande.salaire])

        return response

    # Définition des métadonnées pour l'action d'exportation CSV
    export_to_csv.short_description = "Exporter vers CSV"

admin.site.register(Demande, DemandePersonnalise)

# Supprimer le lien "Voir le site" du menu
admin.site.site_url=None