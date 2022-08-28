# Generated by Django 4.0.6 on 2022-08-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_rename_parentorder_order_parentorder_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='parentOrder',
            new_name='parent_order',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('not handled', 'not handled'), ('on the way', 'on the way')], default='not handled', max_length=200),
        ),
    ]
