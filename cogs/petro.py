from logging import error
import requests
import discord
from discord.ext import commands
from pydactyl import PterodactylClient
import humanfriendly
from humanfriendly import format_size, format_timespan
from utils.config import pterodactylapikey, pterodactyldomain
from discord.commands import slash_command, option

# NOTES:
# ServerIdentification SHOULD be the Name of the Server you will be identifying it as
# server id SHOULD be the ID of the server.

api = PterodactylClient(pterodactyldomain, pterodactylapikey)
AUTHORIZED_USERS = [USER ID, USER ID, USER ID, USER ID, USER ID] # This is for in the event someone runs the command and are not authorized, they will not see the servers listed.
SERVER_ID_LIST = ["ServerIdentification","ServerIdentification","ServerIdentification", "ServerIdentification", "ServerIdentification", "ServerIdentification","ServerIdentification","ServerIdentification","ServerIdentification","ServerIdentification"]


async def authchecker(ctx: discord.AutocompleteContext):
    """
    Returns a list of the Server Identification from the SERVER_ID_LIST list.
    In this example, we've added logic to only display any results in the
    returned list if the user's ID exists in the BASIC_ALLOWED list.
    This is to demonstrate passing a callback in the discord.utils.basic_autocomplete function.
    """

    return [id for id in SERVER_ID_LIST if ctx.interaction.user.id in AUTHORIZED_USERS]

class ServerError:
    """There was a server error during a power action"""
    pass

class ptrodactylcontrols(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   # THE SERVER IDENTIFICATION MUST BE SAME AS THE ONE PROVIDED ABOVE. SPACES ARE NOT ALLOWED DUE TO HOW IT WORKS
    def Convert_Friendly_Name_to_ID(self, server_id):
        """A common function to use to convert custom identifiers to server IDs"""
        if server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"   
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"        
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"   
        elif server_id.lower() == "Name of Server":     
            server_id = "ServerIdentification"   
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"  
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"
        elif server_id.lower() == "Name of Server":
            server_id = "ServerIdentification"    
        return server_id

    @slash_command(description="hello")
    @option(name="server",autocomplete=discord.utils.basic_autocomplete(authchecker))
    @option(name="action", choices=["on", "start", "off", "stop","restart", "status", "sendcommand", "kill"])
    @option(name="command", description="The command to run on the server", required=False)
    async def server(self, ctx: commands.Context, server: str, action: str, command:str):
        """
        Power commands for servers.
        """
        server_id = self.Convert_Friendly_Name_to_ID(server)
        if action.lower() == "on" or action.lower() == "start":
            try:
                api.client.servers.send_power_action(server_id, "start")
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:yes:1013111685172707421> Starting the server - `{server} [{server_id}]`"
                        )
                    )
            except:
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:no:1013111586082259104> Something went wrong while starting - `{server} [{server_id}]`"
                        )
                    )
        elif action.lower() == "off" or action.lower() == "stop":
            try:
                api.client.servers.send_power_action(server_id, "stop")
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:yes:1013111685172707421> Stopping the server - `{server} [{server_id}]`"
                    )
                )
            except:
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:no:1013111586082259104> Something went wrong while stopping the server - `{server}`".format(command)
                        )
                    )
        elif action.lower() == "restart":
            try:
                api.client.servers.send_power_action(server_id, "restart")
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:yes:1013111685172707421> Restarting the server - `{server} [{server_id}]`"
                        )
                    )
            except:
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:no:1013111586082259104> Something went wrong while restarting the server - `{server} [{server_id}]`".format(command)
                        )
                    )
        elif action.lower() == "sendcommand":
            if command == None:
                return await ctx.respond(
                    embed=discord.Embed(
                        description="<:no:1013111586082259104> Hey buddy, you need to specify a command to send",
                        color=0xB51818,
                    )
                )
            try:
                response = api.client.servers.send_console_command(server_id, command)
                if response.status_code == 204:
                    await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:yes:1013111685172707421> Sent command `{command}` to the server - `{server} [{server_id}]`"
                        )
                    )
                else:
                    pass
            except requests.exceptions.HTTPError:
                await ctx.respond(
                    embed=discord.Embed(
                        description="<:no:1013111586082259104> There was a server error while processing that console command, please try again later",
                        color=0xB51818,
                    )
                )
                raise ServerError  # type: ignore
        elif action.lower() == "status":
            try:
                response = api.client.servers.get_server_utilization(server_id, detail=True)
                if response["attributes"]["is_suspended"] == "True":
                    await ctx.respond(embed=discord.Embed(description="<:warning:1014535395658174484> The server is suspended, please contact the server provider to resolve this issue"))
                
                elif response["attributes"]["current_state"] == "running":
                    e = response["attributes"]["resources"]["uptime"] / 1000.0
                    h = humanfriendly.format_timespan(e)
                    memory = humanfriendly.format_size(
                        response["attributes"]["resources"]["memory_bytes"]
                    )
                    disk = humanfriendly.format_size(
                        response["attributes"]["resources"]["disk_bytes"]
                    )
                    upload = humanfriendly.format_size(
                        response["attributes"]["resources"]["network_rx_bytes"]
                    )
                    download = humanfriendly.format_size(
                        response["attributes"]["resources"]["network_tx_bytes"]
                    )
                    ramlimit = "unlimited"
                    disklimit = "unlimited"
                    # YOU WILL HAVE TO MANUALLY ADD THE LIMIT PROVIDED BY YOUR SERVER PROVIDER DUE TO PTERODACTYL LIMITATION(s).
                    # YOU MAY REMOVE THE DISK/RAM LIMIT(s) DOWN BELOW IF THERE IS NO LIMIT ON YOUR PTERODACTYL SERVER.
                    if server_id == "acffbc5b":
                        ramlimit = "6.14 GB"
                    embed = discord.Embed(
                        title="Server Details",
                        description=f"""
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
                    """,
                        color=0x57F287,
                    )
                    await ctx.respond(embed=embed)
                elif response["attributes"]["current_state"] == "offline":
                    embed = discord.Embed(
                        title="Server Details",
                        description=f"""
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
                    """,
                        color=0xED4245,
                    )
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=discord.Embed(description="<:warning:1014535395658174484> The server is either in the middle of a power action, or its not responding"))
            except requests.exceptions.HTTPError:
                await ctx.respond(embed=discord.Embed(description="<:warning:1014535395658174484> There was an error while looking up the server status, please try again later",color=0xB51818))
        elif action.lower() == "kill":
            try:
                api.client.servers.send_power_action(server_id, "kill")
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:yes:1013111685172707421> Killing the server - `{server} [{server_id}]`"
                        )
                    )
            except:
                await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:no:1013111586082259104> Something went wrong while killing the server - `{server} [{server_id}]`"
                        )
                    )
        else:
            await ctx.respond(
                        embed=discord.Embed(
                            description=f"<:no:1013111586082259104> **Invalid action**, please use `start`, `stop`, `restart`, `sendcommand`, `kill` or `status`"
                        )
                    )

    @commands.command()
    @commands.is_owner()
    async def start(self, ctx, server_id=None):
        if server_id == None:
            await ctx.send(
                embed=discord.Embed(
                    description="Hey buddy, you need to specify a server identifier or server id",
                    color=0xB51818,
                )
            )
            return
        else:
            # Use a common function cross commands to convert
            server_id = self.Convert_Friendly_Name_to_ID(server_id)
        try:
            response = api.client.servers.send_power_action(server_id, "start")
            if response.status_code == 204:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Starting the server {ctx.author.mention}, please wait while it starts!",
                        color=0x842899,
                    )
                )
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(
                embed=discord.Embed(
                    description="There was a server error while processing that power action, please try again later",
                    color=0xB51818,
                )
            )
            raise ServerError  # type: ignore

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx, server_id=None):
        if server_id == None:
            await ctx.send(
                embed=discord.Embed(
                    description="Hey buddy, you need to specify a server identifier or server id",
                    color=0xB51818,
                )
            )
            return
        else:
            # Use a common function cross commands to convert
            server_id = self.Convert_Friendly_Name_to_ID(server_id)
        try:
            response = api.client.servers.send_power_action(server_id, "stop")
            if response.status_code == 204:
                await ctx.send(
                    embed=discord.Embed(
                        description="Stopping the server, hope you had a great time!"
                    )
                )
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(
                embed=discord.Embed(
                    description="There was a server error while processing that power action, please try again later",
                    color=0xB51818,
                )
            )
            raise ServerError  # type: ignore

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx, server_id=None):
        if server_id == None:
            await ctx.send(
                embed=discord.Embed(
                    description="Hey buddy, you need to specify a server identifier or server id",
                    color=0xB51818,
                )
            )
            return
        else:
            # Use a common function cross commands to convert
            server_id = self.Convert_Friendly_Name_to_ID(server_id)
        try:
            response = api.client.servers.send_power_action(server_id, "restart")
            if response.status_code == 204:
                await ctx.send(
                    embed=discord.Embed(
                        description="Restarting the server, give it a minute!"
                    )
                )
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(
                embed=discord.Embed(
                    description="There was a server error while processing that power action, please try again later",
                    color=0xB51818,
                )
            )
            raise ServerError  # type: ignore

    @commands.command()
    @commands.is_owner()
    async def sendcommand(self, ctx, server_id=None, *, cmd=None):
        if server_id == None:
            await ctx.send(
                embed=discord.Embed(
                    description="Hey buddy, you need to specify a server identifier or server id",
                    color=0xB51818,
                )
            )
            return
        else:
            # Use a common function cross commands to convert
            server_id = self.Convert_Friendly_Name_to_ID(server_id)
        if cmd == None:
            return await ctx.send(
                embed=discord.Embed(
                    description="Hey buddy, you need to specify a command to send",
                    color=0xB51818,
                )
            )
        try:
            response = api.client.servers.send_console_command(server_id, cmd)
            if response.status_code == 204:
                await ctx.send(
                    embed=discord.Embed(
                        description="Sent command `{}` to the server".format(cmd)
                    )
                )
            else:
                pass
        except requests.exceptions.HTTPError:
            await ctx.send(
                embed=discord.Embed(
                    description="There was a server error while processing that console command, please try again later",
                    color=0xB51818,
                )
            )
            raise ServerError  # type: ignore

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, server_id=None):
        if server_id == None:
            await ctx.send(
                embed=discord.Embed(
                    description="Hey buddy, you need to specify a server identifier or server id",
                    color=0xB51818,
                )
            )
            return
        try:
            # Use a common function cross commands to convert
            server_id = self.Convert_Friendly_Name_to_ID(server_id)
        except:
            pass
        try:
            response = api.client.servers.get_server_utilization(server_id, detail=True)
            if response["attributes"]["is_suspended"] == "True":
                await ctx.send(
                    embed=discord.Embed(
                        description="The server is suspended, please contact the server provider to resolve this issue"
                    )
                )
            elif response["attributes"]["current_state"] == "running":
                e = response["attributes"]["resources"]["uptime"] / 1000.0
                h = humanfriendly.format_timespan(e)
                memory = humanfriendly.format_size(
                    response["attributes"]["resources"]["memory_bytes"]
                )
                disk = humanfriendly.format_size(
                    response["attributes"]["resources"]["disk_bytes"]
                )
                upload = humanfriendly.format_size(
                    response["attributes"]["resources"]["network_rx_bytes"]
                )
                download = humanfriendly.format_size(
                    response["attributes"]["resources"]["network_tx_bytes"]
                )
                ramlimit = "unlimited"
                disklimit = "unlimited"
                # YOU WILL HAVE TO MANUALLY ADD THE LIMIT PROVIDED BY YOUR SERVER PROVIDER DUE TO PTERODACTYL LIMITATION(s).
                # YOU MAY REMOVE THE DISK/RAM LIMIT(s) DOWN BELOW IF THERE IS NO LIMIT ON YOUR PTERODACTYL SERVER.
                if server_id == "acffbc5b":
                    ramlimit = "6.14 GB"
                embed = discord.Embed(
                    title="Server Details",
                    description=f"""
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
                """,
                    color=0x57F287,
                )
                await ctx.send(embed=embed)
            elif response["attributes"]["current_state"] == "offline":
                embed = discord.Embed(
                    title="Server Details",
                    description=f"""
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
                """,
                    color=0xED4245,
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description="The server is either in the middle of a power action, or its not responding"
                    )
                )
        except requests.exceptions.HTTPError:
            await ctx.send(
                embed=discord.Embed(
                    description="There was an error while looking up the server status, please try again later",
                    color=0xB51818,
                )
            )
            raise ServerError  # type: ignore


def setup(bot):
    bot.add_cog(ptrodactylcontrols(bot))
