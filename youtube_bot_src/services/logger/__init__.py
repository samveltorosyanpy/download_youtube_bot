from youtube_bot_src.services.logger.LoggerClass import Logger
from datetime import datetime as dt

black = '\x1b[38;5;0m'
white = '\x1b[38;5;15m'
green = '\x1b[38;5;40m'
purple = '\x1b[38;5;93m'
pink = '\x1b[38;5;206m'
orange = '\x1b[38;5;202m'
gray = '\x1b[38;5;242m'
light_blue = '\x1b[38;5;75m'
cyan = '\x1b[38;5;87m'
magenta = '\x1b[38;5;201m'
reset = '\x1b[0m'

log_dir = f"src/services/logger/logs/{dt.now().strftime('%Y-%m-%d')}"
file_name = f"{log_dir}/{dt.now().strftime('%Y-%m-%dT%H:%M:%S')}.log"

logger_redis = Logger(name='REDIS', log_file=file_name, log_dir=log_dir, color=light_blue)
logger_maria = Logger(name='MARIA', log_file=file_name, log_dir=log_dir, color=magenta)
logger_bot = Logger(name='BOT', log_file=file_name, log_dir=log_dir, color=cyan)