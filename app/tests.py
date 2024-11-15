from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Cours, Suppleant, User, Demande
from .views import  register, Accueil

class LogInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login(self):
        response = self.client.get(reverse('logIn'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('logIn'), {'username': 'testuser', 'password': 'password'})
        self.assertRedirects(response, reverse('Accueil'))

        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('logIn'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_get_request(self):
        response = self.client.get(reverse('logIn'))
        self.assertTemplateUsed(response, 'app/LogIn.html')

class LogOutViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_logout_view(self):
        # Connexion de l'utilisateur avant de tester la déconnexion
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('LogOut'))
        self.assertEqual(response.status_code, 302)

        # Assurez-vous que l'utilisateur est anonyme après la déconnexion
        self.assertTrue(response.wsgi_request.user.is_anonymous)

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


    def test_register_view(self):
        request = self.factory.get(reverse('register'))
        response = register(request)
        self.assertEqual(response.status_code, 200)

class AccueilViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_accueil_view_authenticated(self):
        request = self.factory.get(reverse('Accueil'))
        request.user = self.user
        response = Accueil(request)
        self.assertEqual(response.status_code, 200)

class DeleteViewTestCase(TestCase):
    def setUp(self):
        # Création d'un utilisateur
        self.user = User.objects.create_user(username='testuser', password='password')

        # Création d'un cours
        self.cours = Cours.objects.create(code="ABC123", intitule="Nom du cours", option="Oui", programme="Programme")

        # Création d'un suppleant
        self.suppleant = Suppleant.objects.create(suppleant_nom="Nom du suppleant", suppleant_prenom="Prénom du suppleant")

        # Création d'une demande
        self.demande = Demande.objects.create(
            motif="Motif de la demande",
            accord_suppleant="Oui",
            inputation_salaire="Mission Scientifique",
            utilisateur=self.user,
            cours=self.cours,
            supleant=self.suppleant
        )

    def test_delete_view(self):
        # Nombre initial de demandes
        initial_demande_count = Demande.objects.count()

        # Suppression de la demande directement
        self.demande.delete()

        # Vérification que la demande a bien été supprimée de la base de données
        self.assertEqual(Demande.objects.count(), initial_demande_count - 1)
        self.assertFalse(Demande.objects.filter(pk=self.demande.pk).exists())

