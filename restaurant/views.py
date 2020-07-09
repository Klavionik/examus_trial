from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from restaurant.models import MenuItem
from restaurant.serializers import MenuItemSerializer
from restaurant.permissions import MenuManager


class MenuItemView(ListCreateAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = ()
    permission_classes = (MenuManager,)
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
