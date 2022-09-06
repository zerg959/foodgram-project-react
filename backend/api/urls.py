from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

router = SimpleRouter()
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipesViewSet)
# router.register(r'download_shopping_cart', RecipesViewSet)
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'),
    path('', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
