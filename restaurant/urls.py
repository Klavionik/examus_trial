from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from restaurant.views import MenuItemView, MenuView, AddItemView, QuoteView, HomeRedirectView

urlpatterns = [
    path('api/menu-items/', MenuItemView.as_view(), name='menu-items'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('add/', AddItemView.as_view(), name='add'),
    path('quote/', QuoteView.as_view(), name='quote'),
    path('', HomeRedirectView.as_view(), name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
