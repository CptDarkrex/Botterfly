from __future__ import annotations

from .. import Plugin
from core import Bot, Embed

from discord import Interaction, app_commands, FFmpegPCMAudio, Member

from youtube_dl import YoutubeDL

#
class Music(Plugin):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, interaction: Interaction):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # in case we fail to connect
                if self.vc is None:
                    await interaction.response.send_message("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS, executable="C:/ffmpeg/bin"), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @app_commands.command(name="play", description="Plays a selected song from youtube")
    async def play(self, interaction: Interaction, prompt: str, member: Member):
        query = " ".join(prompt)

        voice_channel = member.voice.channel
        if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await interaction.response.send_message("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await interaction.response.send_message(
                    "Could not download the song. Incorrect format try another keyword."
                    " This could be due to playlist or a livestream format.")
            else:
                await interaction.response.send_message("Song added to the queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing is False:
                    await self.play_music(interaction)

    @app_commands.command(name="pause", description="Pauses the current song being played")
    async def pause(self, interaction: Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @app_commands.command(name="resume", description="Resumes playing with the discord bot")
    async def resume(self, interaction: Interaction):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @app_commands.command(name="skip", description="Skips the current song being played")
    async def skip(self, interaction: Interaction):
        if self.vc is not None and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.play_music(interaction)

    @app_commands.command(name="queue", description="Displays the current songs in queue")
    async def queue(self, interaction: Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await interaction.response.send_message(retval)
        else:
            await interaction.response.send_message("No music in queue")

    @app_commands.command(name="clear_queue", description="Stops the music and clears the queue")
    async def clear(self, interaction: Interaction):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await interaction.response.send_message("Music queue cleared")

    @app_commands.command(name="leave", description="Kick the bot from VC")
    async def dc(self, interaction: Interaction):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()


async def setup(bot: Bot) -> None:
    await bot.add_cog(Music(bot))
