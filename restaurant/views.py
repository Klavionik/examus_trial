from json import loads, JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView
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
    order_key = 'order'
    queryset = Category.objects.all().prefetch_related('menu_items')

    def get(self, request, *args, **kwargs):
        try:
            del self.request.session[self.order_key]
        except KeyError:
            pass
        return super().get(request, args, kwargs)


class AddItemView(View):
    order_key = 'order'

    def post(self, request, *args, **kwargs):
        data = self.decode_request()
        item_qty = self.update_order(data)
        response = {'qty': item_qty}
        return JsonResponse(data=response)

    def update_order(self, data):
        item_id = data.get('item_id')
        order = self.request.session.setdefault(self.order_key, {})
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
        self.request.session[self.order_key][item_id] = item_qty
        self.request.session.modified = True
        return item_qty

    @staticmethod
    def item_exists(item_id):
        return MenuItem.objects.filter(id=item_id).exists()


class QuoteView(View):
    order_key = 'order'
    template_name = 'quote.html'

    def post(self, request, *args, **kwargs):
        subtotal, order = self.get_quote()
        ctx = {'subtotal': subtotal, 'order': order}
        return render(request, self.template_name, ctx)

    def get_quote(self):
        order = self.request.session.get(self.order_key)

        if order is None:
            return redirect('menu')

        qs = list(MenuItem.objects.filter(id__in=order.keys()).prefetch_related('allergens'))
        subtotal, order_content = self.quote(order, qs)
        return subtotal, order_content

    @staticmethod
    def quote(order, qs):
        def item_qty(item):
            return order[str(item.id)]

        order_content = []
        subtotal = 0

        for menu_item in qs:
            qty = item_qty(menu_item)
            item_subtotal = menu_item.price * qty
            subtotal += item_subtotal
            order_content.append((menu_item, item_subtotal, qty))

        return subtotal, order_content


class HomeRedirectView(RedirectView):
    url = reverse_lazy('menu')
