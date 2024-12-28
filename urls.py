from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... 现有的 URL 配置 ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 