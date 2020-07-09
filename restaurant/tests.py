from rest_framework.test import APITestCase
from restaurant.models import Category, Allergen
from django.conf import settings
from rest_framework.reverse import reverse
import os

FIXTURES_DIR = os.path.join(settings.BASE_DIR, 'restaurant', 'fixtures')


class CreateMenuItemTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.salads = Category.objects.create(name='Салаты')
        cls.shellfish = Allergen.objects.create(name='Молюски')
        cls.eggs = Allergen.objects.create(name='Яйца')
        cls.soy = Allergen.objects.create(name='Соя')

    def test_create_menuitem(self):
        path = reverse('menu-items')
        with open(os.path.join(FIXTURES_DIR, 'menu_image', 'carribeansaladshrimp.jpg'), 'rb') as fh:
            payload = {
                'name': 'Карибский салат с креветками',
                'image': fh,
                'category': self.salads.id,
                'price': 800,
                'calories': 600,
                'allergens': [self.eggs.id, self.soy.id, self.shellfish.id]
            }
            response = self.client.post(path, payload)

        self.assertEqual(response.status_code, 201, 'Блюдо добавлено')
