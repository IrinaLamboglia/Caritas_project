<<<<<<< HEAD
# Generated by Django 4.1 on 2024-05-06 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_usuario_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='porDesbloquear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
=======
# Generated by Django 4.1 on 2024-05-06 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_usuario_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='porDesbloquear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
>>>>>>> origin/nuevo
