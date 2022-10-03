import discord

client = discord.Client()

# Bot Config
bot_version = 1.0
bot_dev_mode = bool(False)
# IDs
info_channel_id = 1023238973306458175
invite_channel_id = 1023220232959041611
role_channel_id = 1024237319596802048

info_message_id = 1024246994979524610
role_message_id = 1024247245547245659
invite_message_id = 1024246996447547432

invite_text = 'https://discord.gg/jU6epfjpgF'
info_text = 'Wir sind eine noch recht frische Kompanie, die sich spontan aus "Wiederkehrern" gegründet hat. Unser Fokus liegt auf dem PvE Content von New World. Wir haben keine Mindestanforderungen - Gemeinsame Expeditionen, farmen und gemütliches Beisammensein ohne große Verpflichtungen ist unser Motto! Wenn du Interesse hast uns beizutreten melde dich gerne im #💬allgemein Channel.'
roles_text = '```Reagiert mit dem entsprechenden Emoji auf diese Nachricht, um euch eine Klasse zuzuweisen!```'


if bot_dev_mode:
    help_text = '**!!!ACHTUNG!!! DEV-Mode Aktiv!!!**\n Der Bot (v' + str(bot_version) + ') dient derzeit zur automatischen Rollenverwaltung!\n\nFolgende Commands kannst du nutzen:\n- $bot: Zeigt die Botversion, sowie die verfügbaren Commands\n- $rules: Schickt dir eine PN mit den Serverregeln\n- $chanid: Gibt die aktuelle ChannelID zurück\n**!!!ACHTUNG!!! DEV-Mode Aktiv!!!**'
else:
    help_text = 'Der Bot (v' + str(bot_version) + ') dient derzeit zur automatischen Rollenverwaltung!\n\nFolgende Commands kannst du nutzen:\n- $bot: Zeigt die Botversion, sowie die verfügbaren Commands\n- $rules: Schickt dir eine PN mit den Serverregeln'

class MyClient(discord.Client):
    # Login
    async def on_ready(self):
        print("Bot erfolgreich eingeloggt!")

        infochannel = client.get_channel(info_channel_id)
        rolechannel = client.get_channel(role_channel_id)
        invitechannel = client.get_channel(invite_channel_id)

        # Create Info
        #await infochannel.send(info_text)

        # Create Invite
        #await invitechannel.send(invite_text)

        # Create Rolesmessage
        #await rolechannel.send(roles_text)
        #print("Texte erfolgreich erstellt!")

        # Update Info
        infomessage = await infochannel.fetch_message(info_message_id)
        await infomessage.edit(content=info_text)

        # Update Rolesmessage
        rolesmessage = await rolechannel.fetch_message(role_message_id)
        await rolesmessage.edit(content=roles_text)

        # Update Invite
        invitemessage = await invitechannel.fetch_message(invite_message_id)
        await invitemessage.edit(content=invite_text)
        print("Texte erfolgreich geupdated!")

        # Update Status
        if bot_dev_mode:
            await client.change_presence(activity=discord.Game(name="DEV Mode"))
        else:
            await client.change_presence(activity=discord.Game(name="New World"))

        # Setting `Playing ` status
        # await bot.change_presence(activity=discord.Game(name="a game"))
        # Setting `Streaming ` status
        # await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
        # Setting `Listening ` status
        # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
        # Setting `Watching ` status
        # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))


    # Bei Add Reaction
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == role_message_id:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
            role = None
            
            if payload.emoji.name == 'Tank':
                role = discord.utils.get(guild.roles, name="Tank")
            elif payload.emoji.name == 'Healer':
                role = discord.utils.get(guild.roles, name="Healer")
            elif payload.emoji.name == 'DamageDealer':
                role = discord.utils.get(guild.roles, name="Damage Dealer")

            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                    print("Rolle vergeben!")
                else:
                    print("Rolle nicht gefunden!")

    # Bei Remove Reaction
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == role_message_id:  # ID depends on message
            guild = client.get_guild(payload.guild_id)

            if payload.emoji.name == 'Tank':
                role = discord.utils.get(guild.roles, name="Tank")
            elif payload.emoji.name == 'Healer':
                role = discord.utils.get(guild.roles, name="Healer")
            elif payload.emoji.name == 'DamageDealer':
                role = discord.utils.get(guild.roles, name="Damage Dealer")
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = await guild.fetch_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)
                    print("Rolle entfernt!")
                else:
                    print("User nicht gefunden!")
            else:
                print("Rolle nicht gefunden!")
                
    # Commands
    async def on_message(self, message):
        if message.author == client.user:
            return

        # HELP
        if message.content == "$bot":
            await message.channel.send(help_text)

        if message.content == "$chanid":
            if bot_dev_mode:
                await message.channel.send('Die Channel ID: ' + str(message.channel.id) + '!')
            else:
                await message.channel.send('Diese Funktion gibt es nur im DEV-Mode!')


        # New User Message
        if message.content == "$willkommen":
            if bot_dev_mode:
                await message.author.send(join_message)
            else:
                await message.channel.send('Diese Funktion gibt es nur im DEV-Mode!')

        # Private Nachricht
        if message.content.startswith("$regeln"):
            await message.author.send("Die Regeln - ganz privat!")

    # Neuer User auf dem Server
    @client.event
    async def on_member_join(self, member):
        print("Neuer Nutzer ist da!")
        channel = client.get_channel(welcome_channel_id)
        embed = discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!")  # F-Strings!
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

    @client.event
    async def on_member_remove(self, member):
        print("Nutzer gegangen :(")
        channel = client.get_channel(welcome_channel_id)
        embed = discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!")  # F-Strings!
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

client = MyClient()
client.run("xxxxxxxxx")
