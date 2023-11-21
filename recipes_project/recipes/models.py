from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preparation_steps = models.TextField(verbose_name='Шаги приготовления')
    preparation_time = models.PositiveIntegerField(verbose_name='Время приготовления в минутах')
    image = models.ImageField(upload_to='recipe_images/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    # categories = models.ManyToManyField(Category, through='RecipeCategoryRelation', related_name='recipes', verbose_name='Категории')
    
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'

    CATEGORY_CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин'),
    ]

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default=BREAKFAST,
        verbose_name='Категория',
    )

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})

class RecipeCategoryRelation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    is_primary = models.BooleanField(default=False, verbose_name='Основная категория')

    def __str__(self):
        return f'{self.recipe.title} - {self.category.name}'

   
