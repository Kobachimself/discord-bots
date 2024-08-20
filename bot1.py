import discord
from discord import app_commands
from discord.ext import commands
import os

# Use double backslashes `\\` or raw string `r` to avoid escape sequences issues
os.environ['SSL_CERT_FILE'] = r'C:\Users\horisont1\Desktop\coding\cacert.pem'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Constants
PREFIX_ROLE_ID = 1268321134139412665  # Replace with the correct role ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Snowy Lite"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="setprefix", description="Set a prefix for a role")
@app_commands.describe(role="The role to set the prefix for", prefix="The prefix to set")
async def setprefix(interaction: discord.Interaction, role: discord.Role, prefix: str):
    guild = interaction.guild
    for member in guild.members:
        if role in member.roles:
            nickname = f"{prefix} | {member.display_name}"
            await member.edit(nick=nickname)
    await interaction.response.send_message(f"The prefix '{prefix}' has been set for all members with the role {role.mention}.")

@bot.tree.command(name="removeprefix", description="Remove a prefix from a role")
@app_commands.describe(role="The role to remove the prefix from")
async def removeprefix(interaction: discord.Interaction, role: discord.Role):
    guild = interaction.guild
    for member in guild.members:
        if role in member.roles and member.nick and member.nick.startswith(f"{role.name} |"):
            await member.edit(nick=None)
    await interaction.response.send_message(f"The prefix has been removed for all members with the role {role.mention}.")

bot.run('YOUR_BOT_TOKEN')
