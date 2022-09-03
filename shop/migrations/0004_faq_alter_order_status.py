# Generated by Django 4.0.6 on 2022-09-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_sellerapplication_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('answer', models.TextField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('on the way', 'on the way'), ('not handled', 'not handled')], default='not handled', max_length=200),
        ),
    ]