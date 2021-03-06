# Generated by Django 4.0.2 on 2022-02-06 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NFT_GEN', '0009_alter_projectdesc_stats'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_name', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.CharField(blank=True, max_length=6, null=True)),
                ('stats', models.TextField(blank=True, null=True)),
                ('img_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
