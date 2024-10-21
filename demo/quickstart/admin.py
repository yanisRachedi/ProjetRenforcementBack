from django.contrib import admin
from .models import Auteur, Livre, Categorie, Exemplaire, Emprunt, Commentaire, Evaluation, Editeur

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ('nom', 'date_de_naissance')
    list_filter = ('date_de_naissance',)

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    search_fields = ['titre', 'auteurs']
    list_display = ('titre', 'éditeur', 'date_de_publication')
    list_filter = ('catégories', 'éditeur')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ('nom',) 

