from logging import error
import requests
import discord
from discord.ext import commands
from pydactyl import PterodactylClient
import humanfriendly
from humanfriendly import format_size, format_timespan
from utils.config import pterodactylapikey, pterodactyldomain


api = PterodactylClient(pterodactyldomain, pterodactylapikey)


class ServerError:
    """There was a server error during a power action"""
    pass


class pwtro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.is_owner()
    async def start(self, ctx, server_id=None):
        if server_id == None:
            return await ctx.send(embed=discord.Embed(description="Hey buddy, you need to specify a server identifier or server id",color=0xb51818)) 
        if server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"
        elif server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"   
        try:
            response = api.client.servers.send_power_action(server_id, 'start')
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description=f"Starting the server {ctx.author.mention}, please wait while it starts!",
                    color=0x842899
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(embed=discord.Embed(
            description='There was a server error while processing that power action, please try again later',
            color=0xb51818))
            raise ServerError

    
    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx, server_id=None):
        if server_id == None:
            return await ctx.send(embed=discord.Embed(description="Hey buddy, you need to specify a server identifier or server id",color=0xb51818)) 
        if server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"
        elif server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"    
        try:
            response = api.client.servers.send_power_action(server_id, 'stop')
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description="Stopping the server, hope you had a great time!"
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(embed=discord.Embed(
            description='There was a server error while processing that power action, please try again later',
            color=0xb51818))
            raise ServerError

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx, server_id=None):
        if server_id == None:
            return await ctx.send(embed=discord.Embed(description="Hey buddy, you need to specify a server identifier or server id",color=0xb51818))    
        if server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"
        elif server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"       
        try:
            response = api.client.servers.send_power_action(server_id, 'restart')
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description="Restarting the server, give it a minute!"
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(embed=discord.Embed(
            description='There was a server error while processing that power action, please try again later',
            color=0xb51818))
            raise ServerError

    @commands.command()
    @commands.is_owner()
    async def sendcommand(self, ctx, server_id=None,*, cmd=None):
        if server_id == None:
            return await ctx.send(embed=discord.Embed(description="Hey buddy, you need to specify a server identifier or server id",color=0xb51818))
        if cmd == None:
            return await ctx.send(embed=discord.Embed(description="Hey buddy, you need to specify a command to send",color=0xb51818))
        if server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"
        elif server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"       
        try:
            response = api.client.servers.send_console_command(server_id, cmd)
            if response.status_code == 204:
                await ctx.send(embed=discord.Embed(
                    description="Sent command `{}` to the server".format(cmd)
                ))
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(embed=discord.Embed(
            description='There was a server error while processing that console command, please try again later',
            color=0xb51818))
            raise ServerError

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, server_id=None):
        if server_id == None:
            return await ctx.send(embed=discord.Embed(description="Hey buddy, you need to specify a server identifier or server id",color=0xb51818))
        if server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"
        elif server_id.lower() == "any identifier":
            server_id = "YOUR SERVER ID"      
        try:
            response = api.client.servers.get_server_utilization(server_id, detail=True)
            if response['attributes']['is_suspended'] == 'True':
                await ctx.send(embed=discord.Embed(
                    description="The server is suspended, please contact the server provider to resolve this issue"
                ))
            elif response['attributes']['current_state'] == 'running':
                e = response['attributes']['resources']['uptime'] / 1000.0
                h = humanfriendly.format_timespan(e)
                memory = humanfriendly.format_size(response['attributes']['resources']['memory_bytes'])
                disk = humanfriendly.format_size(response['attributes']['resources']['disk_bytes'])
                upload = humanfriendly.format_size(response['attributes']['resources']['network_rx_bytes'])
                download = humanfriendly.format_size(response['attributes']['resources']['network_tx_bytes'])
                ramlimit = "unlimited" 
                disklimit = "unlimited"
                #YOU WILL HAVE TO MANUALLY ADD THE LIMIT PROVIDED BY YOUR SERVER PROVIDER DUE TO PTERODACTYL LIMITATION(s).
                #YOU MAY REMOVE THE DISK/RAM LIMIT(s) DOWN BELOW IF THERE IS NO LIMIT ON YOUR PTERODACTYL SERVER.
                if server_id == "any identifier":
                    ramlimit = "limit?" 
                    disklimit = "limit?"
                elif server_id == "any 2nd identifier":
                    ramlimit = "limit?" 
                    disklimit = "limit?"
                embed = discord.Embed(title="Server Details",description=
                f"""
                **• Status:** `💚 Running`
                **• SERVER ID:** `{server_id}`
                ==============================================
                __**SERVER UTILIZATION**__
                **• Memory:** `{memory}/{ramlimit}`
                **• CPU:** `{response['attributes']['resources']['cpu_absolute']}%`
                **• Disk:** `{disk}/{disklimit}`
                ==============================================
                __**SERVER NETWORK UTILIZATION**__
                **• Inbound:** `{download}`
                **• Outbound:** `{upload}`
                ==============================================
                __**SERVER UPTIME**__
                **• Uptime:** `{h}`
                """,color=0x57F287)
                await ctx.send(embed=embed)
            elif response['attributes']['current_state'] == 'offline':
                embed = discord.Embed(title="Server Details",description=
                f"""
                **• Status:** `💔 Offline`
                **• SERVER ID:** `{server_id}`
                ==============================================
                __**SERVER UTILIZATION**__
                **• Memory:** `OFFLINE`
                **• CPU:** `OFFLINE`
                **• Disk:** `OFFLINE`
                ==============================================
                __**SERVER NETWORK UTILIZATION**__
                **• Inbound:** `OFFLINE`
                **• Outbound:** `OFFLINE`
                ==============================================
                __**SERVER UPTIME**__
                **• Uptime:** `OFFLINE`
                """,color=0xED4245)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(
                    description='The server is either in the middle of a power action, or its not responding'
                ))
        except requests.exceptions.HTTPError:
            await ctx.send(embed=discord.Embed(
            description='There was an error while looking up the server status, please try again later',
            color=0xb51818))
            raise ServerError


def setup(bot):
    bot.add_cog(pwtro(bot))
