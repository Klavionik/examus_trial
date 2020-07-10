from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from restaurant.views import MenuItemView, MenuView, AddItemView

urlpatterns = [
    path('api/menu-items/', MenuItemView.as_view(), name='menu-items'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('add/', AddItemView.as_view(), name='add'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
