from settings import settings
import discord
# import * - es una forma rápida de importar todos los archivos de la biblioteca
from bot_logic import *
import random
from discord.ext import commands


# Configuración del bot de Discord
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Diccionario para almacenar datos financieros
finances = {}

# Función para añadir usuario
def add_user(user_id):
    if user_id not in finances:
        finances[user_id] = {
            'income': [],
            'expenses': []
        }

# Comando para añadir ingresos
@bot.command()
async def welcome(ctx):
    # Mensaje de bienvenida
    welcome_message = (
        "¡Bienvenido al servidor!\n"
        "Aquí están los comandos disponibles:\n"
    )

    
    await ctx.send(welcome_message)

    




bot.run(settings["TOKEN"])

# This example requires the 'members' and 'message_content' privileged intents to function.




bot.run(settings["TOKEN"])

# This example requires the 'members' and 'message_content' privileged intents to function.
