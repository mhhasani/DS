# Generated by Django 3.1.7 on 2021-09-30 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daneshjoo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daneshjoo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daneshjoo', to='friend.daneshjoo')),
                ('friend', models.ManyToManyField(related_name='friend', to='friend.Daneshjoo')),
            ],
        ),
    ]