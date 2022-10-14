# Generated by Django 3.2.16 on 2022-10-13 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_auto_20221013_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='variants',
            field=models.ManyToManyField(to='tests.Variant'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tests.test', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=160, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('radio', 'Один правильный ответ'), ('checkbox', 'Несколько правильных ответов')], max_length=50, verbose_name='Тип вопроса'),
        ),
        migrations.AlterField(
            model_name='test',
            name='attempts',
            field=models.IntegerField(choices=[(0, 'Не ограничено'), (1, 'Одна попытка'), (2, 'Две попытки'), (3, 'Три попытки')], default=0, verbose_name='Количество попыток'),
        ),
    ]
