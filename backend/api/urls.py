from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from users.views import UserViewSet


router = SimpleRouter()
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'users', UserViewSet, basename='users')
# router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
#                 basename='comments')
# router.register('ingredients', IngredientView, basename='ingredients')


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    # path('users/set_password/', ChangePasswordView.as_view(
    #     {'post': 'update'}), name='set_password'
    #      ),
]
