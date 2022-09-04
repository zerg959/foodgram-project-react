from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path(
    #     'redoc/',
    #     TemplateView.as_view(template_name='redoc.html')
    # ),
    path('', include('api.urls'))]
