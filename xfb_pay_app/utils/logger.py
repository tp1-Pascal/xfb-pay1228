import logging
import sys

logger = logging.getLogger('xfb_pay_app')

def log_command_output():
    """记录命令行输出到日志文件"""
    class StreamToLogger:
        def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            pass

    # 重定向标准输出和错误输出到日志
    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

# 在程序启动时调用
log_command_output() 