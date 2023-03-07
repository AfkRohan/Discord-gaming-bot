
from discord.ext import commands,tasks;
import discord;
import datetime;
import os;
from dotenv import load_dotenv
import Session;

load_dotenv()
token = os.getenv('TOKEN');
channel_id = os.getenv('CHANNEL_ID');
max_time = os.getenv('MAX_SESSION_TIME');

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all());
session = Session();

@bot.event
async def on_ready():
	print("Hello! Game bot is here");
	channel=bot.get_channel(channel_id);
	await channel.send("Hello! Welcome to this test server");

@tasks.loop(minutes=max_time,count=2)
async def break_remainder():
	if break_remainder.current_loop==0:
		return;
	channel = bot.get_channel(channel_id);
	await channel.send(f"**Take a break NOW!**Its already been {max_time} minutes");

@bot.command()
async def start(ctx):
	if session.is_active==True:
		await ctx.send("Session is already active")
		return;
	session.is_active=True;
	session.start_time=ctx.message.created_at.timestamp();
	human_time = ctx.message.created_at.strftime("%H:%M:%S");
	break_remainder.start();
	await ctx.send(f"**New Session started at {human_time} **")

@bot.command()
async def end(ctx):
	if session.is_active==False:
		await ctx.send("Session is not active!")
		return;
	session.is_active=False;
	end_time=ctx.message.created_at.timestamp();
	duration = end_time-session.start_time;
	human_time = str(datetime.timedelta(seconds=duration));
	break_remainder.stop();
	await ctx.send(f"** Session Ended in {human_time} Minutes**")


@bot.command()
async def hello(ctx):
	await ctx.send("Hey! How are you buddy?");

@bot.command()
async def add(ctx,*arr):
	result = 0;
	for x in arr:
		result+=int(x);
	await ctx.send(result);

bot.run(token);
