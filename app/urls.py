from django.urls import path
from app import  views
from django.contrib import admin
urlpatterns = [
    path('LogIn/', views.logIn, name='logIn'),
    path('Register/' ,views.register, name='register'),
    path('LogOut/' ,views.LogOut, name='LogOut'),
    path('Accueil/' ,views.Accueil, name='Accueil'),
    path('Add_Request/', views.Add_Request, name='Add_Request'),
    path('Modify/<int:pk>/', views.Modify, name='Modify'),
    path('Delete/<int:pk>/', views.Delete, name='Delete'),
    path('demande_encours/' ,views.DemandeEnCoursDeTraitement, name='demande_encours'),
    path('demande_traiter/' ,views.demande_traiter, name='demande_traiter'),
    path('admin/', admin.site.urls),
    path('make_query/<str:code>', views.make_query_view, name='make_query'),
    

    ]
