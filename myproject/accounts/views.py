from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
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
        # Par exemple, on peut transmettre un paramètre "role" pour adapter l'affichage
        context['role'] = self.request.GET.get('role', '')
        return context


# Vue de déconnexion (Logout)
class CustomLogoutView(LogoutView):
    next_page = '/'  # Redirige vers la page d'accueil après la déconnexion


# Vue d'inscription pour étudiants
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Assigner le rôle étudiant
            user.role = CustomUser.STUDENT  # Ou 'student' si vous avez défini des chaînes
            user.save()
            login(request, user)
            return redirect('text_analysis:home')  # Redirige vers le correcteur de texte ou une autre page
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/student_signup.html', {'form': form})


# Vue d'inscription pour professeurs
def professor_signup(request):
    if request.method == 'POST':
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Assigner le rôle professeur
            user.role = CustomUser.PROFESSOR  # Ou 'professor'
            user.save()
            login(request, user)
            return redirect('text_analysis:home')
    else:
        form = ProfessorSignUpForm()
    return render(request, 'registration/professor_signup.html', {'form': form})


# Vue d'inscription générale (si vous souhaitez garder une vue d'inscription générique)
# Cette vue peut rediriger l'utilisateur vers la page d'inscription appropriée en fonction d'un paramètre GET, par exemple.
def signup(request):
    # Si un paramètre 'role' est passé dans l'URL pour différencier le type
    role = request.GET.get('role', '')
    if role == 'professor':
        return professor_signup(request)
    else:
        # Par défaut, on redirige vers l'inscription étudiant
        return student_signup(request)
