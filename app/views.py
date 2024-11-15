from datetime import datetime
from django.contrib.auth import logout
from django.http import JsonResponse
from .forms import FormRegister, Log , NouvelleDemandeForm,ModifyDemandeForm
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Demande, Cours, User
from django.db.models.query import QuerySet

def logIn(request):
    """
    View for managing user login.

    Allows users to log into their accounts.
    If a user is a superuser, they are redirected to the admin panel.
    Otherwise, they are redirected to the home page.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponse: HTTP response for the login page.
    """
    assert request.method == 'GET' or request.method == 'POST'
    form = Log()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        assert isinstance(username, str)
        assert isinstance(password, str)
        user = authenticate(request, username=username, password=password)
        assert user is None or isinstance(user, User)
        if user is not None:
            login(request, user)
            assert user.is_superuser or not user.is_superuser
            if user.is_superuser:
                return redirect('admin:index')
            else:
                return redirect('Accueil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'app/LogIn.html', {'form': form})

def LogOut(request):
    """
    View for user logout.

    Logs out the currently logged-in user and redirects to the login page.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponseRedirect: Redirection to the login page.
    """
    logout(request)
    return redirect('logIn')

def register(request):
    """
    View for user registration.

    Allows new users to register by creating an account.
    Upon successful registration, the user is redirected to the login page.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponse: HTTP response for the registration page.
    """
    assert request.method == 'GET' or request.method == 'POST'
    form = FormRegister()
    if request.method == 'POST':
        form = FormRegister(request.POST)
        assert isinstance(form, FormRegister)
        if form.is_valid():
            form.save()
            return redirect('logIn')
    else:
        return render(request, 'app/Register.html', {'form': form})
    return render(request, 'app/Register.html', {'form': form})

def Accueil(request):
    """
    View for the user homepage.

    Displays the homepage with requests currently being processed for the logged-in user.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponse: HTTP response for the homepage.
    """
    assert request.user.is_authenticated or not request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('logIn')
    else:
        demandes_utilisateur = Demande.objects.filter(
            utilisateur=request.user,
            accord_cf__isnull=True,
            remarque__isnull=True,
            salaire__isnull=True
        ).values(
            'id',
            'motif',
            'accord_suppleant',
            'inputation_salaire',
            'cpo',
            'cours__code',
            'cours__intitule',
            'cours__option',
            'cours__programme',
            'supleant__suppleant_nom',
            'supleant__suppleant_prenom'
        )
        nom_utilisateur = request.user.username
        assert isinstance(demandes_utilisateur, QuerySet)
        assert isinstance(nom_utilisateur, str)
        context = {
            'demandes_utilisateur': demandes_utilisateur,
            'nom_utilisateur': nom_utilisateur,
        }
        return render(request, 'app/accueil.html', context)

def Add_Request(request):
    """
    View for adding a new request.

    Allows the user to submit a new request.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponse: HTTP response for the request addition page.
    """
    assert request.user.is_authenticated or not request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('logIn')
    else:
        if request.method == 'POST':
            form = NouvelleDemandeForm(request.POST)
            assert isinstance(form, NouvelleDemandeForm)
            if form.is_valid():
                nouvelle_demande = form.save(commit=False)
                cours = nouvelle_demande.cours
                cours_instance = get_object_or_404(Cours, pk=cours.pk)
                assert isinstance(cours_instance, Cours)
                if request.user in cours_instance.enseignants.all():
                    current_year = datetime.now().year
                    demandes_existantes = Demande.objects.filter(cours=cours, utilisateur=request.user, date_creation__year=current_year)
                    assert isinstance(demandes_existantes, QuerySet)
                    if not demandes_existantes.exists():
                        nouvelle_demande.utilisateur = request.user
                        nouvelle_demande.save()
                        return redirect('Accueil')
                    else:
                        messages.error(request, "Vous avez déjà soumis une demande pour ce cours cette année.")
                else:
                    messages.error(request, "Vous n'êtes pas autorisé à soumettre une demande pour ce cours.")
            else:
                # Affichage des erreurs du formulaire
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = NouvelleDemandeForm()
            assert isinstance(form, NouvelleDemandeForm)
    return render(request, 'app/Add_Request.html', {'form': form})

def Modify(request, pk):
    """
    View for modifying an existing request.

    Allows the user to modify an existing request identified by its primary key (pk).
    Only users responsible for the associated course can modify the request.

    Args:
        request (HttpRequest): HTTP request received by the view.
        pk (int): Primary key of the request to modify.

    Returns:
        HttpResponse: HTTP response for the request modification page.
    """
    assert request.user.is_authenticated or not request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('logIn')
    else:
        demande = get_object_or_404(Demande, pk=pk)
        assert isinstance(demande, Demande)
        form = ModifyDemandeForm(instance=demande)
        assert isinstance(form, ModifyDemandeForm)
      
        if request.method == 'POST':
            form = ModifyDemandeForm(request.POST, instance=demande)
            assert isinstance(form, ModifyDemandeForm)
            if form.is_valid():
                instance = form.save(commit=False)
                cours = instance.cours
                assert isinstance(cours, Cours)
                if request.user in cours.enseignants.all():
                    if instance.inputation_salaire != "Mission Scientifique":
                        instance.cpo = None
                    instance.save()
                    return redirect('Accueil')
                else:
                    messages.error(request, "Vous pouvez pas soumettre une demande pour un cours dont vous n'etes pas responsable")
                    
        return render(request, 'app/Modify.html', {'form': form, 'demande': demande})

def Delete(request, pk):
    """
    View for deleting an existing request.

    Allows the user to delete an existing request identified by its primary key (pk).

    Args:
        request (HttpRequest): HTTP request received by the view.
        pk (int): Primary key of the request to delete.

    Returns:
        HttpResponseRedirect: Redirection to the homepage after deleting the request.
    """
    assert request.user.is_authenticated or not request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('logIn')
    else:
        demande = get_object_or_404(Demande, pk=pk)
        assert isinstance(demande, Demande)
        demande.delete()    
        return redirect('Accueil')

def DemandeEnCoursDeTraitement(request):
    """
    View for displaying requests currently being processed.

    Displays requests currently being processed for the logged-in user.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponse: HTTP response for the page displaying requests currently being processed.
    """
    assert request.user.is_authenticated or not request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('logIn')
    else:
        demandes_utilisateur = Demande.objects.filter(
            utilisateur=request.user,
            accord_cf__isnull=True,
            remarque__isnull=False,
            salaire__isnull=False
        ).values(
            'id', 'motif', 'accord_suppleant', 'inputation_salaire', 'cpo', 
            'cours__code', 'cours__intitule', 'cours__option', 'cours__programme', 
            'supleant__suppleant_nom', 'supleant__suppleant_prenom','remarque', 'salaire',
        )

        nom_utilisateur = request.user.username
        assert isinstance(demandes_utilisateur, QuerySet)
        assert isinstance(nom_utilisateur, str)
    
        context = {
            'demandes_utilisateur': demandes_utilisateur,
            'nom_utilisateur': nom_utilisateur,
        }
        return render(request, 'app/demande_encours.html', context)

def demande_traiter(request):
    """
    View for displaying processed requests.

    Displays processed requests for the logged-in user.

    Args:
        request (HttpRequest): HTTP request received by the view.

    Returns:
        HttpResponse: HTTP response for the page displaying processed requests.
    """
    assert request.user.is_authenticated or not request.user.is_authenticated
    if not request.user.is_authenticated:
        return redirect('logIn')  
    else:
        demandes_utilisateur = Demande.objects.filter(
            utilisateur=request.user,
            accord_cf__isnull=False,
            remarque__isnull=False,
            salaire__isnull=False
        ).values(
            'id', 'motif', 'accord_suppleant', 'inputation_salaire', 'cpo', 
            'cours__code', 'cours__intitule', 'cours__option', 'cours__programme', 
            'supleant__suppleant_nom', 'supleant__suppleant_prenom','remarque', 'salaire','accord_cf',
        )

        nom_utilisateur = request.user.username
        assert isinstance(demandes_utilisateur, QuerySet)
        assert isinstance(nom_utilisateur, str)
    
        context = {
            'demandes_utilisateur': demandes_utilisateur,
            'nom_utilisateur': nom_utilisateur,
        }
        return render(request, 'app/demande_traiter.html', context)

def make_query_view(request, code):
    """
    View for generating a JSON response.

    Generates a JSON response containing information about the course corresponding to the given code.

    Args:
        request (HttpRequest): HTTP request received by the view.
        code (str): Course code.

    Returns:
        JsonResponse: JSON response containing information about the course.
    """
    assert code is not None
    cours = Cours.objects.get(code=code)
    option_cours = cours.option
    return JsonResponse({'option': option_cours})