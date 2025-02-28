# Generated by Django 5.1.5 on 2025-01-31 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_faq_question_gu_faq_question_kn_faq_question_ml_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='answer_bn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_gu',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_hi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_kn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_ml',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_mr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_or',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_pa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_ta',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_te',
            field=models.TextField(blank=True, null=True),
        ),
    ]
