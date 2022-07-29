# Generated by Django 4.0.6 on 2022-07-29 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_category_alter_item_keywords_image_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='categories',
        ),
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(to='shop.category'),
        ),
    ]