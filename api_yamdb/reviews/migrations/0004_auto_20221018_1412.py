# Generated by Django 2.2.16 on 2022-10-18 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_categories_genre_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('author', 'title')},
        ),
    ]
