from django.urls import path
from . import views

app_name = 'xfb_pay_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<str:url_code>/', views.product_detail, name='product_detail'),
] 