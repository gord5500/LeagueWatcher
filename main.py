import os

import discord
import sched, time
import imagecreator
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from leagueapi import LeagueApi


class LolWatcher(discord.Client):
    api = None
    champions = {}
    _names = {"fionnodo", "ron swanson", "santeniett", "single mums"}

    async def on_ready(self):

        print("Logged in as {}".format(self.user))

        self.api = LeagueApi()
        self.champions = self.api.get_champions()
        self.check_in_game.start()

    @tasks.loop(minutes=1)
    async def check_in_game(self):

        for name in self._names:
            account_id, name, encrypted_id, puuid = self.api.summoner_by_name("euw1", name)
            status_code, match_info = self.api.match_by_id("euw1", encrypted_id)

            if status_code == 200:
                print("{} is ingame!".format(name))
                img = imagecreator.create(match_info, self.champions)
                img.save("pic.jpg")
                channel = client.get_guild(801880864921092118).get_channel(939296773934030900)
                await channel.send(file=discord.File("pic.jpg"))
                self.api.insert_match("{}".format(match_info["gameId"]))
            else:
                print("{} is not ingame.".format(name))


client = LolWatcher(intents=discord.Intents.all())
client.run(os.environ.get("DISCORD_TOKEN"))
