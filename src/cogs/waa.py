import io
import re

import discord
from discord import app_commands
from discord.ext import commands

import models
from bot import Bot
from models import Dispatch, Telegram

proposal_name_re = re.compile(
    r"^\[(ga|sc)\] ?\[(for|against|abstain|no recommendation)\] ?([a-z: ]*)$",
    flags=re.IGNORECASE,
)


class IfvDispatchModal(discord.ui.Modal, title="Format IFV Dispatch"):
    def __init__(self, bot: Bot, dispatch_template: Dispatch):
        super().__init__(timeout=None)
        self._bot = bot
        self._dispatch_template = dispatch_template

    proposal_name = discord.ui.Label(
        text="Proposal Name",
        component=discord.ui.TextInput(
            style=discord.TextStyle.short,
            placeholder="[GA/SC] [FOR/AGAINST/ABSTAIN/NO RECOMMENDATION] PROPOSAL NAME",
            required=True,
        ),
    )

    forum_thread_url = discord.ui.Label(
        text="Forum Thread URL",
        component=discord.ui.TextInput(style=discord.TextStyle.short, required=True),
    )

    proposal_overview = discord.ui.Label(
        text="Proposal Overview",
        component=discord.ui.TextInput(style=discord.TextStyle.long, required=True),
    )

    ministry_analysis = discord.ui.Label(
        text="Ministry Analysis",
        component=discord.ui.TextInput(style=discord.TextStyle.long, required=True),
    )

    ifv_author = discord.ui.Label(
        text="IFV Author",
        component=discord.ui.TextInput(style=discord.TextStyle.short, required=True),
    )

    async def on_submit(self, interaction: discord.Interaction):
        assert isinstance(self.proposal_name.component, discord.ui.TextInput)
        assert isinstance(self.forum_thread_url.component, discord.ui.TextInput)
        assert isinstance(self.proposal_overview.component, discord.ui.TextInput)
        assert isinstance(self.ministry_analysis.component, discord.ui.TextInput)
        assert isinstance(self.ifv_author.component, discord.ui.TextInput)

        proposal_name = self.proposal_name.component.value
        forum_thread_url = self.forum_thread_url.component.value
        proposal_overview = self.proposal_overview.component.value
        ministry_analysis = self.ministry_analysis.component.value
        ifv_author = self.ifv_author.component.value

        captures = proposal_name_re.search(proposal_name)

        if not captures:
            raise ValueError("Proposal Name Doesn't Match Expected Format")

        chamber = captures[1].lower()
        position = captures[2].lower()
        proposal_name = captures[3]

        if not models.is_chamber(chamber):
            raise ValueError("Chamber should be GA or SC")

        if not models.is_position(position):
            raise ValueError(
                "Position should be FOR, AGAINST, ABSTAIN, or NO RECOMMENDATION"
            )

        formatted_dispatch = self._dispatch_template.format(
            proposal_name=proposal_name,
            chamber=chamber,
            forum_thread_url=forum_thread_url,
            position=position,
            proposal_overview=proposal_overview,
            ministry_analysis=ministry_analysis,
            ifv_author=ifv_author,
            mowaa_nation=self._bot.roles.mowaa_nation,
            mowaa_forum=self._bot.roles.mowaa_forum,
            europeia_del=self._bot.roles.europeia_del,
            estalcia_del=self._bot.roles.estalcia_del,
        )

        await interaction.response.send_message(
            file=discord.File(
                fp=io.BytesIO(formatted_dispatch.encode("utf-8")),
                filename="ifv_dispatch.txt",
            )
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(error)


class IfvTelegramModal(discord.ui.Modal, title="Format IFV Telegram"):
    def __init__(self, bot: Bot, telegram_template: Telegram):
        super().__init__(timeout=None)
        self._bot = bot
        self._telegram_template = telegram_template

    proposal_name = discord.ui.Label(
        text="Proposal Name",
        component=discord.ui.TextInput(
            style=discord.TextStyle.short,
            placeholder="[GA/SC] [FOR/AGAINST/ABSTAIN/NO RECOMMENDATION] PROPOSAL NAME",
            required=True,
        ),
    )

    forum_thread_url = discord.ui.Label(
        text="Forum Thread URL",
        component=discord.ui.TextInput(style=discord.TextStyle.short, required=True),
    )

    ifv_dispatch_url = discord.ui.Label(
        text="IFV Dispatch URL",
        component=discord.ui.TextInput(style=discord.TextStyle.short, required=True),
    )

    async def on_submit(self, interaction: discord.Interaction):
        assert isinstance(self.proposal_name.component, discord.ui.TextInput)
        assert isinstance(self.forum_thread_url.component, discord.ui.TextInput)
        assert isinstance(self.ifv_dispatch_url.component, discord.ui.TextInput)

        proposal_name = self.proposal_name.component.value
        forum_thread_url = self.forum_thread_url.component.value
        ifv_dispatch_url = self.ifv_dispatch_url.component.value

        captures = proposal_name_re.search(proposal_name)

        if not captures:
            raise ValueError("Proposal Name Doesn't Match Expected Format")

        chamber = captures[1].lower()
        position = captures[2].lower()
        proposal_name = captures[3]

        print(chamber)
        print(position)
        print(proposal_name)

        if not models.is_chamber(chamber):
            raise ValueError("Chamber should be GA or SC")

        if not models.is_position(position):
            raise ValueError(
                "Position should be FOR, AGAINST, ABSTAIN, or NO RECOMMENDATION"
            )

        formatted_telegram = self._telegram_template.format(
            chamber=chamber,
            proposal_name=proposal_name,
            forum_thread_url=forum_thread_url,
            position=position,
            ifv_dispatch_url=ifv_dispatch_url,
            mowaa_nation=self._bot.roles.mowaa_nation,
            mowaa_forum=self._bot.roles.mowaa_forum,
            europeia_del=self._bot.roles.europeia_del,
            estalcia_del=self._bot.roles.estalcia_del,
        )

        await interaction.response.send_message(
            file=discord.File(
                fp=io.BytesIO(formatted_telegram.encode("utf-8")),
                filename="ifv_telegram.txt",
            )
        )


class WaaCog(commands.Cog):
    def __init__(self, bot: Bot):
        self._bot = bot

    ifv_format_command_group = app_commands.Group(
        name="format", description="commands for IFVs", guild_only=True
    )

    @ifv_format_command_group.command(
        name="dispatch", description="format an IFV dispatch"
    )
    # @app_commands.guild_only()
    async def format_ifv_dispatch(self, interaction: discord.Interaction):
        modal = IfvDispatchModal(self._bot, self._bot.dispatch_template)

        await interaction.response.send_modal(modal)

    @ifv_format_command_group.command(
        name="telegram", description="format an IFV telegram"
    )
    # @app_commands.guild_only()
    async def format_ifv_telegram(self, interaction: discord.Interaction):
        modal = IfvTelegramModal(self._bot, self._bot.telegram_template)

        await interaction.response.send_modal(modal)

    setting_command_group = app_commands.Group(
        name="set", description="configure settings", guild_only=True
    )

    @setting_command_group.command(
        name="mowaa_forum", description="set the MoWAA's forum username"
    )
    # @app_commands.guild_only()
    async def set_mowaa_forum_username(
        self, interaction: discord.Interaction, username: str
    ):
        self._bot.roles.mowaa_forum = username

        await interaction.response.send_message("setting updated")

    @setting_command_group.command(
        name="mowaa_nation", description="set the MoWAA's nation name"
    )
    # @app_commands.guild_only()
    async def set_mowaa_nation_name(
        self, interaction: discord.Interaction, nation: str
    ):
        self._bot.roles.mowaa_nation = nation

        await interaction.response.send_message("setting updated")

    @setting_command_group.command(
        name="euro_del", description="set the Europeian delegate's nation name"
    )
    # @app_commands.guild_only()
    async def set_euro_del_nation_name(
        self, interaction: discord.Interaction, nation: str
    ):
        self._bot.roles.europeia_del = nation

        await interaction.response.send_message("setting updated")

    @setting_command_group.command(
        name="estalcia_del", description="set the Estalcian delegate's nation name"
    )
    # @app_commands.guild_only()
    async def set_estalcia_del_nation_name(
        self, interaction: discord.Interaction, nation: str
    ):
        self._bot.roles.estalcia_del = nation

        await interaction.response.send_message("setting updated")


async def setup(bot: Bot):
    await bot.add_cog(WaaCog(bot))
