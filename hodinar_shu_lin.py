import discord
from discord.ext import commands as cmds
from discord.ext import tasks
import asyncio
import tinytag
import datetime
done = False
intents = discord.Intents.default()
intents.message_content = True
client = cmds.Bot(
    command_prefix=cmds.when_mentioned_or("!"),
    description='Relatively simple music bot example',
    intents=intents,
)
def get_song_duration(audio_file):
    tag = tinytag.TinyTag.get(audio_file)
    return tag.duration
audio_file = 'bigben.mp3'  
duration_seconds = get_song_duration(audio_file)

class TheTasker(cmds.Cog):
    def __init__(self, bot, ctx):
        self.bot = bot 
        self.ctx = ctx 

    def hodinar_stop(self):
        self.zvonik.cancel()

    def hodinar_start(self):
        self.zvonik.start()

    @tasks.loop(seconds=15.0)
    async def zvonik(self):
        global done
        print("My task is running!")
        ctx = self.ctx
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        voice_channel_id = 1245691357931114551  
        voice_channel = client.get_channel(voice_channel_id)
        times = 0
        if minute == 0 and done == False:
            done = True
            if hour > 12:
                times = hour - 12
            else:
                times = hour
            voice_client = await voice_channel.connect()
            if ctx.voice_client:
                print(f"Connected to {voice_channel.name}")
                for _ in range(times):  
                    source = discord.FFmpegPCMAudio(executable='C:\\ffmpeg\\bin\\ffmpeg.exe', source='bigben.mp3',)
                    voice_client.play(source)
                    await asyncio.sleep(duration_seconds + 0.5)
                    voice_client.stop()
                await ctx.voice_client.disconnect()
                print(f"Disconnected from {voice_channel.name}")
        if minute != 0 and done:
            done = False
@client.event
async def on_ready():
    global tasks
    print(f'We have logged in as {client.user}')
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!
    channel = client.get_channel(1245691357931114550)  
    ctx = await client.get_context(await channel.send('Status: Ready'))
    tasks = TheTasker(client, ctx)
    tasks.hodinar_start()
    
client.add_cog(client)
client.run('MTI4NzExNzY2NTM5NTE0NjgxNA.G5PLVR.jnZaZgGvQtfVsmQwo6Z9r042vuN88yEjKV6JLA')