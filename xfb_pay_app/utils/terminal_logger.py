import sys
import logging
from datetime import datetime

logger = logging.getLogger('xfb_pay_app')

class TerminalLogger:
    """终端输出记录器"""
    def __init__(self, log_file='logs/debug.log'):
        self.terminal = sys.stdout
        self.log_file = log_file
        
    def write(self, message):
        if message.strip():  # 只记录非空消息
            # 输出到终端
            self.terminal.write(message)
            # 记录到日志
            if message.strip():
                logger.info(f"终端输出: {message.strip()}")
        
    def flush(self):
        self.terminal.flush()

class TerminalErrorLogger:
    """终端错误输出记录器"""
    def __init__(self, log_file='logs/debug.log'):
        self.terminal = sys.stderr
        self.log_file = log_file
        
    def write(self, message):
        if message.strip():  # 只记录非空消息
            # 输出到终端
            self.terminal.write(message)
            # 记录到日志
            if message.strip():
                logger.error(f"终端错误: {message.strip()}")
        
    def flush(self):
        self.terminal.flush()

def setup_terminal_logging():
    """设置终端日志记录"""
    sys.stdout = TerminalLogger()
    sys.stderr = TerminalErrorLogger() 