from importlib.metadata import distributions
import logging

logger = logging.getLogger('xfb_pay_app')

def log_dependencies():
    """记录已安装的依赖包版本"""
    installed_packages = [
        f"{dist.metadata['Name']}=={dist.version}"
        for dist in distributions()
    ]
    
    logger.info("依赖包信息 - " + " | ".join(installed_packages)) 