import discord
from settings import settings
from discord.ext import commands
import random, requests, aiohttp, os
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Command: Welcome Message
@bot.command()
async def welcome(ctx):
    # Welcome message with game instructions
    welcome_message = (
        "¡Bienvenido al servidor!\n"
        "Aquí están los comandos disponibles:\n"
        "1. `!guess`: Juega un juego de adivinanza de números.\n"
        "2. `!rps`: Juega piedra, papel o tijera.\n"
        "3. `!dice`: Lanza un dado y mira el resultado.\n"
    )
    await ctx.send(welcome_message)

# Number Guessing Game
@bot.command()
async def guess(ctx):
    number = random.randint(1, 10)

    def check(m):
        return m.author == ctx.author and m.content.isdigit()

    await ctx.send("Adivina un número entre 1 y 10:")

    try:
        guess = await bot.wait_for('message', check=check, timeout=15.0)
        guess = int(guess.content)

        if guess == number:
            await ctx.send(f"¡Correcto! El número era {number}.")
        else:
            await ctx.send(f"¡Incorrecto! El número era {number}.")
    except:
        await ctx.send(f"¡No adivinaste a tiempo! El número era {number}.")

# Rock-Paper-Scissors 
@bot.command()
async def rps(ctx, choice: str):
    options = ["piedra", "papel", "tijera"]
    bot_choice = random.choice(options)

    valid_choices = ["piedra", "Piedra", "PAPEL", "papel", "Tijera", "tijera"]

    if choice not in valid_choices:
        await ctx.send("Por favor, elige entre `piedra`, `papel` o `tijera`.")
        return

    if choice in ["Piedra", "piedra"]:
        user_choice = "piedra"
    elif choice in ["Papel", "papel", "PAPEL"]:
        user_choice = "papel"
    elif choice in ["Tijera", "tijera"]:
        user_choice = "tijera"
    else:
        user_choice = ""

    if user_choice == bot_choice:
        result = "¡Es un empate!"
    elif (user_choice == "piedra" and bot_choice == "tijera") or \
         (user_choice == "papel" and bot_choice == "piedra") or \
         (user_choice == "tijera" and bot_choice == "papel"):
        result = "¡Ganaste!"
    else:
        result = "¡Perdiste!"

    await ctx.send(f"Tú elegiste **{choice}**, y yo elegí **{bot_choice}**. {result}")

# Mini-Game 3: Dice Roll
@bot.command()
async def dice(ctx):
    dice_roll = random.randint(1, 6)
    await ctx.send(f"¡Tiraste un dado y salió {dice_roll}!")




@bot.command()
async def poke(ctx,arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/"+ pokemon)
        if result.text == "Not Found":
            await ctx.send("Pokemon no encontrado")
        else:
            image_url = result.json()["sprites"]["front_default"]
            print(image_url)
            await ctx.send(image_url)
    except Exception as e:
        print("Error:", e)
@poke.error
async def error_type(ctx,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("Tienes que darme un pokemon")

@bot.command()
async def check(ctx, link=None):
    if ctx.message.attachments:  # Manejo de archivos adjuntos
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{file_name}")
            await ctx.send(f"Guardé la imagen en ./{file_name}")
    elif link:  # Manejo de enlaces proporcionados como argumento
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link) as response:
                    if response.status == 200:
                        content_disposition = response.headers.get("Content-Disposition", "")
                        file_name = (
                            content_disposition.split("filename=")[-1].strip('"')
                            if "filename=" in content_disposition
                            else os.path.basename(link)
                        )
                        file_path = f"./{file_name}"
                        with open(file_path, "wb") as f:
                            f.write(await response.read())
                        await ctx.send(f"Guardé el archivo del enlace en {file_path}")
                    else:
                        await ctx.send(f"No se pudo descargar el archivo. Estado HTTP: {response.status}")
            except Exception as e:
                await ctx.send(f"Hubo un error al descargar el archivo: {e}")
    else:
        await ctx.send("Por favor, sube una imagen o proporciona un enlace.")

# Run the bot
bot.run(settings["TOKEN"])




bot.run(settings["TOKEN"])

# This example requires the 'members' and 'message_content' privileged intents to function.
