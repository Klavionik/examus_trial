from django.urls import path

from restaurant.views import MenuItemView

urlpatterns = [
    path('api/menu-items/', MenuItemView.as_view(), name='menu-items'),
]
