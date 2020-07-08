from django.db import models


class Category(models.Model):
    name = models.CharField(
        'название категории',
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class MenuItem(models.Model):
    name = models.CharField(
        'название блюда',
        max_length=100,
        unique=True,
    )
    image = models.ImageField(
        'изображение блюда',
        upload_to='menu_items',
    )
    price = models.PositiveIntegerField(
        'цена блюда',
    )
    calories = models.PositiveIntegerField(
        'пищевая ценность',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.CASCADE,
        related_name='menu_items',
    )
    allergens = models.ManyToManyField(
        'Allergen',
        verbose_name='аллергены',
        related_name='menu_items'
    )

    def __str__(self):
        return f'{self.category.name} {self.name}'

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'


class Allergen(models.Model):
    name = models.CharField(
        'название аллергена',
        max_length=100,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'аллерген'
        verbose_name_plural = 'аллергены'
