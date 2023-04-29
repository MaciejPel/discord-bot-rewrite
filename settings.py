import discord, youtube_dl, asyncio, validators

#ffmpeg
ffmpeg_options = {
    'options': '-vn -ss 0'
}

#ytdl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'files/%(id)s.mp3',
    # 'restrictfilenames': True,
    'noplaylist': True,
    # 'nocheckcertificate': True,
    # 'ignoreerrors': False,
    # 'logtostderr': False,
    'quiet': True,
    # 'no_warnings': True,
    'default_search': 'auto',
    # 'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def search(cls, arg):
        if validators.url(arg):
            data = ytdl.extract_info(arg, download=False)
            return data['title']
        else:
            data = ytdl.extract_info(f'"ytsearch:{arg}"', download=False)
            return data['entries'][0]['title']
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), data['duration'], data['id']+'.mp3'
    @classmethod
    async def from_search(cls, arg, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f'"ytsearch:{arg}"', download=not stream))
        print(data)
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), data['duration'], data['id']+'.mp3'
