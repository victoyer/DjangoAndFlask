# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-06-10 07:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='is_Delete',
            field=models.BooleanField(default=False, verbose_name='逻辑删除'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gclick',
            field=models.IntegerField(verbose_name='商品被点击次数'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gdescribe',
            field=models.CharField(max_length=200, verbose_name='商品描述'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gimg',
            field=models.ImageField(upload_to='df_goods', verbose_name='商品图片'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gname',
            field=models.CharField(max_length=30, verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gprice',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='商品价格'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gsort',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gstock',
            field=models.IntegerField(verbose_name='商品库存'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_goods.GoodsType', verbose_name='商品类型'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gunit',
            field=models.CharField(default='500g', max_length=20, verbose_name='商品规格'),
        ),
        migrations.AlterField(
            model_name='goodstype',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='逻辑删除'),
        ),
        migrations.AlterField(
            model_name='goodstype',
            name='typename',
            field=models.CharField(max_length=20, verbose_name='分类名称'),
        ),
    ]
