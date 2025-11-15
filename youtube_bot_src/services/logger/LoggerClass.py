import logging
import os


class Logger:
    def __init__(self, name: str, log_file: str = None, log_dir: str = None, color: str = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(color + '[%(asctime)s] %(name)s: %(levelname)s %(message)s' + "\x1b[0m")

        if log_file:
            if os.path.exists(log_dir) is False:
                os.makedirs(log_dir)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str, user_id: int = '') -> None:
        self.logger.debug(f"[user id: {user_id}] {message}")

    def info(self, message: str, user_id: int = '') -> None:
        self.logger.info(f"[user id: {user_id}] {message}")

    def warning(self, message: str, user_id: int = '') -> None:
        self.logger.warning(f"[user id: {user_id}] {message}")

    def error(self, message: str, user_id: int = '') -> None:
        self.logger.error(f"[user id: {user_id}] {message}")

    def critical(self, message: str, user_id: int = '') -> None:
        self.logger.critical(f"[user id: {user_id}] {message}")
