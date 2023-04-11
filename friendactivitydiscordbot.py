import random
from selenium import webdriver
import discord
import asyncio
import os
import threading
from discord.ext import commands, tasks
from asyncio import sleep
from selenium.common.exceptions import TimeoutException

url = 'INSERT STEAM URL HERE' #Need Friend's Steam URL here
browser = webdriver.Chrome()
browser.get(url)
savedUrl = None
savedGame = None
urlCheck = True
userList = []
userBalList = []

#creating bot and initializing it
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is Online")
    checkURL.start()


@tasks.loop(seconds = 100)
async def checkURL():
    global savedUrl
    print('refreshing page....')
    browser.refresh()
    try:
        someVar = browser.find_element("xpath", '//*[@id="responsive_page_template_content"]/div/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]').click()
        someUrl = browser.current_url
        if(someUrl!=savedUrl):
            print('new game url found.')
            savedUrl = someUrl
            channel = bot.get_channel("INSERT CHANNEL ID HERE") #Insert Channel ID for Discord Bot to message to here
            await channel.send('User has began playing: ')
            await channel.send(savedUrl) 
    except Exception as e:
       print(e)
    except TimeoutException as ex:
        print(ex.Message)
        browser.get(url)
        browser.refresh()
    browser.get(url)
    await sleep(100)


@bot.command()
async def recentgame(ctx):
    print('recent game called')
    test = browser.find_element("xpath", '//*[@id="responsive_page_template_content"]/div/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[3]/a').click()
    strUrl = browser.current_url
    await ctx.reply(strUrl)
    browser.get(url)


@commands.has_permissions(administrator=True)
@bot.command()
async def echo(ctx, *,args):
    await ctx.send(args)

#simple checking command
@bot.command()
async def hello(ctx):
    await ctx.reply('hello')

bot.run("INSERT TOKEN") #Need Bot Token To Start
