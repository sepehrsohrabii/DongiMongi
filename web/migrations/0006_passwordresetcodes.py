# Generated by Django 3.0.4 on 2020-03-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20200328_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passwordresetcodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=120)),
                ('time', models.DateTimeField()),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
