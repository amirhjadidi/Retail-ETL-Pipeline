import inspect
import logging
import sys
from pathlib import Path
from sys import path


def get_logger(name=None, level=logging.INFO):
    # frame = sys._getframe(1)
    # name = Path(frame.f_code.co_filename).stem
    if name is None:
        name = __name__
    logger = logging.getLogger(name)

    if not logger.handlers:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        file_handler = logging.FileHandler(log_dir / f'{name}.log')
        # file_handler = logging.FileHandler(log_dir / 'log.log')
        file_handler.setLevel(level)

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(level)
    return logger
