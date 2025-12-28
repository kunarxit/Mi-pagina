import discord
import time
from discord.ext import commands, tasks
intents = discord.Intents.default()
intents.message_content = True

start_time = time.time() 
bot = commands.Bot(command_prefix=",",intents=intents)

MENSAJE = "Mensaje por defecto"
CANAL_ID = None

@bot.command()
@commands.has_permissions(administrator=True)
async def ch(ctx):
    global CANAL_ID
    CANAL_ID = ctx.channel.id
    await ctx.send("✅ Canal de envío cambiado a este canal")

@tasks.loop(seconds=4)
async def loop_mensaje():
    canal = bot.get_channel(CANAL_ID)
    if canal:
        await canal.send(MENSAJE)

@bot.event
async def on_ready():
    print("Bot listo")

# 🔒 Solo admins
def es_admin(ctx):
    return ctx.author.guild_permissions.administrator

@bot.command()
@commands.check(es_admin)
async def start(ctx):
    if not loop_mensaje.is_running():
        loop_mensaje.start()
        await ctx.send("✅ Loop iniciado")
    else:
        await ctx.send("⚠️ El loop ya está activo")

@bot.command()
@commands.check(es_admin)
async def stop(ctx):
    if loop_mensaje.is_running():
        loop_mensaje.stop()
        await ctx.send("🛑 Loop detenido")
    else:
        await ctx.send("⚠️ El loop no está activo")

@bot.command()
@commands.check(es_admin)
async def msj(ctx, *, texto):
    global MENSAJE
    MENSAJE = texto
    await ctx.send(f"✏️ Mensaje cambiado a:\n{texto}")


# commando para enviar mensajes atravez del bot


@bot.command()
async def say(ctx, canal: discord.TextChannel = None, *, mensaje=None):
    if not canal or not mensaje:
        await ctx.send("❌ Uso correcto: `!say #canal mensaje`")
        return
    await ctx.message.delete()
    await canal.send(mensaje)




# commando para ver el tiempo que el bot lleva activo

@bot.command()
@commands.has_permissions(administrator=True)
async def uptime(ctx):
    segundos = int(time.time() - start_time)

    dias = segundos // 86400
    horas = (segundos % 86400) // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    await ctx.send(
        f"🟢 **Bot activo desde hace:** `{dias}d {horas}h {minutos}m {segundos}s`"
    )



# comando para ver el ping

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Ping: ´{latency}ms´")

# commando para eliminar mensajes

@bot.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(manage_messages=True)
async def p(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f" se eliminaron {amount} mensajes.", delete_after=5)


@bot.event
async def on_ready():
    print(f"bot connectado como {bot.user}")
    

# commando para banear personas

@bot.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} lo banearon. Razón: {reason if reason else 'NO especificada'}")
    except Exception as e:    
       await ctx.send(f"No se pudo banear a {member.name}. Error: {e}")




# commando para desbanear usuarios

@bot.command()
@commands.has_permissions(administrator=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user:str):
    try:
        banned_users = await ctx.guild.bans()
        name, discriminator = user.split("#")
        
        for ban_entry in banned_users:
            usuario = ban_entry.user
            if usuario.name == name and usuario.discriminator == discriminator:
                await ctx.guild.unban(usuario)
                await ctx.send(f"{usuario.name}#{usuario.discriminator} fue desbaneado.")
                return
            
        await ctx.send("revisa bien el nombre malparido.")
    except:
        await ctx.send("commando no valido. usa: ,unban `Nombre#000`")



#commando para mostrar los demas commandos

@bot.command()
async def inf(ctx):
    embed = discord.Embed(
        title=" lista de commandos",
        description=" aqui estan todos los commandos disponibles",
        color=discord.Color.red()
        )
    embed.add_field(name=",uptime", value="muestra cuanto tiempo lleva el bot activo")
    embed.add_field(name=",ping", value="muestra el ping del bot.")
    embed.add_field(name=",p", value="borra mensajes.")
    embed.add_field(name=",inf", value="muestra todos los commandos disponibles.")
    embed.add_field(name=",ban", value="banea al mienbro mencionado.")
    embed.add_field(name=",unban", value="desbanea al miembro mencionado.")
    embed.add_field(name=",say", value="commando para enviar mensajes atravez del bot")
    embed.add_field(name=",msj", value="commando para agregar un mensaje para que el bot repita")
    embed.add_field(name=",start", value="commando para iniciar el loop")
    embed.add_field(name=",stop", value="detener el loop")
    embed.add_field(name=",ch", value="eligir el canal por el cual enviara el loop (poner id del canal)")
    await ctx.send(embed=embed)


bot.run("")
