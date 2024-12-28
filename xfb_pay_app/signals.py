from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Order
import logging

logger = logging.getLogger('xfb_pay_app')

@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    """记录商品保存操作"""
    if created:
        logger.info(f"新商品创建: {instance.name}")
    else:
        logger.info(f"商品更新: {instance.name}")

@receiver(post_save, sender=Order)
def log_order_save(sender, instance, created, **kwargs):
    """记录订单保存操作"""
    if created:
        logger.info(f"新订单创建: {instance.order_number}")
    else:
        logger.info(f"订单更新: {instance.order_number}") 