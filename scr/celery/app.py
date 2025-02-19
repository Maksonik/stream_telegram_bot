from celery import Celery
from dotenv import load_dotenv

from scr.celery.celeryconfig import Config

load_dotenv()

app = Celery("tasks")
app.config_from_object(Config)

if __name__ == '__main__':
    app.start()

