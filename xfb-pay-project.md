# XFB Pay Project Documentation
## 项目初始化
### 1. 创建项目目录和虚拟环境
    创建项目目录
        mkdir -p /Users/wangtaiping/Desktop/Coding/xfb-pay1228
        cd /Users/wangtaiping/Desktop/Coding/xfb-pay1228
    创建并激活虚拟环境
        python -m venv venv
        source venv/bin/activate
### 2. 安装依赖
    安装基础依赖
        pip install Django==4.2.8
        pip install python-dotenv==1.0.0
        pip install Pillow==10.1.0
        pip install requests==2.31.0
        pip install cryptography==42.0.5
    保存依赖列表
        pip freeze > requirements.txt
### 3. 创建项目结构
    创建Django项目和应用
        django-admin startproject xfb_pay .
        python manage.py startapp xfb_pay_app
    创建必要目录
        mkdir -p logs
        mkdir -p xfb_pay_app/views
        mkdir -p xfb_pay_app/utils
        mkdir -p xfb_pay_app/templates
        mkdir -p xfb_pay_app/static/js
        mkdir -p xfb_pay_app/management/commands
    创建初始文件
        touch logs/debug.log
        touch xfb_pay_app/views/init.py
        touch xfb_pay_app/utils/init.py
## 项目配置
### 1. 日志配置 (settings.py)
    LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
    'verbose': {
    'format': '[{asctime}] {levelname} {module} {process:d} {thread:d} {message}',
    'style': '{',
    'datefmt': '%Y-%m-%d %H:%M:%S'
    },
    'simple': {
    'format': '[{asctime}] {levelname} {message}',
    'style': '{',
    'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    },
    'handlers': {
    'debug_file': {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': 'logs/debug.log',
    'formatter': 'verbose',
    }
    },
    'loggers': {
    'django': {
    'handlers': ['debug_file'],
    'level': 'INFO',
    'propagate': True,
    },
    'xfb_pay_app': {
    'handlers': ['debug_file'],
    'level': 'DEBUG',
    'propagate': True,
    }
    }
    }
### 2. 中间件配置 (settings.py)
    MIDDLEWARE = [
    # Django默认中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件
    'xfb_pay_app.middleware.RequestLoggingMiddleware',
    ]
## 关键功能模块

### 1. 请求日志中间件 (middleware.py)
    class RequestLoggingMiddleware:
    def call(self, request):
    start_time = time.time()
    logger.info(f"收到请求 - PATH:{request.path}")
    response = self.get_response(request)
    duration = time.time() - start_time
    logger.info(f"请求结束 - PATH:{request.path} 耗时:{duration:.2f}秒")
    return response

### 2. 错误处理 (views/error.py)
    @csrf_exempt
    def log_js_error(request):
    """接收并记录前端 JavaScript 错误"""
    if request.method == 'POST':
    error_data = request.POST.dict()
    logger.error(f"浏览器错误 - {error_data}")
    return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=405)

### 3. 系统状态监控 (management/commands/log_system_status.py)
    class Command(BaseCommand):
    help = '记录系统状态'
    def handle(self, args, options):
    while True:
    logger.info("系统状态检查")
    time.sleep(300) # 每5分钟记录一次
### 4. 依赖包记录 (utils/dependency_logger.py)
    def log_dependencies():
    """记录已安装的依赖包版本"""
    installed_packages = [
    f"{dist.metadata['Name']}=={dist.version}"
    for dist in distributions()
    ]
    logger.info("依赖包信息 - " + " | ".join(installed_packages))

## 运行项目

### 1. 初始化数据库
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
### 2. 启动开发服务器
    python manage.py runserver
### 3. 访问管理界面
    http://127.0.0.1:8000/admin/
### 4. 访问前端页面
    http://127.0.0.1:8000/

## 日志记录内容
    项目会记录以下类型的日志到 logs/debug.log：
    1. HTTP请求日志（路径、耗时）
    2. 浏览器端JavaScript错误
    3. 系统状态信息
    4. 依赖包信息
    5. Django系统日志
    6. 应用程序错误日志

## 项目结构
    xfb-pay1228/
    ├── logs/
    │ └── debug.log
    ├── xfb_pay/
    │ ├── settings.py
    │ └── urls.py
    ├── xfb_pay_app/
    │ ├── views/
    │ ├── utils/
    │ ├── templates/
    │ ├── static/
    │ ├── management/
    │ ├── middleware.py
    │ └── models.py
    ├── requirements.txt
    └── manage.py

## 关键文件说明

### 配置文件
1. settings.py
   - 项目的核心配置文件
   - 包含数据库配置、中间件配置、日志配置等
   - 定义了项目的基本设置（DEBUG、时区、语言等）
   - 配置静态文件和媒体文件的处理

2. urls.py
   - URL路由配置文件
   - 定义了URL模式和对应的视图函数
   - 处理所有的HTTP请求路由

### 核心功能文件
1. middleware.py
   - 包含自定义中间件类
   - 处理请求/响应的日志记录
   - 性能监控和安全检查
   - 用户行为跟踪

2. models.py
   - 定义数据库模型
   - 包含所有的数据表结构
   - 定义模型之间的关系
   - 包含数据验证和业务逻辑

### 视图和模板
1. views/
   - error.py: 处理错误日志记录
   - auth.py: 处理认证相关功能
   - product.py: 处理商品相关功能
   - 其他业务视图文件

2. templates/
   - 存放HTML模板文件
   - 定义页面结构和样式
   - 包含基础模板和继承模板

### 工具和辅助文件
1. utils/
   - dependency_logger.py: 依赖包版本记录
   - env_logger.py: 环境信息记录
   - cache_logger.py: 缓存操作记录
   - api_logger.py: API调用记录
   - task_logger.py: 定时任务记录

2. management/commands/
   - log_system_status.py: 系统状态监控命令
   - 其他自定义管理命令

### 日志文件
1. logs/debug.log
   - 记录所有系统日志
   - 包含请求日志、错误日志
   - 性能监控数据
   - 安全警告信息

### 静态文件
1. static/
   - js/: JavaScript文件
   - css/: 样式文件
   - images/: 图片资源
   - error-handler.js: 前端错误处理

### 项目管理文件
1. requirements.txt
   - 列出所有Python依赖包
   - 包含具体的版本号
   - 用于环境复制和部署

2. manage.py
   - Django项目管理脚本
   - 提供各种管理命令
   - 用于数据库操作、运行服务器等