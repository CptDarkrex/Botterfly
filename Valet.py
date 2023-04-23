#   ===========================================================  #
#   ===== Project Valet                                   =====  #
#   ===== Bot for personal use, the zerotwo alternative   =====  #
#   ===== Created by Carlos Rodriguez                     =====  #
#   ===== Copyright reserved Lubris                       =====  #
#   ===========================================================  #

#   ===== Discord Setup =====   #
import discord
from discord import app_commands
from discord.ext import ipc, commands

#   ===== Pillow Setup =====   #
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

#   ===== MariaDB Dependencies =====   #
import mysql.connector as mariadb

#   ===== Music Function Dependencies ===== #
import youtube_dl
import asyncio
import os

#   ===== Maria DB =====    #
mariadb_connection = mariadb.connect(user='root', password='zqf3afr1GVQ9uae-cwe', host='10.20.10.35', port='3306', database='Valet')
create_cursor = mariadb_connection.cursor()#dictionary=True <--- can make the database into dictionary format

#   ===== Create Database ===== #
# create_cursor.execute("CREATE DATABASE Valet")

# create_cursor.execute("SHOW DATABASES")
# for x in create_cursor:
#     print(x)

  # ===== Create Tables =====   #
# create_cursor.execute("CREATE TABLE profile_card_users (usr_id BIGINT PRIMARY KEY, name VARCHAR(24), birth DATE, description VARCHAR(250), cus_img_url VARCHAR(9000))") #<-- CREATES THE PROFILE TABLE MAIN TABLE
# create_cursor.execute("CREATE TABLE svr_mod ()")


#   ===========================   #
#   ===== Profile backend =====   #
#   ===========================   #

#   ===== Profile Insert into Database ===== #
def profile_data(usr_id, name, birth, desc, img_id):
    sql_cd = "INSERT INTO profile_card_users (usr_id, name, birth, description, cus_img_url) VALUES (%s, %s, %s, %s, %s)"
    sql_values = (usr_id, name, birth, desc, img_id)
    create_cursor.execute(sql_cd, sql_values)
    mariadb_connection.commit()

#   ===== Profile Name Update =====   #
def profile_data_name(usr_id, name):
    sql_cd = "UPDATE profile_card_users SET name = %s WHERE usr_id = %s"
    sql_values = (name, usr_id)
    create_cursor.execute(sql_cd, sql_values)
    mariadb_connection.commit()

#   ===== Profile Birth Update =====   #
def profile_data_birth(usr_id, birth):
    sql_cd = "UPDATE profile_card_users SET birth = %s WHERE usr_id = %s"
    sql_values = (birth, usr_id)
    create_cursor.execute(sql_cd, sql_values)
    mariadb_connection.commit()

#   ===== Profile Description Update =====   #
def profile_data_desc(usr_id, desc):
    sql_cd = "UPDATE profile_card_users SET description = %s WHERE usr_id = %s"
    sql_values = (desc, usr_id)
    create_cursor.execute(sql_cd, sql_values)
    mariadb_connection.commit()

#   ===== Profile Profile Background Update =====   #
def profile_data_pbg(usr_id, pbg):
    sql_cd = "UPDATE profile_card_users SET cus_img_url = %s WHERE usr_id = %s"
    sql_values = (pbg, usr_id)
    create_cursor.execute(sql_cd, sql_values)
    mariadb_connection.commit()

print(create_cursor.rowcount)


#   ============================    #
#   ===== Profile Frontend =====    #
#   ============================    #

# ===== Profile Drawing Functions =====  #
def profile_create(usr):
    # creates a new image copy to work in
    if Path(f"{usr}.jpg").is_file() == False:
        my_image = Image.open("../images/yuu.jpg")
        my_image.save(f"completed_profiles/{usr}_template.jpg")

    user = (usr,)
    sql_statement = "SELECT * FROM profile_card_users WHERE usr_id = %s"
    create_cursor.execute(sql_statement, user)
    my_result = create_cursor.fetchall()
    my_tuple = my_result[0]
    name = my_tuple[1]
    birth = my_tuple[2]
    desc = my_tuple[3]

    profile_name(usr, name, f"completed_profiles/{usr}_template.jpg")
    # profile_birth(usr, birth, f"{usr}.jpg")
    profile_description_text(usr, desc, f"completed_profiles/{usr}_template2.jpg")

def profile_name(user, name, img_path):
    # my_image = Image.open(f"{user}.jpg")
    # if Path(f"{user}.jpg").is_file() == False:
    #     my_image = Image.open("images/yuu.jpg")
    # if Path(f"{user}.jpg").is_file() == True:
    #     my_image = Image.open(f"{user}.jpg")
    my_image = Image.open(img_path)

    title_font = ImageFont.truetype("fonts/IndieFlower-Regular.ttf", size=28)
    title_text = f"Name: {name}"
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((15, 15), title_text, (237, 230, 211), font=title_font)
    my_image.save(f"completed_profiles/{user}_template2.jpg")

def profile_birth(user, birth, img_path):
    # my_image = Image.open(f"{user}.jpg")
    # edit_user_image = ""
    # my_image = ""
    # if Path(f"{user}.jpg").is_file() == False:
    #     my_image = Image.open("images/yuu.jpg")
    # if Path(f"{user}.jpg").is_file() == True:
    #     my_image = Image.open(f"{user}.jpg")
    my_image = Image.open(img_path)

    title_font = ImageFont.truetype("fonts/IndieFlower-Regular.ttf", size=28)
    birth_text = birth
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((15,60), birth_text, (237, 230, 211), font=title_font)
    my_image.save(f"completed_profiles/{user}.jpg")

def profile_description_text(user, desc, img_path):
    # if Path(f"{user}.jpg").is_file() == False:
    #     my_image = Image.open("images/yuu.jpg")
    # if Path(f"{user}.jpg").is_file() == True:
    #     my_image = Image.open(f"{user}.jpg")
    my_image = Image.open(img_path)

    title_font = ImageFont.truetype("fonts/IndieFlower-Regular.ttf", size=28)
    title_text = f"Description: {desc}"
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((15, 50), title_text, (237, 230, 211), font=title_font)
    my_image.save(f"completed_profiles/{user}.jpg")

#  ===== Embed Template =====  #
embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                      description="This is an embed that will show how to build an embed and the different components",
                      color=0xFF5733, )
embed.set_image(url="https://c4.wallpaperflare.com/wallpaper/771/807/811/anime-anime-girls-zero-two-zero-two-darling-in-the-franxx-wallpaper-preview.jpg")
embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
embed.add_field(name="Field 2 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)

#   ===== Developement Variables =====  #
dev_server_id = 944147234562400256


#   ===== Set up =====  #
class aclient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synced = False #we use this so the bot doesn't sync commands more than once
        self.server = ipc.Server(self, secret_key="my_secret_key")

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced
            await tree.sync(guild = discord.Object(id=dev_server_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")





client = aclient(intents = discord.Intents.default())
tree = app_commands.CommandTree(client)

#   ==========================  #
#   ===== Slash Commands =====  #
#   ==========================  #

#   ===== Slash command templates =====  #
@tree.command(guild = discord.Object(id=dev_server_id), name = 'hi', description='testing') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = False)

#   =====================================   #
#   ===== Profile Command sequences =====   #
#   =====================================   #

@tree.command(guild = discord.Object(id=dev_server_id), name = 'embed', description='testing out the embed') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am working ! I was made with Discord.py!", ephemeral = False, embed=embed)

@tree.command(guild = discord.Object(id=dev_server_id), name = 'profile', description='A profile card of who you are accross all servers with this bot in it.') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    user = interaction.user.id
    profile_create(user)
    await interaction.response.send_message(ephemeral = False, file=discord.File(f"completed_profiles/{user}.jpg"))

@tree.command(guild = discord.Object(id=dev_server_id), name = 'create_profile', description='creates a profile card. Birth is in YY/MM/DD format. Paste a URL in img_id (optional)') #guild specific slash command
async def slash2(interaction: discord.Interaction, name:str, description:str, birth:int, img_id:str):
    user_id = interaction.user.id

    profile_data(user_id, name, description, birth, img_id)
    # profile_name(user_id, name)
    # profile_description_text(user_id, description)
    user_id = user_id
    # sql_statement = "SELECT usr_id FROM profile_card_users WHERE usr_id = %s"
    # create_cursor.execute(sql_statement, user_id[0])
    # usr_id = create_cursor.fetchall()

    # print(usr_id)

    # if user_id in usr_id:
    #     await interaction.response.send_message(f"Failed, you already have a profile! if you wish to update use the update commmand", ephemeral=False)
    # else:
    #     profile_data(user_id, name, birth, description, img_id)
    #     await interaction.response.send_message(f"Success! created you profile!", ephemeral=False)

#   ===== Profile Updates ===== #
@tree.command(guild = discord.Object(id=dev_server_id), name = 'update_profile_name', description='updates your profile name!') #guild specific slash command
async def slash2(interaction: discord.Interaction, name:str):
    user_id = interaction.user.id
    profile_data_name(user_id, name)
    await interaction.response.send_message(f"Success! Changed name", ephemeral = False)

@tree.command(guild = discord.Object(id=dev_server_id), name = 'update_profile_birth', description='updates your profile birth!') #guild specific slash command
async def slash2(interaction: discord.Interaction, birth:str):
    user_id = interaction.user.id
    profile_data_birth(user_id, birth)
    await interaction.response.send_message(f"Success! Changed birth", ephemeral = False)

@tree.command(guild = discord.Object(id=dev_server_id), name = 'update_profile_desc', description='updates your profile description!') #guild specific slash command
async def slash2(interaction: discord.Interaction, description:str):
    user_id = interaction.user.id
    profile_data_desc(user_id, description)
    await interaction.response.send_message(f"Success! Changed description", ephemeral = False)

@tree.command(guild = discord.Object(id=dev_server_id), name = 'update_profile_background', description='updates your profile background!') #guild specific slash command
async def slash2(interaction: discord.Interaction, backgroud_url:str):
    user_id = interaction.user.id
    profile_data_pbg(user_id, backgroud_url)
    await interaction.response.send_message(f"Success! Changed background", ephemeral = False)


#   ==========================  #
#   ===== Music Commands =====  #
#   ==========================  #
voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

@tree.command(guild = discord.Object(id=dev_server_id), name = 'play', description='testing') #guild specific slash command 944147234562400256
async def slash2(interaction: discord.Interaction, url:str):
    try:
        voice_client = await interaction.user.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except:
        print("error")

    try:
        # discord.FFmpegPCMAudio.cleanup(self=)
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg-2022\\bin\\ffmpeg.exe")

        voice_clients[interaction.user.guild.id].play(player)

    except Exception as err:
        print(err)
    await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = False)

@tree.command(guild = discord.Object(id=dev_server_id), name = 'pause', description='testing') #guild specific slash command 944147234562400256
async def slash2(interaction: discord.Interaction):
    try:
        voice_clients[interaction.user.guild.id].pause()
    except Exception as err:
        print(err)
    await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = False)

@tree.command(guild=discord.Object(id=dev_server_id), name='resume',description='testing')  # guild specific slash command
async def slash2(interaction: discord.Interaction):
    try:
        voice_clients[interaction.user.guild.id].resume()
    except Exception as err:
        print(err)
    await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral=False)

@tree.command(guild = discord.Object(id=dev_server_id), name = 'stop', description='testing') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    try:
        voice_clients[interaction.user.guild.id].stop()
        await voice_clients[interaction.user.guild.id].disconnect()
    except Exception as err:
        print(err)
    await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = False)






client.run('OTY0MzY4NDg3NjAwNDk2Njgw.G1_1LN.N3ZrksNiDbcSGL4sp8Vq4GJFqwADldUZcE0Q6c')
