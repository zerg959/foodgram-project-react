from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'name',
        unique=True,
        max_length=150,
    )
    measurement_unit = models.CharField(
        'Unit',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Ingredient(s)'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(
        'name',
        unique=True,
        max_length=150,
    )
    color = models.CharField(
        'HEX-code',
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='tag',
    )

    class Meta:
        verbose_name = 'Tag(s)'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """Recipe model."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='CountIngredient'
    )
    name = models.CharField(
        'name',
        max_length=200,
    )
    image = models.ImageField('Image', blank=True)
    text = models.TextField('Recipe')
    cooking_time = models.PositiveIntegerField(
        'Cooking time',
        validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Recipe(s)'
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.name}'


class CountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='count_ingredients',
    )
    amount = models.PositiveIntegerField('Amount',
                                         validators=[MinValueValidator(1)])
    def amount_validator(self, amount):
        if amount < 1:
            raise ValueError(
                'Amount cant be < 1'
            )


    class Meta:
        verbose_name = 'Ingredient(s) amount in recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites')

    class Meta:
        verbose_name = 'Favorite(s)'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart')

    class Meta:
        verbose_name = 'Shop list'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.user}'
