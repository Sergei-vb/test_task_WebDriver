# Generated by Django 2.0.6 on 2018-06-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file_image',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='image_list',
            field=models.ManyToManyField(blank=True, to='recruiting.Image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
