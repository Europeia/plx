import discord
from discord.ext import commands

from models import Dispatch, Telegram
from roles import Roles


class Bot(commands.Bot):
    def __init__(
        self, dispatch_template: Dispatch, telegram_template: Telegram, roles: Roles
    ):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
        self._dispatch_template = dispatch_template
        self._telegram_template = telegram_template
        self.roles = roles

    async def setup_hook(self):
        default_cogs = ["base", "waa"]

        for cog in default_cogs:
            await self.load_extension(f"cogs.{cog}")
            print("loaded cog")

    @property
    def dispatch_template(self):
        return self._dispatch_template

    @property
    def telegram_template(self):
        return self._telegram_template
