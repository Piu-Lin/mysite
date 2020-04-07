# Generated by Django 3.0.4 on 2020-04-01 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_readnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='readNum',
        ),
        migrations.CreateModel(
            name='readNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readNum', models.IntegerField(default=0)),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog')),
            ],
        ),
    ]