from django.db import models

# Create your models here.
class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    biographie = models.TextField()
    date_de_naissance = models.DateField()
    date_de_décès = models.DateField(null=True)
    nationalité = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='auteurs/', null=True)

class Livre(models.Model):
    titre = models.CharField(max_length=255)
    résumé = models.TextField()
    date_de_publication = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    nombre_de_pages = models.PositiveIntegerField()
    langue = models.CharField(max_length=100)
    image_de_couverture = models.ImageField(upload_to='couvertures/', null=True)
    éditeur = models.CharField(max_length=255)
    format = models.CharField(max_length=50)
    auteurs = models.ManyToManyField(Auteur, related_name='livres')
    catégories = models.ManyToManyField('Categorie', related_name='livres')

    def __str__(self):
        return self.titre
    
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom

class Exemplaire(models.Model):
    état = models.CharField(max_length=50, choices=[('Neuf', 'Neuf'), ('Bon état', 'Bon état'), ('Mauvais état', 'Mauvais état')])
    date_acquisition = models.DateField()
    localisation = models.CharField(max_length=255)
    disponibilité = models.BooleanField(default=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='exemplaires')

    def __str__(self):
        return f"Exemplaire de {self.livre.titre} - {self.état}"

class Emprunt(models.Model):
    exemplaire = models.ForeignKey(Exemplaire, on_delete=models.CASCADE, related_name='emprunts')
    utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prévue = models.DateTimeField()
    date_retour_effective = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[('En cours', 'En cours'), ('Terminé', 'Terminé'), ('En retard', 'En retard')])
    remarques = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Emprunt de {self.exemplaire.livre.titre} par {self.utilisateur.username}"

class Commentaire(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    note = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    visible = models.BooleanField(default=True)
    modéré = models.BooleanField(default=False)

    def __str__(self):
        return f"Commentaire de {self.utilisateur.username} sur {self.livre.titre}"


class Editeur(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    site_web = models.URLField(null=True, blank=True)
    email_contact = models.EmailField()
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="logo_editeurs/", null=True)

    def __str__(self):
        return self.nom

class Evaluation(models.Model):
    note = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    commentaire = models.TextField()
    date_evaluation = models.DateTimeField(auto_now_add=True)
    recommande = models.BooleanField()
    titre = models.CharField(max_length=100)