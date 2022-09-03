# Generated by Django 4.0.6 on 2022-09-02 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_faq_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='type',
            field=models.CharField(choices=[('seller', 'seller'), ('buyer', 'buyer')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('not handled', 'not handled'), ('on the way', 'on the way'), ('completed', 'completed')], default='not handled', max_length=200),
        ),
    ]