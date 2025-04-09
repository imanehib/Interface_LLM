from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

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

# Vue d'inscription (Signup)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connecter l'utilisateur après inscription
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil (ou une page dédiée)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
