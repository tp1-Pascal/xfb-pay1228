from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, CustomerService, Order

# 表单验证
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3 or len(name) > 30:
            raise forms.ValidationError('商品名称必须在3-30个汉字之间')
        return name
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0.01 or price > 99999.99:
            raise forms.ValidationError('商品定价必须在0.01-99999.99元之间')
        return price

# 商品管理
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm  # 使用自定义表单
    list_display = (
        'name',
        'price',
        'is_active',
        'updated_at',
        'purchase_count',
    )
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'name',
                'price',
                'user_day',
            ),
            'description': '商品的基本信息'
        }),
        ('图片信息', {
            'fields': (
                'cover_image',
                'detail_image',
            ),
            'description': '商品的图片信息，支持gif、png、bmp、jpg格式'
        }),
        ('状态信息', {
            'fields': (
                'is_active',
                'purchase_count',
                'view_count',
                'get_product_link',
            ),
            'description': '商品的状态信息'
        }),
        ('时间信息', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
        ('其他信息', {
            'fields': (
                'notes',
            ),
            'description': '商品的备注信息，0-9999个汉字'
        }),
    )

    readonly_fields = [
        'purchase_count',
        'view_count',
        'created_at',
        'updated_at',
        'get_product_link',
    ]
    
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['-updated_at']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].help_text = '3-30个汉字'
        form.base_fields['price'].help_text = '0.01-99999.99元'
        form.base_fields['user_day'].help_text = '商品可使用的天数'
        form.base_fields['notes'].help_text = '0-9999个汉字'
        return form

    def save_model(self, request, obj, form, change):
        """只有被修改的字段被存储"""
        if change:
            original = self.model.objects.get(pk=obj.pk)
            changed_fields = []
            for field in form.changed_data:
                if field not in ['purchase_count', 'view_count']:
                    changed_fields.append(field)
                    setattr(obj, field, form.cleaned_data[field])
            if changed_fields:
                obj.save(update_fields=changed_fields + ['updated_at'])
        else:
            obj.save()

    def get_product_link(self, obj):
        if obj.url_code:
            url = reverse('xfb_pay_app:product_detail', kwargs={'url_code': obj.url_code})
            return mark_safe(f'<a href="{url}" target="_blank">查看商品链接</a>')
        return "尚未生成链接"
    get_product_link.short_description = '商品链接'

# 客服管理
@admin.register(CustomerService)
class CustomerServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    search_fields = ['name', 'phone']
    exclude = ('session_key', 'password')
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑时
            return self.readonly_fields + ('phone',)
        return self.readonly_fields

# 订单管理
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'get_product_info',
        'total_amount',
        'payment_status',
        'created_at',
        'completed_at',
        'buyer_name',
        'buyer_phone',
    )

    search_fields = [
        'order_number',
        'buyer_name',
        'buyer_phone',
        'buyer_company',
    ]

    list_filter = [
        'payment_status',
        'customer_service',
        'created_at',
    ]

    ordering = ['-updated_at']

    fieldsets = (
        ('订单信息', {
            'fields': (
                'order_number',
                'product',
                'total_amount',
                'payment_status',
                'get_user_day',
            )
        }),
        ('时间信息', {
            'fields': (
                'created_at',
                'completed_at',
            )
        }),
        ('买家信息', {
            'fields': (
                'buyer_nickname',
                'buyer_name',
                'buyer_phone',
                'buyer_company',
            )
        }),
        ('其他信息', {
            'fields': (
                'customer_service',
                'notes',
            )
        }),
    )

    readonly_fields = [
        'order_number',
        'created_at',
        'completed_at',
        'get_user_day',
    ]

    def get_user_day(self, obj):
        """获取商品使用天数"""
        if obj.product:
            return f"{obj.product.user_day} 天"
        return f"{obj.product_user_day} 天" if obj.product_user_day else "未设置"
    get_user_day.short_description = '使用天数'

    def save_model(self, request, obj, form, change):
        """在保存订单时，自动设置总金额为商品价格"""
        if obj.product and not change:
            obj.total_amount = obj.product.price    
        super().save_model(request, obj, form, change)
    
    def get_product_info(self, obj):
        """获取商品信息"""
        if obj.product:
            return obj.product.name
        return obj.product_name or '商品已删除'
    get_product_info.short_description = '商品'

# 自定义管理界面标题
admin.site.site_header = "小法博销售页面管理"
admin.site.site_title = "小法博销售页面"
admin.site.index_title = "管理中心"