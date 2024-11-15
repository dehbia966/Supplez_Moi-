from django import forms
from .models import User, Demande
from .models import Cours, Suppleant


class Log(forms.Form):
    """
    Formulaire de connexion.

    Fields:
        username (CharField): Champ pour le nom d'utilisateur.
        password (CharField): Champ pour le mot de passe (obscure).
    """
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())

class FormRegister(forms.ModelForm):
    """
    Formulaire d'inscription.

    Fields:
        username (CharField): Champ pour le nom d'utilisateur.
        first_name (CharField): Champ pour le prénom de l'utilisateur (optionnel).
        last_name (CharField): Champ pour le nom de l'utilisateur (optionnel).
        password1 (CharField): Champ pour le mot de passe.
        password2 (CharField): Champ pour confirmer le mot de passe.
        email (EmailField): Champ pour l'adresse e-mail de l'utilisateur.

    Methods:
        clean: Vérifie si les mots de passe correspondent.
        save: Enregistre l'utilisateur avec le mot de passe chiffré.
    """

    username = forms.CharField(label='Username', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=30, required=False)
    last_name = forms.CharField(label='Last Name', max_length=30, required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput()) 
    password2 = forms.CharField(label='Re-enter the password', widget=forms.PasswordInput()) 
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Vérifier si les deux mots de passe sont identiques
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class DemandeForm(forms.ModelForm):
    """
    Formulaire pour une demande.

    Meta:
        model (Demande): Modèle associé au formulaire.
        fields (list): Champs du modèle à inclure dans le formulaire.
    """

    class Meta:
        model = Demande
        fields = ['motif', 'accord_suppleant', 'inputation_salaire', 'cpo', 'remarque', 'salaire', 'accord_cf', 'utilisateur', 'cours', 'supleant']

class SelectWithAttributeField(forms.Select):    
    """
    Widget de sélection avec attribut personnalisé.

    Méthodes:
        create_option: Crée une option avec un attribut de données personnalisé.
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None ):     
        option = super().create_option( name, value, label, selected, index, subindex, attrs   )       
        if value:           
            option["attrs"]["data-option"] = value.get().option       
        return option  
                   
class NouvelleDemandeForm(forms.ModelForm):
    """
    Formulaire pour une nouvelle demande.

    Meta:
        model (Demande): Modèle associé au formulaire.
        fields (list): Champs du modèle à inclure dans le formulaire.
        widgets: Utilise le widget SelectWithAttributeField pour le champ 'cours'.

    Méthodes:
        clean: Vérifie la validité des données.
    """
    MOTIF_CHOICES = [
        ("Mission Scientifique", "Mission Scientifique"),
        ("Montée en charge nouvel académique", "Montée en charge nouvel académique"),
        ("A titre gracieux", "A titre gracieux"),
        ("Maladie de longue durée", "Maladie de longue durée"),
        ("A déterminer par l'administration", "A déterminer par l'administration"),
    ]
    

    ACCORD_CHOICES = [
        ("Oui", "Oui"),
        ("En Cour", "En Cour"),
        ("Non", "Non"),
    ]

    cours = forms.ModelChoiceField(queryset=Cours.objects.all(), empty_label=None)
    supleant = forms.ModelChoiceField(queryset=Suppleant.objects.all(), empty_label=None)
    inputation_salaire = forms.ChoiceField(choices=MOTIF_CHOICES)
    motif=forms.Textarea()
    cpo=forms.IntegerField(required=False)
    accord_suppleant = forms.ChoiceField(choices=ACCORD_CHOICES)

    class Meta:
        model = Demande  
        fields = ['motif','cours', 'supleant', 'inputation_salaire','cpo', 'accord_suppleant']
        widgets={
            "cours": SelectWithAttributeField
        }

    def clean(self):
        cleaned_data = super().clean()
        inputation_salaire = cleaned_data.get('inputation_salaire')
        cpo = cleaned_data.get('cpo')
        cours = cleaned_data.get('cours')

        if inputation_salaire == "Mission Scientifique" and not cpo:
            raise forms.ValidationError("Le champ CPO est obligatoire pour la mission scientifique.")

        if inputation_salaire != "Mission Scientifique" and cpo:
            raise forms.ValidationError("Le champ CPO ne doit pas être rempli pour les motifs autres que la mission scientifique.")
     # Assuming multiple options (use Select for single)

class ModifyDemandeForm(forms.ModelForm):
    """
    Formulaire de modification de demande.
    
    Ce formulaire est utilisé pour modifier une demande existante dans le système.

    Attributes:
        cours (ModelChoiceField): Champ pour sélectionner le cours.
        supleant (ModelChoiceField): Champ pour sélectionner le suppléant.
        inputation_salaire (ChoiceField): Champ pour sélectionner le motif de l'inputation salaire.
        motif (Textarea): Champ pour entrer le motif de la demande.
        cpo (IntegerField, facultatif): Champ pour entrer le CPO.
        accord_suppleant (ChoiceField): Champ pour indiquer l'accord avec le suppléant.
    """
    MOTIF_CHOICES = [
        ("Mission Scientifique", "Mission Scientifique"),
        ("Montée en charge nouvel académique", "Montée en charge nouvel académique"),
        ("A titre gracieux", "A titre gracieux"),
        ("Maladie de longue durée", "Maladie de longue durée"),
        ("A déterminer par l'administration", "A déterminer par l'administration"),
    ]

    ACCORD_CHOICES = [
        ("Oui", "Oui"),
        ("En Cour", "En Cour"),
        ("Non", "Non"),
    ]

    cours = forms.ModelChoiceField(queryset=Cours.objects.all(), empty_label=None)
    supleant = forms.ModelChoiceField(queryset=Suppleant.objects.all(), empty_label=None)
    inputation_salaire = forms.ChoiceField(choices=MOTIF_CHOICES)
    motif=forms.Textarea()
    cpo=forms.IntegerField(required=False)
    accord_suppleant = forms.ChoiceField(choices=ACCORD_CHOICES)

    class Meta:
        model = Demande
        fields = ['cours', 'supleant','inputation_salaire', 'motif','cpo', 'accord_suppleant']