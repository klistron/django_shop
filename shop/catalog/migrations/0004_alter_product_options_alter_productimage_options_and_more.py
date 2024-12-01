# Generated by Django 4.2.13 on 2024-06-20 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_alter_tag_products"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "Товар", "verbose_name_plural": "Товары"},
        ),
        migrations.AlterModelOptions(
            name="productimage",
            options={
                "verbose_name": "Изображение товара",
                "verbose_name_plural": "Изображение товаров",
            },
        ),
        migrations.AlterModelOptions(
            name="productspecification",
            options={
                "verbose_name": "Характеристика",
                "verbose_name_plural": "Характеристики",
            },
        ),
        migrations.AlterModelOptions(
            name="review",
            options={"verbose_name": "Отзыв", "verbose_name_plural": "Отзывы"},
        ),
        migrations.AlterField(
            model_name="categories",
            name="title",
            field=models.CharField(
                max_length=100, unique=True, verbose_name="Название категории"
            ),
        ),
    ]
