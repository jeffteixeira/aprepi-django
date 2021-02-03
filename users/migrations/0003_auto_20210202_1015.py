# Generated by Django 3.1.5 on 2021-02-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210129_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='treatment',
            field=models.CharField(choices=[('HM', 'Hemodiálise'), ('DP', 'Diálise Peritoneal'), ('TP', 'Transplantado')], max_length=3),
        ),
    ]