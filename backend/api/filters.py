import django_filters

from recipes.models import Ingredient, Recipe


class IngredientSearchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = django_filters.CharFilter()
    is_in_shopping_cart = django_filters.BooleanFilter(
        widget=django_filters.widgets.BooleanWidget())
    is_favorited = django_filters.BooleanFilter(
        widget=django_filters.widgets.BooleanWidget())

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']
