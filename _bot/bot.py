import asyncio
import os

import discord
import discord.app_commands
from discord import app_commands
from discord.ext import commands, tasks

from _services.alert import alert, formatList


class DiscordBot():
    def __init__(self):
        self.token = os.environ.get("TOKEN")
        self.channel_id = int(os.environ.get("CHANNEL_ID")) if os.environ.get("CHANNEL_ID") else None
        self.bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

        # register event handlers
        self.bot.event(self.on_ready)

        # register commands
        self.register_commands()

    async def on_ready(self):
        channel = self.bot.get_channel(self.channel_id)
        await channel.send("Bot has successfully started!")

        try:
            synced_commands = await self.bot.tree.sync()
            print(f"Synced {len(synced_commands)} commands")
        except Exception as e:
            print("Error while syncing application commands", e)

    def register_commands(self):
        self.cmdStock()

    def run(self):
        self.bot.run(self.token)

    def cmdStock(self):
        @self.bot.tree.command(name="stock_predict")
        @app_commands.describe(
            t1_closetoclose="_t-1_closetoclose (with comma)",
            closevalreached="bool_closevalreached"
        )
        async def register(interaction: discord.Interaction,
                           t1_closetoclose: float | None,
                           closevalreached: bool | None):

            if t1_closetoclose is None or closevalreached is None:

                embed = discord.Embed(
                    title="❌ Error",
                    description="'t1_closeToClose' or 'closeValReached' missing",
                    color=0xFF0000)

                await interaction.response.send_message(embed=embed)
                return

            if t1_closetoclose and closevalreached:
                dateStr, strings = await asyncio.wait_for(alert(t1_closetoclose, closevalreached), 20)

                if not strings:
                    desc = "No alerts"
                    color = 0xFF0000
                else:
                    desc = formatList(strings)
                    color = 0x33CC33

                embed = discord.Embed(
                    title=dateStr,
                    description=desc,
                    color=color)

                await interaction.response.send_message(embed=embed)
                return