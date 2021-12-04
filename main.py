import json
import discord
from youtube import *
from datetime import datetime
from weby import *
from datetime import datetime
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
aktive = False
def nacti_slova():
    pass
conf = []
def nacti_json():
    with open("config.json", mode="r") as f:
        global conf
        data = f.read()
        conf = json.loads(data)
zpravy = {}
allowed_users = []
nacti_json()
prefix = "!"
pouzivatele = {}
@client.event
async def on_ready():
    print("ahoj")
    for guild in client.guilds:
        mezi = []
        for member in guild.members:
            print(member)
            for a in member.roles:
                print(a)
                if str(a) == "Moderátor":
                    mezi.append(member.name)
                    allowed_users.append(member)
        pouzivatele[guild.name] = mezi
    print(pouzivatele)
    with open("users.json", mode="w") as f:
        f.write(json.dumps(pouzivatele))
    print(allowed_users)
async def smazat(message,zprava):
    await message.delete()
    print("ajo")
    await message.author.send("VAROVÁNÍ "+zprava)
async def strezic(message):
    if message.author.bot == True:
        return
    nacti_json()
    message.content = message.content.lower()
    for i in conf[message.guild.name]:
        with open("zpravy.json", mode="r") as f:
            zpravy = json.loads(f.read())
            try:
                for b in zpravy[message.guild.name][message.author.name]:
                    print(b)
                    zprava = zpravy[message.guild.name][message.author.name]
                    ind = zprava.index(b)
                    zprava[ind] = zprava[ind].lower()
            except:
                zprava = []
            print(zpravy)
        zpravy[message.guild.name][message.author.name] = zprava
        if message.content.find(i.lower()) >= 0:
            await smazat(message, "Na tomto serveru nebudeme tolerovat ŽÁDNÁ sprosté slova.")
            for b in allowed_users:
                if b.guild.name == message.guild.name:
                    await b.send("uživatel "+str(message.author)+" Napsal sprosté slovo na serveru: "+str(message.guild.name)+". Celá zpráva: "+str(message.content))
            if not message.content in zpravy[message.guild.name][message.author.name]:
                with open("zpravy.json", mode="w") as a:
                    try:
                        zpravy[message.guild.name][message.author.name].append(message.content)
                        print("append")
                    except KeyError:
                        zpravy[message.guild.name] = {message.author.name: []}
                        print(zpravy)
                        print(type(zpravy[message.guild.name]), zpravy)
                        zpravy[message.guild.name][message.author.name].append(message.content)
                        print("KeyError")
                    a.write(json.dumps(zpravy))
    print(zpravy)
def zapsat(id, message):
    global mezi
    with open("idkca.json", mode="r") as a:
        mezi = json.loads(a.read())
    with open("idkca.json", mode="w") as f:
        mezi[message.guild.name] = str(id)
        print(mezi)
        f.write(json.dumps(mezi))
def nacist(message):
    with open("idkca.json", mode="r") as s:
        guild = client.get_guild(message.guild_id)
        return json.loads(s.read())[guild.name]
async def embediky(videa, message, nadpis):
    print("vypisuji")
    user = await client.fetch_user(909015370864689162)
    for tema, odkazy in videa.items():
        embedik = discord.Embed(
            title="Aktuality z: " + nadpis + " téma: "+tema,
            description="**Odkazy: **",
            url="https://www.vzdelanibudoucnosti.cz/",
            timestamp=datetime.now(),
        )
        if odkazy == []:
            continue
        for video in odkazy:
            print(video)
            embedik.add_field(name=list(video)[1], value=list(video)[0], inline=False)
        embedik.set_author(name="příkaz od: " + message.author.display_name, url="https://vzdelanibudoucnosti.cz", icon_url=user.avatar_url)
        print(embedik)
        await message.channel.send(embed=embedik)
@client.event
async def on_message(message):
    await strezic(message)
    if message.content.startswith(prefix+"ahoj"):
        print("posilam")
        embedik = discord.Embed(
            title="kliknutím na reakci si přidělíš roli",
            description="Pravidla: \n 1. Buďte na sebe hodní \n 2. Nemluvte sprostě \n 3. Žádný nsfw content \n 4.Porušení pravidel bude trestáno administrátory a botem. \n 5. Pokud napíšete sprosté slovo, bude celá zpráva přeposlána uživatelům s rolí <@&844673978778124338> \n Kliknutím na reakci níže vyjadřuješ souhlas s těmito pravidly. :white_check_mark: ",
            url="https://www.vzdelanibudoucnosti.cz/",
            timestamp=datetime.now(),
        )
        msg = await message.channel.send(embed=embedik)
        zapsat(msg.id, message)
        await msg.add_reaction('✅')
        await message.delete()
    if message.content.startswith(prefix + "aktuality"):
        delka = 2+len("aktuality")
        print(message.content[delka:])
        if message.content[delka:] == "youtube":
            print("sap")
            await message.reply("Pracuji...")
            async with message.channel.typing():
                videa = vysledky()
            pprint(videa)
            await embediky(videa, message, "Youtube")
        elif message.content[delka:] == "weby":
            await message.reply("Pracuji...")
            videa = {}
            async with message.channel.typing():
                vraceno = stahni()
            for tema, odkaz in vraceno.items():
                print(odkaz)
                mezi = []
                for odkazicek in zip(odkaz["list_clanku"], odkaz["nadpis"]):
                    print(odkazicek)
                    mezi.append([odkazicek[0], odkazicek[1]])
                videa[tema] = mezi
            pprint(videa)
            await embediky(videa, message, "webů:")
        else:
            embedik = discord.Embed(
                title="Aktuality",
                description="Pro Aktuality z youtubu přidej reakci ✅ pro aktuality z webl",
                url="https://www.vzdelanibudoucnosti.cz/",
                timestamp=datetime.now(),
            )
            msg = await message.channel.send(embed=embedik)
            await msg.add_reaction('✅')
@client.event
async def on_raw_reaction_add(payload):
    print("trigger")
    ourMessageId = nacist(payload)
    print(ourMessageId)
    if str(ourMessageId) == str(payload.message_id):
        member = payload.member
        guild = member.guild
        role = discord.utils.get(guild.roles, name="ověřený")
        await member.add_roles(role)
client.run("OTA5MDE1MzcwODY0Njg5MTYy.YY-IiQ.lrw0gtK-GZcqRhnwy1EYGSETORg")