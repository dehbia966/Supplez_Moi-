from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

class Cours(models.Model):
    code = models.CharField(max_length=100, primary_key=True,unique=True)
    intitule = models.CharField(max_length=100)
    option = models.CharField(max_length=7, choices=(("Oui", "Oui"), ("Non", "Non")))
    programme = models.CharField(max_length=100)
    enseignants = models.ManyToManyField(User, related_name='cours_enseignes', blank=True)

class Suppleant(models.Model):
    suppleant_nom = models.CharField(max_length=100,primary_key=True,unique=True)
    suppleant_prenom = models.CharField(max_length=100)

class Demande(models.Model):
    id = models.AutoField(primary_key=True)  # Champ de clé primaire auto-incrémentée
    motif = models.TextField()
    accord_suppleant = models.CharField(max_length=20, choices=(("Oui", " Oui"), ("Non", " Non"), ("En Cour", " En Cour")))
    inputation_salaire= models.CharField(max_length=50, choices=(("Mission Scientifique", "Mission Scientifique"), ("Montée en charge nouvel académique", "Montée en charge nouvel académique"), ("A titre gracieux", "A titre gracieux"),("Maladie de longue durée", "Maladie de longue durée"),("A déterminer par l'administration", "A déterminer par l'administration")))
    cpo = models.IntegerField( null=True, blank=True)
    remarque = models.TextField(null=True,blank=True)
    salaire = models.FloatField(null=True,blank=True)
    accord_cf = models.CharField(null=True,max_length=10, choices=(("Oui", "Oui"), ("Non", "Non")),blank=True) 
    date_creation = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_utilisateur')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='demandes_cours')
    supleant=models.ForeignKey(Suppleant, on_delete=models.CASCADE, related_name='demandes_suppleant')


