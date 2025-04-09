from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, ProfessorSignUpForm

# Récupère le modèle utilisateur personnalisé
CustomUser = get_user_model()

def index(request):
    return render(request, 'index.html')

# Vue de connexion (Login)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Vous pouvez transmettre un paramètre "role" si nécessaire
        context['role'] = self.request.GET.get('role', '')
        return context

# Vue de déconnexion (Logout)
class CustomLogoutView(LogoutView):
    next_page = '/'  # Redirige vers la page d'accueil après déconnexion

# Vue d'inscription pour étudiants
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.STUDENT  # ou simplement 'student'
            user.save()
            login(request, user)
            return redirect('text_analysis:home')  # ou une autre route adaptée
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/student_signup.html', {'form': form})

# Vue d'inscription pour professeurs
def professor_signup(request):
    if request.method == 'POST':
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.PROFESSOR  # ou simplement 'professor'
            user.save()
            login(request, user)
            return redirect('text_analysis:home')
    else:
        form = ProfessorSignUpForm()
    return render(request, 'registration/professor_signup.html', {'form': form})

# choix : étudiant ou professeur
def signup_choice(request):
    return render(request, 'registration/signup_choice.html')

@login_required
def dashboard(request):
    user = request.user
    # Vous pouvez personnaliser le contenu en fonction du rôle
    if user.role == 'professor':
        template = 'accounts/professor_dashboard.html'
    elif user.role == 'student':
        template = 'accounts/student_dashboard.html'
    else:
        template = 'accounts/dashboard.html'
    return render(request, template, {})