from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product

def index(request):
    """
    首页视图函数
    """
    return HttpResponse("XFB Pay App Index Page")

def product_detail(request, url_code):
    """
    产品详情页视图
    """
    product = get_object_or_404(Product, url_code=url_code)
    return render(request, 'xfb_pay_app/product_detail.html', {'product': product})

__all__ = ['index', 'product_detail']
