from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

router = SimpleRouter()
router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
