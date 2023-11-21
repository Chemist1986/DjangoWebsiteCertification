from django import forms
from .models import Recipe, Profile, Category
from allauth.account.forms import SignupForm

class RecipeForm(forms.ModelForm):
    category = forms.CharField(max_length=255, widget=forms.Select(choices=Recipe.CATEGORY_CHOICES))
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 'preparation_steps', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields.pop('email')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'date_of_birth', 'profile_image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
