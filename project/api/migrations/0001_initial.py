# Generated by Django 2.1.3 on 2018-12-02 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_inserted', models.DateField()),
                ('date_invalidated', models.DateField()),
            ],
        ),
    ]
