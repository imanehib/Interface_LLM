#  Projet AWE – Plateforme de Correction de Texte avec Suivi de Rédaction

##  Objectif

Ce projet a été développé dans le cadre d’un projet universitaire de Master 1 Informatique. Il a pour but de proposer une plateforme web pédagogique permettant :

* aux **étudiants** de rédiger des textes, recevoir des corrections linguistiques automatiques et suivre leur progression ;
* aux **enseignants** de créer des exercices d’expression écrite, visualiser les textes rendus et observer les dynamiques d’écriture (suivi des frappes clavier).

Le projet explore le domaine de l’**AWE (Automatic Writing Evaluation)** à travers une approche pratique, alliant NLP, interface web et collecte de données comportementales.

---

##  Architecture du projet

L’architecture repose sur **Django** (backend + gestion des utilisateurs) et un frontend en **HTML/CSS** intégré dans les templates Django. Voici les principaux composants :

```
backend/
├── accounts/                # Gestion des utilisateurs (professeurs et étudiants)
│   └── views.py, forms.py, models.py, urls.py
├── text_analysis/          # Logique métier : exercices, analyse de texte, suivi des frappes
│   └── views.py, forms.py, models.py
├── templates/              # Interfaces utilisateur : login, dashboards, correcteur, etc.
│   ├── registration/
│   └── base.html, home.html, add_exercise.html
├── static/                 # Fichiers CSS, JS (optionnel)
└── manage.py, settings.py, urls.py
```

---

##  Fonctionnalités principales

* **Authentification personnalisée** : distinction entre professeurs et étudiants.
* **Dashboard professeur** : création/suppression d’exercices avec énoncés.
* **Interface étudiante** : sélection d’un exercice, saisie du texte, retour corrigé.
* **Correction automatique** :

  * *spaCy* pour la segmentation et l’analyse linguistique.
  * *LanguageTool* pour la détection des fautes grammaticales et de conjugaison.
  * *PySpellChecker* pour les fautes d’orthographe.
* **Suivi de frappe (keylogging éducatif)** : enregistrement des actions clavier avec position, texte, session, horodatage.
* **Sauvegarde & consultation** : les textes corrigés sont enregistrables et consultables.
* **Administration Django** : accessible aux superutilisateurs pour supervision.

---

## Installation

### Pré-requis

* Python ≥ 3.7
* Pip installé
* Environnement virtuel recommandé

### Dépendances (automatiquement via `requirements.txt`)

* `Django`
* `spacy`
* `pyspellchecker`
* `language_tool_python`
* `transformers` (si analyse avancée)

Installez-les avec :

```bash
pip install -r requirements.txt
```

Puis, téléchargez le modèle linguistique français pour spaCy :

```bash
python3 -m spacy download fr_core_news_sm
```

---

## Lancement du projet

Dans le dossier du projet, lancez le serveur de développement :

```bash
python3 manage.py runserver
```

L'application est accessible à l’adresse :

```
http://127.0.0.1:8000/
```

---

##  Accès selon les rôles

* **Étudiant** : après inscription, accède à l’interface de rédaction.
* **Professeur** : dispose d’un tableau de bord pour ajouter/voir/supprimer ses propres exercices.

Les rôles sont automatiquement assignés à l’inscription via les formulaires personnalisés.

---

## Technologies utilisées

* **Django 5.0+** : framework web robuste
* **spaCy** : NLP open-source
* **LanguageTool API** : vérification grammaticale
* **PySpellChecker** : correction orthographique
* **AJAX / JavaScript** : pour la capture en temps réel des frappes clavier

---

## Structure du code

| Composant        | Rôle                                                                  |
| ---------------- | --------------------------------------------------------------------- |
| `accounts/`      | Authentification, inscription, gestion des rôles                      |
| `text_analysis/` | Correction linguistique, gestion des textes et exercices              |
| `templates/`     | Interface HTML selon rôle (étudiant ou professeur)                    |
| `models.py`      | Définition des entités : `SavedText`, `Exercise`, `TypingEvent`, etc. |

---

## Exemple d’utilisation

1. Le professeur se connecte, accède à son tableau de bord, ajoute un exercice.
2. L’étudiant se connecte, choisit un exercice, rédige, puis corrige son texte.
3. La correction s’affiche, avec score, suggestions, messages pédagogiques.
4. Le texte corrigé peut être sauvegardé.
5. Les actions clavier sont stockées pour analyse (date, curseur, progression...).

---

##  Sécurité

* Accès restreint à l’administration Django.
* Middleware CSRF activé (à réactiver en prod).
* Rôles et permissions à renforcer dans les futures versions.

---

## À venir / Pistes d'amélioration

* Visualisation graphique du suivi d’écriture
* Tableau d’analyse pour les enseignants
* Éditeur XML visuel pour les énoncés
* Export des données pour analyse statistique

---

## Développeurs

Projet réalisé par un groupe d'étudiants de M1 Informatique dans le cadre du projet tutoré Android.


