
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class SavedText(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Ajoute ceci si ce champ n'est pas défini

    def __str__(self):
        return self.text[:50]  # Afficher un extrait du texte



class UserTyping(models.Model):
    session_id = models.CharField(max_length=255)
    cursor_position = models.IntegerField()
    text_progression = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Ce champ enregistre la date de création de l'objet

    def __str__(self):
        return self.session_id  # Tu peux afficher ce qui te convient ici



class TypingEvent(models.Model):
    session_id = models.CharField(max_length=255)  # ID de session unique
    cursor_position = models.IntegerField()  # Position du curseur
    text_progression = models.TextField()  # Évolution du texte
    timestamp = models.DateTimeField(auto_now_add=True)  # Date d'enregistrement

    def __str__(self):
        return f"Session {self.session_id} - Pos {self.cursor_position}"


User = get_user_model()

class Exercise(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    title       = models.CharField(max_length=200)
    content     = models.TextField(default="", help_text="Entrez votre énoncé de l’exercice")
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} par {self.author.username}"
