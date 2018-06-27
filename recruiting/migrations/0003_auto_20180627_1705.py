# Generated by Django 2.0.6 on 2018-06-27 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0002_auto_20180626_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen_name', models.CharField(max_length=500, null=True)),
                ('file_screen', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='exchangeresult',
            name='screenshot_list',
            field=models.ManyToManyField(to='recruiting.Screenshot'),
        ),
    ]
