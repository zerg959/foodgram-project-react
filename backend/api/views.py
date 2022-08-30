import io

from django.db.models import Sum
from django.db.models.expressions import Exists, OuterRef, Value
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import User
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, IngredientsCount
from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import AuthorOrReadOnly
from .pagination import CustomPagination
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          RecipesCreateSerializer, RecipesSerializer,
                          ShoppingCartSerializer, TagsSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    filter_class = RecipeFilter
    pagination_class = None
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    path_name = 'recipe__ingredients__name'
    path_measurement_unit = (
        'recipe__ingredients__measurement_unit'
    )
    path_amount = 'recipe__ingredientscount__amount'
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend, ]
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [AuthorOrReadOnly, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=user, recipe=OuterRef('id'))
                ),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=user, recipe=OuterRef('id'))
                )
            ).select_related('author', )
        else:
            return Recipe.objects.annotate(
                is_favorited=Value(False), is_in_shopping_cart=Value(False))

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSerializer
        return RecipesCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def favorite_and_sopping_cart(self, request, pk, model, serializer):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            model.objects.get_or_create(
                user=user, recipe=recipe
            )
            return Response(
                serializer.to_representation(instance=recipe),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            model.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='favorite'
    )
    def favorite(self, request, pk):
        return self.favorite_and_sopping_cart(
            request,
            pk,
            model=Favorite,
            serializer=FavoriteSerializer()
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly, ],
        url_path='shopping_cart'
    )
    def shopping_cart(self, request, pk):
        return self.favorite_and_sopping_cart(
            request,
            pk,
            model=ShoppingCart,
            serializer=ShoppingCartSerializer()
        )

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def load_shop_list(self, request):
        """Load Shop List"""
        user = get_object_or_404(User, username=request.user)
        recipes_id = ShoppingCart.objects.filter(user=user).values('recipe')
        recipes = Recipe.objects.filter(pk__in=recipes_id)
        shop_dict = {}
        n_rec = 0
        for recipe in recipes:
            n_rec += 1
            ing_amounts = IngredientsCount.objects.filter(recipe=recipe)
            for item in ing_amounts:
                if item.ingredient.name in shop_dict:
                    shop_dict[item.ingredient.name][0] += item.amount
                else:
                    shop_dict[item.ingredient.name] = [
                        item.amount,
                        item.ingredient.measurement_unit
                    ]
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y")
        shop_string = (
            f'FoodGram ShopList:\
             \n-------------------'
        )
        for key, value in shop_dict.items():
            shop_string += f'\n{key} ({value[1]}) - {str(value[0])}'
        return HttpResponse(shop_string, content_type='text/plain')


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = IngredientSearchFilter
