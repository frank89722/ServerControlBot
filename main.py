import os
import time
import json
import discord
import asyncio
from discord.ext import commands

from serverController import serverController

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

servers = []
svName = []
lastStatus = {}

def serverList():
    folder_content = os.listdir()
    for i, item in enumerate(folder_content):
        if os.path.isdir(item):
            if(item != '.git' and item != '__pycache__' and item != 'funcs'):
                try:
                    with open(item + '/' + item + '.json', 'r', encoding='utf8') as svjfile:
                        svjdata = json.load(svjfile)

                    servers.append(serverController(item, svjdata['JAVA_PARAMETERS'], svjdata['SERVER_JAR']))
                    svName.append(item)
                    lastStatus[item] = ''
                    print(item + ' 已載入')
                    svjfile.close()
                except:
                    print(item + ' 沒有json檔案，所以跳過')
                    pass      

@bot.event
async def on_ready():
    print('Discord bot is ready!')

@bot.command()
async def start(ctx, svN):
    if svN in svName:
        for sv in servers:
            if sv.getServerName() == svN:
                if sv.startServer():
                    await ctx.send(sv.getServerName() + ' 正在啟動')
                else:
                    await ctx.send(sv.getServerName() + ' 本來就開著了')
    else:
        await ctx.send('can\'t find ' + svN)

@bot.command()
async def stop(ctx, svN):
    if svN in svName:
        for sv in servers:
            if sv.getServerName() == svN:
                if sv.stopServer():
                    await ctx.send(sv.getServerName() + ' 正在關閉')
                else:
                    await ctx.send(sv.getServerName() + ' 本來就是關的')
    else:
        await ctx.send('can\'t find ' + svN)

@bot.command()
async def reload(ctx):
    servers = []
    svName = []
    lastStatus = {}
    serverList()
    await ctx.send('重新載入完畢')

@bot.command()
async def svlist(ctx):
    li = ''
    for sv in servers:
        li += sv.getServerName() + ' - ' + sv.getLastStatus() + '\n'
    await ctx.send('```' + li +'```')

@bot.command()
async def commands(ctx):
    await ctx.send('```!start [serverName] - 啟動某個伺服器\n!stop [serverName] - 關閉某個伺服器\n!svlist - 顯示已載入的伺服器\n!reload - 重新載入各伺服器設定\n```')
    
async def serverChecker():
    await bot.wait_until_ready()
    channel = bot.get_channel(jdata['CHANNEL'])
    while not bot.is_closed():
        for sv in servers:
            if sv.checkRestart():
                crp = discord.File(os.path.join(sv.getCrashReport()))
                await channel.send(sv.getServerName() + ' 炸了＝＝')
                await channel.send(file = crp)
                if sv.startServer():
                    await channel.send(sv.getServerName() + ' 正在重起...')
            
            else:
                if lastStatus[sv.getServerName()] != sv.getLastStatus():
                    await channel.send(sv.getServerName() + ' is ' + sv.getLastStatus())
                    lastStatus[sv.getServerName()] = sv.getLastStatus()
                
        await asyncio.sleep(1)

    
if __name__ == '__main__':
    serverList()
    
    with open('discord.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)

    bot.loop.create_task(serverChecker())
    bot.run(jdata['TOKEN'])
    