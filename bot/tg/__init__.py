import os

from .client import TgClient
from .dc import get_updates_schema, send_message_schema

tg_client = TgClient(os.environ.get('TG_TOKEN'))

__all__ = ('get_updates_schema', 'send_message_schema', 'tg_client', 'TgClient')
