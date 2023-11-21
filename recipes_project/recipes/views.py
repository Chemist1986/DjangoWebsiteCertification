from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, Profile
from .forms import CustomSignupForm, RecipeForm, ProfileForm 
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from allauth.account.views import SignupView
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def user_signed_up_callback(request, user, **kwargs):
    return redirect('login')

class CustomSignupView(SignupView):
    form_class = CustomSignupForm

class CustomLoginView(BaseLoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('recipes')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    model = Recipe
    template_name = 'recipes/recipe_form.html'
    fields = '__all__'
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})
    
class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipe-detail')

class YourUpdateView(UpdateView):
    model = Recipe
    template_name = 'recipes/recipe_form.html'
    fields = ['title', 'description', 'preparation_steps', 'preparation_time', 'image']

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})

class YourDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return HttpResponseForbidden("У Вас нет прав на удаление этого рецепта.")
        return super().get(request, *args, **kwargs)

class YourDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def create_profile(request):
    user = request.user
    profile = Profile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'create_profile.html', {'form': form, 'profile': profile})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Обязательный вызов для сохранения связанных полей (категорий)
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Проверка, что пользователь является автором рецепта
    if recipe.author != request.user:
        return redirect('recipe_detail', pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            form.save_m2m()  # Обязательный вызов для сохранения связанных полей (категорий)
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {'form': form, 'recipe': recipe})