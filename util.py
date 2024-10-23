import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def strip_embracing_quotes(text: str):
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text


def current_time():
    return datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %z')


def current_date():
    return datetime.now().astimezone().strftime('%Y-%m-%d')

def current_first_date_week():
    # Get the current date
    today = datetime.today()
    
    # Calculate the start of the week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    return start_of_week.date()

def ensure_dir(file: str):
    directory = os.path.abspath(os.path.dirname(file))
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_text(file: str, text: str):
    ensure_dir(file)
    with open(file, 'a') as f:
        f.write(text)
        f.write("\n")


if __name__ == "__main__":
    logger.info('hello world')
