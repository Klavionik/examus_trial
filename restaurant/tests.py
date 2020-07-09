from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, override_settings

from restaurant.models import Category, Allergen

FAKE_MEDIA_ROOT = TemporaryDirectory()


@override_settings(MEDIA_ROOT=FAKE_MEDIA_ROOT.name)
class CreateMenuItemTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.salads = Category.objects.create(name='Салаты')
        cls.shellfish = Allergen.objects.create(name='Молюски')
        cls.eggs = Allergen.objects.create(name='Яйца')
        cls.soy = Allergen.objects.create(name='Соя')

    def test_create_menuitem(self):
        path = reverse('menu-items')
        token_header = {'HTTP_X_ACCESS_TOKEN': settings.ACCESS_TOKEN}

        with BytesIO() as buffer:
            payload = {
                'name': 'Карибский салат с креветками',
                'image': self.get_test_img(buffer),
                'category': self.salads.id,
                'price': 800,
                'calories': 600,
                'allergens': [self.eggs.id, self.soy.id, self.shellfish.id]
            }

            response = self.client.post(path, payload, **token_header)

        self.assertEqual(response.status_code, 201, 'Блюдо добавлено')

    @staticmethod
    def get_test_img(buffer):
        _image = Image.new('RGB', size=(1, 1), color=(0, 0, 0))
        _image.save(buffer, 'JPEG')
        buffer.name = 'carribeansaladshrimp.jpg'
        buffer.seek(0)
        return buffer
