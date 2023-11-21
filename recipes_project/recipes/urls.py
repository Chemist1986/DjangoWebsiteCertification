from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import (
    profile, create_profile, YourDetailView, YourUpdateView, RecipeUpdateView, 
    RecipeListView, RecipeDetailView, RecipeCreateView, 
    CustomLoginView, CustomSignupView, RecipeDeleteView, YourDeleteView
    )

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/<int:pk>/', YourDetailView.as_view(), name='recipe_detail'),
    path('recipe/<int:pk>/edit/', YourUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<int:pk>/delete/', YourDeleteView.as_view(), name='recipe_delete'),
    path('login/', LoginView.as_view(), name='login'),  
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', CustomSignupView.as_view(), name='signup'),
    path('accounts/custom-login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('__debug__/', include('debug_toolbar.urls')),
]
