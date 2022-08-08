# Generated by Django 3.2.14 on 2022-07-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='uploads/')),
                ('min_bid', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
