# Generated by Django 3.1.7 on 2021-03-27 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('calories', models.DecimalField(decimal_places=2, max_digits=6)),
                ('carbs', models.DecimalField(decimal_places=2, max_digits=6)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sugar', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
