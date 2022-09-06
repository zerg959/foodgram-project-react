from django.db.models import Sum
from django.db.models.expressions import Exists, OuterRef, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (CountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          RecipesCreateSerializer, RecipesSerializer,
                          ShoppingCartSerializer, TagsSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    filter_class = RecipeFilter
    pagination_class = None
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filterset_class = IngredientSearchFilter


class RecipesViewSet(viewsets.ModelViewSet):
    path_name = 'recipe__ingredients__name'
    path_measurement_unit = (
        'recipe__ingredients__measurement_unit'
    )
    path_amount = 'recipe__countingredient__amount'
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

    def favorite_and_shopping_cart(self, request, pk, model, serializer):
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
        return self.favorite_and_shopping_cart(
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
        return self.favorite_and_shopping_cart(
            request,
            pk,
            model=ShoppingCart,
            serializer=ShoppingCartSerializer()
        )

    @action(
        detail=False,
        methods=['GET', ],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        ingredients = (
            request.user.shopping_cart.values(
                self.path_name,
                self.path_measurement_unit)
            .order_by(self.path_name).annotate(total=Sum(self.path_amount))
        )
        shopping_cart = (
            f'{"---------Foodgram Shop List----------"}'
        )
        for ingredient in ingredients:
            shopping_cart += f'\n{ingredient[self.path_name]} ' \
                              f'({ingredient[self.path_measurement_unit]}) ' \
                              f'- {ingredient["total"]}'
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
