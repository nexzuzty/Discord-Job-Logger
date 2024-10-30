import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

#load environment variables
load_dotenv()

#load the token from an evinronment variable
TOKEN = os.getenv('DISCORD_TOKEN')
MONGODB_URI = os.getenv('MONGODB_URI')

#check to see if available
if not TOKEN:
    print("Error: DISCORD_TOKEN not found. Please check your .env file.")
if not MONGODB_URI:
    print("Error: MONGODB_URI not found. PLease check your .env file.")

#Setup MongoDB client
client = MongoClient(MONGODB_URI)
db = client['job_application_db']
applications_collection = db['applications']


# Set up intents and bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user.name}!')
    
    # Send a message to a specific channel when the bot is ready
    channel_id = 1301121796866834432  # Replace with your channel ID
    channel = bot.get_channel(channel_id)
    
    if channel:
        await channel.send('Bot is now online. Please use !log {{position}} {{company}} {{status}}')
    else:
        print('Channel not found. Please check the channel ID.')


#Command: Ping(for testing)
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

#command for creating application
@bot.command(name="log")
async def log_application(ctx, position: str, company: str, status: str):
    #create a document for the job application
    application = {
        "position": position,
        "company": company,
        "status": status
    }


    result = applications_collection.insert_one(application)

    if result.inserted_id:
        await ctx.send(f"Application logged with ID: {result.inserted_id}")
    else:
        await ctx.send("Error logging application.")

@bot.command(name="update")
async def update_application(ctx, company: str, new_status: str):
    result = applications_collection.find_one({"company": company})

    if result:
        applications_collection.update_one(
        {"company": company},
        {"$set": {"status": new_status}}
    )
        await ctx.send(f"Status updated for '{company}'.")
    else:
        await ctx.send(f"No company found")

try:
    client = MongoClient(MONGODB_URI)
    print(f"ping")
except Exception as e:
    print(f"error connecting to MongoDB: {e}")

# Run the bot
bot.run(TOKEN)