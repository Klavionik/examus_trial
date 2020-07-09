from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from restaurant.views import MenuItemView

urlpatterns = [
    path('api/menu-items/', MenuItemView.as_view(), name='menu-items'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
