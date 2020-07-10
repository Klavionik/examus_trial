from json import loads, JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from django.views import View

from restaurant.models import MenuItem, Category
from restaurant.serializers import MenuItemSerializer
from restaurant.permissions import MenuManager


class MenuItemView(ListCreateAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = ()
    permission_classes = (MenuManager,)
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()


class MenuView(ListView):
    template_name = 'menu.html'
    queryset = Category.objects.all().prefetch_related('menu_items')

    def get(self, request, *args, **kwargs):
        try:
            del self.request.session['order']
        except KeyError:
            pass
        return super().get(request, args, kwargs)


class AddItemView(View):
    def post(self, request, *args, **kwargs):
        data = self.decode_request()
        item_qty = self.update_order(data)
        response = {'qty': item_qty}
        return JsonResponse(data=response)

    def update_order(self, data):
        item_id = data.get('item_id')
        order = self.request.session.setdefault('order', {})
        return self.add_item(item_id, order)

    def decode_request(self):
        try:
            data = loads(self.request.body)
        except JSONDecodeError:
            return HttpResponse(status=400)
        return data

    def add_item(self, item_id, order):
        if not self.item_exists(item_id):
            return 0

        item_qty = order.get(item_id, 0) + 1
        self.request.session['order'][item_id] = item_qty
        self.request.session.modified = True
        return item_qty

    @staticmethod
    def item_exists(item_id):
        return MenuItem.objects.filter(id=item_id).exists()
