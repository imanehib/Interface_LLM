from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import SavedText, Exercise 
from .forms import ExerciseForm
from django.contrib.auth.decorators import login_required
import spacy
from spellchecker import SpellChecker
import re
import language_tool_python

# Charger spaCy avec le modèle français
nlp = spacy.load("fr_core_news_sm")
# tool = language_tool_python.LanguageToolPublicAPI('fr')

tool = None

def get_language_tool():
    global tool
    if tool is None:
        try:
            tool = language_tool_python.LanguageToolPublicAPI('fr')
        except LanguageToolError:
            # En fallback, on peut utiliser le serveur local embarqué
            tool = language_tool_python.LanguageTool('fr')
    return tool

# Initialisation du correcteur orthographique
spell_checker = SpellChecker(language='fr')

def correct_text(text):
    """Corrige les fautes orthographiques, grammaticales et de conjugaison"""

    if not text.strip():
        return {"corrected_text": text, "score": 100, "suggestions": {}, "special_messages": []}

    # Séparer les phrases en tenant compte de la ponctuation
    sentences = re.split(r'([.!?])\s*', text)
    
    suggestions = {}
    special_messages = []
    corrected_sentences = []

    for i in range(0, len(sentences), 2):  # Parcours des phrases
        if i < len(sentences):
            sentence = sentences[i].strip()  
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""  

            # Vérification des majuscules AVANT tout
            words = re.findall(r"\w+|[.,!?;']", sentence)
            if words:
                first_word = words[0]
                if first_word[0].islower():
                    words[0] = first_word.capitalize()
                    special_messages.append(("La phrase doit commencer par une majuscule.", first_word))
                sentence = " ".join(words)  

            # Vérification avec LanguageTool pour grammaire et conjugaison
            matches = get_language_tool().check(sentence)

            
            for match in matches:
                error_word = match.context[match.offset:match.offset + match.errorLength]
                suggestion = match.replacements[0] if match.replacements else ""

                # Gestion des mots avec apostrophe, comme "m'appelle"
                if "'" in error_word:
                    parts = error_word.split("'")
                    if len(parts) == 2 and parts[0] in {"m", "t", "s", "l", "d", "n", "j"}:
                        # On ne vérifie que la partie après l'apostrophe
                        root_word = parts[1]
                        if root_word.lower() in spell_checker.unknown([root_word.lower()]):
                            corrected = spell_checker.correction(root_word.lower())
                            if corrected:
                                suggestions[root_word] = corrected
                                sentence = sentence.replace(root_word, corrected, 1)
                        continue  # On ne doit pas modifier "m'" par exemple, seulement la deuxième partie

                if suggestion and error_word.lower() != suggestion.lower():
                    suggestions[error_word] = suggestion
                    sentence = sentence.replace(error_word, suggestion, 1)

            # Vérification orthographique des autres mots
            words = re.findall(r"\w+|[.,!?;']", sentence)

            for j, word in enumerate(words):
                if word.isalpha() and "'" not in word:  
                    lower_word = word.lower()
                    if lower_word in spell_checker.unknown([lower_word]):  
                        corrected = spell_checker.correction(lower_word)
                        if corrected:
                            suggestions[word] = corrected
                            words[j] = corrected  

            # Reconstruction de la phrase corrigée
            corrected_sentence = " ".join(words) + punctuation
            corrected_sentences.append(corrected_sentence)

    # Reconstruction du texte corrigé
    corrected_text = " ".join(corrected_sentences)

    # Calcul du score
    total_words = sum(1 for w in corrected_text.split() if w.isalpha())
    incorrect_words = len(suggestions)
    score = max(0, 100 - (incorrect_words / total_words * 100)) if total_words else 100
    score = round(score, 2)

    return {
        "corrected_text": corrected_text,
        "score": score,
        "suggestions": suggestions,
        "special_messages": special_messages  
    }
    # 🔹 Corriger la majuscule au début de la phrase et après chaque ponctuation
    def capitalize_after_punctuation(text):
        # Mettre la première lettre en majuscule après une ponctuation, même sans espace
        text = re.sub(r'([.!?]\s*)(\w)', lambda x: x.group(1) + x.group(2).upper(), text)
        # Vérifier la première lettre du texte
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
            special_messages.append('La phrase devrait commencer par une majuscule.')
        return text

    # Corriger la capitalisation après chaque ponctuation
    corrected_text = capitalize_after_punctuation(corrected_text)

    # Calcul du score basé sur le nombre d'erreurs corrigées
    total_words = len(words)
    incorrect_words = len(suggestions)
    score = max(0, 100 - (incorrect_words / total_words * 100)) if total_words else 100
    score = round(score, 2)

    return {
        "corrected_text": corrected_text,
        "score": score,
        "suggestions": suggestions,
        "grammar_errors": grammar_errors,
        "special_messages": special_messages  # Ajout de messages spéciaux dans un champ séparé
    }

def home(request):
    # 1. Récupérer tous les exercices
    exercises = Exercise.objects.all()

    # 2. Récupérer, si présent, l'exercice sélectionné en GET
    exercise_id  = request.GET.get('exercise')
    exercise_content = ''
    if exercise_id:
        try:
            exercise_content = Exercise.objects.get(pk=exercise_id).content
        except Exercise.DoesNotExist:
            exercise_content = ''

    # 3. correction (POST)
    result = None
    saved_texts = SavedText.objects.all()  # Récupère tous les textes sauvegardés

    if request.method == "POST":
        text = request.POST.get('text', '').strip()
        list_position = request.POST.get('list_position', '')  # Récupère la position du curseur
        list_progression = request.POST.get('list_progression', '')  # Récupère la progression du texte

        # Correction du texte
        result = correct_text(text)

        # Sauvegarder dans la base de données
        if 'save' in request.POST:
            # Sauvegarder le texte, la position et la progression dans la base de données
            SavedText.objects.create(
                text=text, 
                score=result.get("score", 0), 
                list_position=list_position, 
                list_progression=list_progression
            )
            return redirect('text_analysis:home')  # Redirige après avoir sauvegardé

    return render(request, 'home.html', {'exercises':    exercises, 'selected_id':  exercise_id, 'exercise_content': exercise_content, 'result': result, 'saved_texts': saved_texts})

def save_text(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        score = 0
        SavedText.objects.create(text=text, score=score)
        return redirect('text_analysis:home')
    return JsonResponse({"error": "Méthode non autorisée"}, status=400)

def delete_text(request, text_id):
    text = get_object_or_404(SavedText, id=text_id)
    text.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Texte supprimé avec succès!'})
    return redirect('text_analysis:home')

from django.http import JsonResponse
from .models import UserTyping
import json

def update_typing_data(request):
    # Récupérer les données envoyées par la requête JavaScript
    text = request.POST.get('text', '')  # Le texte actuel
    cursor_position = int(request.POST.get('cursor_position', 0))  # Position du curseur
    
    # Si l'utilisateur a déjà des données de frappe dans la base
    user_typing_data, created = UserTyping.objects.get_or_create(user=request.user)

    # Mise à jour des listes dans le modèle
    user_typing_data.list_position.append(cursor_position)
    user_typing_data.list_progression.append(text)
    
    # Sauvegarde des changements dans la base de données
    user_typing_data.save()

    return JsonResponse({"message": "Données sauvegardées avec succès"}, status=200)

from django.http import JsonResponse
from .models import SavedText

def update_list(request):
    if request.method == "POST":
        list_position = request.POST.get("list_position")  # Récupérer les données envoyées
        list_progression = request.POST.get("list_progression")

        # Mettre à jour ou ajouter les données dans la base de données
        new_entry = SavedText(list_position=list_position, list_progression=list_progression)
        new_entry.save()

        # Retourner une réponse JSON
        return JsonResponse({
            'success': True,
            'list_position': list_position,
            'list_progression': list_progression
        })
    return JsonResponse({'success': False})

from django.shortcuts import render, redirect
from .models import SavedText
from django.shortcuts import render
from .models import UserTyping  # Ou d'autres modèles si nécessaire

from django.shortcuts import render

from django.shortcuts import render

# Supposons que tu aies une fonction d'analyse de texte
def analyze_text(text):
    # Ta logique d'analyse du texte ici
    # Retourne le texte corrigé ou les résultats de l'analyse
    return {
        'corrected_text': text,  # Juste un exemple, remplace cela par ta logique réelle
        'score': 85  # Exemple de score, à remplacer par ton propre calcul
    }

def analyze(request):
    if request.method == 'POST':
        # Récupérer les données envoyées par la requête
        text = request.POST.get('text', None)  # Si 'text' n'est pas trouvé, il renvoie None
        list_position = request.POST.get('list_position', '')  # Position du curseur
        list_progression = request.POST.get('list_progression', '')  # Progression du texte

        # Ajouter des logs pour vérifier les paramètres
        print(f"Texte reçu: {text}")
        print(f"Position du curseur: {list_position}")
        print(f"Progression du texte: {list_progression}")

        # Vérifier si 'text' est valide
        if not text or not isinstance(text, str):
            return JsonResponse({'error': 'Texte invalide ou vide'}, status=400)

        # Appeler la fonction correct_text pour analyser le texte
        result = correct_text(text)

        # Passer les résultats au template 'home.html' au lieu de renvoyer JSON
        return render(request, 'home.html', {
            'result': result,
            'list_position': list_position,
            'list_progression': list_progression
        })
    
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import UserTyping

def save_user_typing(request):
    if request.method == "POST":
        text = request.POST.get('text', '')
        cursor_position = request.POST.get('cursor_position', 0)

        # Sauvegarde les frappes dans la base de données
        user_typing = UserTyping.objects.create(
            text=text,
            cursor_position=cursor_position
        )
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TypingEvent
@csrf_exempt  # Désactiver temporairement CSRF pour le test
def save_typing_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            session_id = data.get("session_id")
            cursor_position = data.get("cursor_position")
            text_progression = data.get("text_progression")

            # Sauvegarder l'événement de frappe
            typing_event = UserTyping(
                session_id=session_id,
                cursor_position=cursor_position,
                text_progression=text_progression
            )
            typing_event.save()

            return JsonResponse({"message": "Frappes enregistrées !"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Méthode non autorisée"}, status=405)


@login_required
def teacher_dashboard(request):
    exercises = Exercise.objects.filter(author=request.user)
    return render(request, 'text_analysis/teacher_dashboard.html', {
        'exercises': exercises
    })

@login_required
def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            ex = form.save(commit=False)
            ex.author = request.user
            ex.save()
            return redirect('text_analysis:teacher_dashboard')
    else:
        form = ExerciseForm()
    return render(request, 'add_exercise.html', {'form': form})