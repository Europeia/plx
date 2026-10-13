import os

from bot import Bot
from config import Config
from models import Dispatch, Telegram
from roles import Roles


def main() -> None:
    config = Config.from_yaml(os.getenv("PLX_CONFIG_FILE"))

    roles = Roles.from_json(config.roles_path)

    dispatch_template = Dispatch.from_file(config.dispatch_template_path)
    telegram_template = Telegram.from_file(config.telegram_template_path)

    bot = Bot(
        dispatch_template=dispatch_template,
        telegram_template=telegram_template,
        roles=roles,
    )

    bot.run(config.token)
