import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

emojis = ["🟥", "🟠", "🟨", "🟢", "🟦", "🟣", "🟫", "⚫", "⬜", "💖", "🟧", "💛", "🟩", "💙", "🟪", "🤎", "⬛", "🤍"]
monthNames = {"jan": 1,"feb":2,"maa":3,"mrt":3,"mar":3,"apr":4,"mei":5,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"okt":10,"oct":10,"nov":11,"dec":12}

# Placeholder values
daysHold = 10
headerHold = "When GAMING?"
inhoudHold = "What evenings are you available?"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def dot(ctx,*args):
    try:
        separatedInfo = await checkInput(ctx, args)
        days = separatedInfo["days"]
        startDate = separatedInfo["startDate"]
        header = separatedInfo["header"]
        inhoud = separatedInfo["inhoud"]
        tag = separatedInfo["tag"]
    except (ValueError, TypeError):
        return
    message_content = tag + "\n# " + header +  "\n\n" + inhoud + "\n\n" + generateDates(ctx, days, startDate)

    # Send the message
    msg = await ctx.send(message_content)
    # Add reactions
    for emoji in emojis[:days]:  # Slice the list to only include the used emojis
        await msg.add_reaction(emoji)

# Check users args
async def checkInput(ctx, args):
    days = daysHold
    startDate = datetime.now()
    header = headerHold
    inhoud = inhoudHold
    titleSet = False
    tag = "@everyone"
    
    # loop over args to detect what inputs are given
    if args:
        for arg in args:
            clean_arg = arg.strip()
            if clean_arg.isnumeric():
                days = int(arg)
                if days < 1 or days > 18: 
                    await ctx.send("Detected a day number. However you must choose a number of days that is not under 1 and not higher than 18.")
                    return
            elif re.fullmatch(r"\d{1,2}[-/,\\|](\d{1,2}|[a-z]{3,9})([-/,\\|]\d{4})?", clean_arg):
                parts = re.split(r"[-/,\\|]", clean_arg)
                try:
                    startDate = await handleCustomStartDate(ctx, parts)
                except ValueError:
                    return
            elif arg.lower() == "@no-one" or arg.lower() == "no@":
                tag = ""
            else:
                if not titleSet:
                    titleSet = True
                    header = arg
                else:
                    inhoud = arg
                        
    return {"days":days,"startDate":startDate,"header":header,"inhoud":inhoud,"tag":tag}


async def handleCustomStartDate(ctx, parts):
    # Get day
    try:
        day = int(parts[0])
    except ValueError:
        await ctx.send("Detected custom start date input on the day spot but its not numerical.")
        return 
    
    # Get month or convert it    
    try:
        dirtyMonth = parts[1]
        if dirtyMonth.isnumeric():
            month = int(dirtyMonth)
        else:
            month = int(monthNames[dirtyMonth[:3].lower()])         
    except ValueError:
        await ctx.send("Detected custom start date input on the month spot but doesn't covert to an actual month.")
        return
        
    # Get year if it is given
    if len(parts) == 3:
        try:
            year = int(parts[2])
        except ValueError:
            await ctx.send("Detected custom start date input on the year spot but its not numerical.")
            return  
    else:
        year = int(datetime.now().strftime('%Y'))

    try:
        startDate = datetime(year, month, day)
    except ValueError:
        await ctx.send("Detected a custom start date. However it failed to convert to an actual date. It should be DD-MM-YYYY (year is optional)")
        await ctx.send(f"You inputted day = {day} month = {month}  year = {year}")
        return
    return startDate
 
 
def generateDates(ctx, days, startDate):
    dates = ""
    # Generate dates with emojis
    for i in range(days):
        date = startDate + timedelta(days=i)
        day_name = date.strftime('%A')  # Full day name (like "Tuesday")
        day_number = date.strftime('%d').rjust(4)  # Right-align the day number to 2 spaces
        month_name = date.strftime("%b")
        dates += f"`{day_name: <10} {day_number} {month_name} {emojis[i]}`\n"
    return dates


@bot.command()
async def info(ctx):
    info = ""
    info += '# Dotbot info:\nDotBot is a bot that can generate a dot voting message.' 
    
    info += '\n\n**!dot**\nWhen you type !dot DotBot will generate a message with a list of dates for the next 10 days and a unique emoji behind each date.'
    
    info += '\n## Custom inputs:' 
    info += '\n**Amount of days**\nWhen you type !dot plus a number 1-18 DotBot will generate the dates for however many days as the number given.'
    
    info += '\n\n**Start date**\nYou can add a custom start date in the format DD-MM-YYYY (year is optional, add it in december...). You can write the month as a number, an abbreviation or fully'
    
    info += '\n\n**Title and Content**' 
    info += '\nDotBot will add the first "quoted" text as title and the second as content.'
    info += '\nExample: !dot "Example title" "Example content\nYou can add enters by doing shift+enter like how you would in your own message.'
    info += '\nJust make sure to end the quotation marks!!"'
    
    info += '\n\n**@no-one**\nFor testmessages! The @no-one ensures that dotbot will NOT tag everyone. Otherwise it is always true'
    
    info += '\n\n**The inputs can go in any order**, you can include or leave out any! (except when you want to change the content, this must always come somewhere after the title)'
    await ctx.send(info)
    return
    
# Meme stuff
@bot.event
async def on_message(message):
    if re.search("wat is de code?", message.content, re.IGNORECASE):
        await message.channel.send('https://tenor.com/view/family-guy-peter-griffin-he-said-it-he-said-gif-5286270')
    if re.search("heeft cyn gelijk?", message.content, re.IGNORECASE):
        await message.channel.send('"Jep 👌😌"')
    await bot.process_commands(message)
    return
        
bot.run(os.environ.get('DISCORD_BOT_TOKEN'))