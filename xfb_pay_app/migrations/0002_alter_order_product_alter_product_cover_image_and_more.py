# Generated by Django 4.2.8 on 2024-12-28 13:03

from django.db import migrations, models
import django.db.models.deletion
import xfb_pay_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('xfb_pay_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='xfb_pay_app.product', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cover_image',
            field=models.ImageField(blank=True, help_text='支持jpg、png、gif格式，大小不超过5MB', null=True, upload_to='products/covers', validators=[xfb_pay_app.models.validate_image], verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='product',
            name='detail_image',
            field=models.ImageField(blank=True, help_text='支持jpg、png、gif格式，大小不超过5MB', null=True, upload_to='products/details', validators=[xfb_pay_app.models.validate_image], verbose_name='详情图片'),
        ),
    ]
