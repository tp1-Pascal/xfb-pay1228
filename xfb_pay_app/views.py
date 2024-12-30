from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
import logging

logger = logging.getLogger('xfb_pay_app')

def index(request):
    """
    首页视图函数
    """
    logger.info(f"访问首页 - IP: {request.META.get('REMOTE_ADDR')}")
    return HttpResponse("XFB Pay App Index Page")

def product_detail(request, url_code):
    """
    产品详情页视图
    """
    try:
        logger.info(f"查看商品详情 - URL Code: {url_code}, IP: {request.META.get('REMOTE_ADDR')}")
        product = get_object_or_404(Product, url_code=url_code)
        logger.debug(f"商品信息 - ID: {product.id}, 名称: {product.name}, 价格: {product.price}")
        return render(request, 'xfb_pay_app/product_detail.html', {'product': product})
    except Exception as e:
        logger.error(f"访问商品详情页面出错 - URL Code: {url_code}, 错误: {str(e)}")
        raise

__all__ = ['index', 'product_detail']
