# Generated by Django 5.0.2 on 2024-03-08 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdPages', '0002_visitor_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100)),
                ('country_name', models.CharField(max_length=100)),
                ('coordinates', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]