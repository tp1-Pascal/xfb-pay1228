from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import uuid
import hmac
import hashlib
import random
import string
from datetime import timedelta
import logging
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import os
from PIL import Image
from django.urls import reverse

logger = logging.getLogger('xfb_pay_app')


class BaseModel(models.Model):
    """
    基础模型类，包含共用字段和方法
    """
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间"
    )

    class Meta:
        abstract = True

class CustomerService(BaseModel):
    """
    客服模型
    处理客服账号的认证和管理
    """
    name = models.CharField(
        max_length=50, 
        verbose_name="客服姓名"
    )
    phone = models.CharField(
        max_length=15, 
        unique=True, 
        verbose_name="客服手机号"
    )
    password = models.CharField(
        max_length=128, 
        verbose_name="客服密码"
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="会话密钥"
    )

    class Meta:
        verbose_name = "客服"
        verbose_name_plural = "客服管理"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def save(self, *args, **kwargs):
        if not self.pk:  # 新建客服��密密码
            self.password = make_password(self.password)
        elif 'update_fields' in kwargs and 'password' in kwargs['update_fields']:
            # 明确更新密码字段时加密
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """检查密码是否正确"""
        return check_password(raw_password, self.password)

def validate_image(image):
    """验证上传的图片"""
    if not image:
        return

    # 检查文件大小
    if image.size > settings.IMAGE_UPLOAD_MAX_SIZE:
        raise ValidationError(f'图片大小不能超过 {settings.IMAGE_UPLOAD_MAX_SIZE/1024/1024}MB')

    # 检查文���扩展名
    file_extension = os.path.splitext(image.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if file_extension not in allowed_extensions:
        raise ValidationError('只允许上传 JPG、JPEG、PNG 或 GIF 格式的图片')

    return None

class Product(BaseModel):
    """
    商品模型
    处理商品信息和链接成
    """
    name = models.CharField(
        max_length=200, 
        verbose_name="商品名称"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="商品定价"
    )
    user_day = models.IntegerField(
        default=0, 
        verbose_name="用户使用天数"
    )
    cover_image = models.ImageField(
        upload_to=settings.PRODUCT_COVERS_DIR,
        verbose_name="封面图片",
        validators=[validate_image],
        help_text="支持jpg、png、gif格式，大小不超过5MB",
        null=True,
        blank=True
    )
    detail_image = models.ImageField(
        upload_to=settings.PRODUCT_DETAILS_DIR,
        verbose_name="详情图片",
        validators=[validate_image],
        help_text="支持jpg、png、gif格式，大小不超过5MB",
        null=True,
        blank=True
    )
    url_code = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="商品编码", 
        blank=True
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="是否上架"
    )
    purchase_count = models.IntegerField(
        default=0, 
        verbose_name="购买次数"
    )
    view_count = models.IntegerField(
        default=0, 
        verbose_name="浏览次数"
    )
    notes = models.TextField(
        verbose_name="商品备注信息", 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品管理"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (¥{self.price})"

    def save(self, *args, **kwargs):
        # 生成商品编码
        if not self.url_code:
            self.url_code = self._generate_unique_code()
        
        # 更新时间处理
        if self.pk:
            try:
                original = Product.objects.get(pk=self.pk)
                if original.view_count != self.view_count or original.purchase_count != self.purchase_count:
                    kwargs['update_fields'] = [f for f in kwargs.get('update_fields', []) 
                                             if f not in ['updated_at']]
                    self.updated_at = original.updated_at
            except Product.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        """生成唯一商品编码"""
        while True:
            code = self._generate_code()
            if not Product.objects.filter(url_code=code).exists():
                return code

    @staticmethod
    def _generate_code():
        """生成商品编码"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=4))
        sequence = ''.join(random.choices(string.digits, k=4))
        code = f"{timestamp}{random_str}{sequence}"
        total = sum(int(d) * (i % 10 + 1) for i, d in enumerate(code))
        check_digit = str(total % 10)
        return f"{code}{check_digit}"

    def get_absolute_url(self):
        return reverse('xfb_pay_app:product_detail', kwargs={'url_code': self.url_code})

class Order(BaseModel):
    """
    订单模型
    处理订单信息和支付流程
    """
    PAYMENT_STATUS_CHOICES = [
        ('paid', '已支付'),
        ('pending', '待支付'),
        ('canceled', '已取消')
    ]

    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="商品"
    )
    product_name = models.CharField(
        max_length=200,
        verbose_name="商品名称",
        null=True,
        blank=True
    )
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="订单金额",
        null=True,
        blank=True
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="总金额"
    )
    customer_service = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="归属客服"
    )
    buyer_nickname = models.CharField(
        max_length=20, 
        default='未知', 
        verbose_name="买家微信昵称"
    )
    buyer_name = models.CharField(
        max_length=8, 
        verbose_name="买家姓名"
    )   
    buyer_phone = models.CharField(
        max_length=11, 
        verbose_name="买家联系电话"
    )
    buyer_company = models.CharField(
        max_length=50, 
        verbose_name="买家工作单位"
    )
    completed_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="完成时间"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="支付状态"
    )
    notes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="备注", 
        max_length=3000
    )
    order_number = models.CharField(
        max_length=32, 
        unique=True, 
        verbose_name='订单号', 
        null=True, 
        blank=True
    )
    payment_link = models.CharField(
        max_length=255, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name='支付链接'
    )
    payment_link_expires = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='支付链接过期时间'
    )
    payment_link_used = models.BooleanField(
        default=False, 
        verbose_name='支付链接是否已用'
    )
    payment_code = models.CharField(
        max_length=32, 
        unique=True, 
        verbose_name='支付码', 
        null=True, 
        blank=True
    )
    product_user_day = models.IntegerField(
        default=0,
        verbose_name="商品使用天数",
        null=True,
        blank=True
    )
    order_name = models.CharField(
        max_length=200,
        verbose_name="订单商品名称",
        help_text="订单创建时的商品名称，不随原商品变化",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单管理"
        ordering = ['-created_at']

    def __str__(self):
        product_name = self.product.name if self.product else self.product_name or '商品已删除'
        return f"订单 {self.order_number} - {product_name}"

    def save(self, *args, **kwargs):
        # 保存商品信息
        if self.product and not self.product_name:
            self.product_name = self.product.name
            self.order_price = self.product.price
            self.product_user_day = self.product.user_day
            if not self.total_amount:
                self.total_amount = self.product.price

        is_new = self.pk is None
        
        if is_new:
            self._generate_order_codes()
        elif 'payment_status' in kwargs.get('update_fields', []):
            self._handle_payment_status_change()
        
        super().save(*args, **kwargs)

    def _generate_order_codes(self):
        """生成订单号和支付码"""
        while True:
            order_number = self._generate_unique_code('O')
            if not Order.objects.filter(order_number=order_number).exists():
                self.order_number = order_number
                break
                
        while True:
            payment_code = self._generate_unique_code('P')
            if not Order.objects.filter(payment_code=payment_code).exists():
                self.payment_code = payment_code
                break

    def _handle_payment_status_change(self):
        """处理支付状态变更"""
        try:
            original = Order.objects.get(pk=self.pk)
            if original.payment_status != 'paid' and self.payment_status == 'paid':
                self.product.purchase_count += 1
                self.product.save(update_fields=['purchase_count'])
        except Order.DoesNotExist:
            pass

    def generate_payment_link(self, secret_key=None):
        """生成支付链接"""
        if not secret_key:
            secret_key = settings.PAYMENT_SECRET_KEY

        if not self.order_number:
            self.order_number = self._generate_unique_code('O')
        
        payment_id = str(uuid.uuid4())[:8]
        timestamp = int(timezone.now().timestamp())
        
        message = f"{self.order_number}:{payment_id}:{timestamp}"
        signature = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()[:16]
        
        self.payment_link_expires = timezone.now() + timedelta(minutes=30)
        self.payment_link = f"{payment_id}:{signature}"
        self.save(update_fields=['payment_link', 'payment_link_expires'])
        
        return self.payment_link

    @staticmethod
    def _generate_unique_code(prefix):
        """生成唯一编码"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=4))
        sequence = str(random.randint(0, 999)).zfill(3)
        
        code = f"{prefix}{timestamp}{random_str}{sequence}"
        digits_only = ''.join(c for c in code if c.isdigit())
        total = sum(int(d) * (i % 10 + 1) for i, d in enumerate(digits_only))
        check_digit = str(total % 10)
        
        return f"{code}{check_digit}"

    @staticmethod
    def verify_payment_link(payment_link, secret_key=None):
        """验证支付链接"""
        if not secret_key:
            secret_key = settings.PAYMENT_SECRET_KEY

        try:
            payment_id, signature = payment_link.split(':')
            
            valid_time = timezone.now() - timedelta(minutes=30)
            order = Order.objects.filter(
                payment_link__startswith=payment_id,
                payment_link_expires__gt=timezone.now(),
                created_at__gt=valid_time,
                payment_status='pending'
            ).first()
            
            if not order:
                return None, "支付链接无效或已过期"
            
            if order.payment_link_used:
                return None, "支付链接已使用"
                
            return order, None
            
        except ValueError:
            return None, "支付链接格式错误"
        except Exception as e:
            return None, f"验证失败: {str(e)}"