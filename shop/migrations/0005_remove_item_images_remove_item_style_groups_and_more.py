# Generated by Django 4.0.6 on 2022-07-27 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_stylegroup_item_style_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='images',
        ),
        migrations.RemoveField(
            model_name='item',
            name='style_groups',
        ),
        migrations.RemoveField(
            model_name='stylegroup',
            name='styles',
        ),
        migrations.AddField(
            model_name='image',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.item'),
        ),
        migrations.AddField(
            model_name='style',
            name='style_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.stylegroup'),
        ),
        migrations.AddField(
            model_name='stylegroup',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.item'),
        ),
    ]
