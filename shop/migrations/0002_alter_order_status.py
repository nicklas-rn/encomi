# Generated by Django 4.0.6 on 2022-08-30 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('not handled', 'not handled'), ('on the way', 'on the way')], default='not handled', max_length=200),
        ),
    ]