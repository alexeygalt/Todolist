from django.core.management import BaseCommand

from bot.tg import tg_client
from bot.tg.bot import TgBot


class Command(BaseCommand):
    help = 'Команда для запуска telegram бота'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = tg_client

    def handle(self, *args, **options):
        tg_bot = TgBot(tg_client=self.tg_client)
        tg_bot.run()
