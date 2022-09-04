from django.urls import include, path

from .views import ChangePasswordView, SubscriptionViewSet, UserViewSet

app_name = 'users'

urlpatterns = [
    path('me/', UserViewSet.as_view(
        {'get': 'me'}), name='users_get'),
    path('set_password/', ChangePasswordView.as_view(
        {'post': 'update'}), name='set_password'),
    path('', include('djoser.urls.authtoken')),
    path('subscriptions/', SubscriptionViewSet.as_view(
        {'get': 'list'}), name='subscriptions'),
    path('<int:pk>/subscribe/', SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'perform_destroy'}), name='subscribe'),
]
