from django.db.backends.signals import connection_created
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
import logging

logger = logging.getLogger('xfb_pay_app')

@receiver(connection_created)
def log_database_connection(sender, connection, **kwargs):
    logger.info(f"数据库连接创建 - {connection.alias}")

@receiver(pre_save)
def log_model_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        action = "创建"
    else:
        action = "更新"
    
    logger.info(
        f"数据库操作 - "
        f"动作:{action} "
        f"模型:{sender.__name__} "
        f"ID:{instance.pk if instance.pk else 'NEW'} "
        f"数据:{str(instance.__dict__)}"
    )

@receiver(post_delete)
def log_model_deletion(sender, instance, **kwargs):
    logger.info(
        f"数据库操作 - "
        f"动作:删除 "
        f"模型:{sender.__name__} "
        f"ID:{instance.pk}"
    ) 