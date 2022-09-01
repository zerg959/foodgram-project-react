# Generated by Django 3.2.7 on 2022-09-01 10:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countingredient',
            options={'verbose_name': 'Ingredient(s) amount in recipe'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Favorite(s)'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredient(s)'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pk',), 'verbose_name': 'Recipe(s)'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Shop list'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag(s)'},
        ),
        migrations.AlterField(
            model_name='countingredient',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='countingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=150, verbose_name='Unit'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cooking time'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='Recipe'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, verbose_name='HEX-code'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='tag'),
        ),
    ]