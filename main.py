import discord
from discord import File, app_commands
from discord.ext import commands
import json
import os
import requests
import qrcode
import asyncio
from io import BytesIO
import re
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
headers = {
    'Authorization': f'Bearer {config["sellauth_api"]}'
}

def get_ltc_price():
    url = "https://api.diadata.org/v1/assetQuotation/Litecoin/0x0000000000000000000000000000000000000000"
    response = requests.get(url)
    data = response.json()
    return data["Price"]

def calculate_ltc_amount(usd_amount, ltc_price):
    return usd_amount / ltc_price

def generate_qr_code(address, amount):
    payment_data = f"{address}?amount={amount}"
    img = qrcode.make(payment_data)
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="help", description="Shows all available commands")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="<:Tools_2:1326132401688019065> | Help Menu", description="List of commands available", color=discord.Color.blue())
    
    commands = [
        ("bal", "Check Balance of the sellauth"),
        ("payout", "Withdraw Balance from sellauth"),
        ("getstock", "Withdraw stock out of sellauth"),
        ("invoice", "Check Invoice ID, Fetch details"),
        ("payment", "Create a Payment Invoice"),
        ("process", "Process unpaid invoice manually"),
        ("restock", "Restock any product which is low on stock"),
        ("stock", "Check Products which are in stock"),
        ("replace", "Replace the particular product"),
        ("calc", "Calculate the amounts with the expression"),
        ("checkcpn", "Checks if there is some discount coupon available"),
        ("restocknotif", "Sends restock notification to restock channel"),
        ("createcoupon", "To create a discount coupon"),
        ("coupondelete", "To delete a discount coupon"),
        ("couponedit", "To edit a discount coupon"),
        ("update", "To update a product price and information")
    ]
    
    for cmd, desc in commands:
        embed.add_field(name=f"/{cmd}", value=desc, inline=True)
    
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1318481149777150015/a_9fb7ec7c6b752452808dd6b7a902ff33.gif?size=1024")
    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stock", description="Check available product stock")
@app_commands.checks.cooldown(1, 10.0)
async def stock(interaction: discord.Interaction):
    params = {
        'page': '1',
        'search': '',
        'orderColumn': 'id',
        'orderDirection': 'asc',
    }
    
    response = requests.get(
        f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products',
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        await interaction.response.send_message(f"Failed to retrieve stock data. Error: {response.status_code}")
        return

    data = response.json()
    embed = discord.Embed(title="<:shop:1326128875759079475> | Sellauth Stock", color=discord.Color.green())

    for product in data['data']:
        product_name = product['name']
        stock = product['stock_count'] if product['stock_count'] is not None else "Not Available"
        price = product['price'] if product['price'] is not None else "Not Available"
        products_sold = product['products_sold']

        embed.add_field(
            name=product_name,
            value=f"**<:stock:1322253893026971699> | Stock:** {stock}\n**<:Money:1326113026184708136> | Price:** ${price}\n**<:restocked:1326118109790343170> | Sold:** {products_sold}",
            inline=False
        )

    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="payment", description="Create a payment invoice")
@app_commands.describe(amount="Amount in USD")
async def payment(interaction: discord.Interaction, amount: str):
    if interaction.user.id not in bot.staff:
        await interaction.response.send_message("You do not have permission to use this command.")
        return
        
    cleaned_amount = re.sub(r"[^\d.]", "", amount)
    
    try:
        usd_amount = float(cleaned_amount)
    except ValueError:
        await interaction.response.send_message("Invalid amount. Please provide a valid number.")
        return
    
    address = config["address"]
    ltc_price = get_ltc_price()
    ltc_amount = calculate_ltc_amount(usd_amount, ltc_price)
    qr_code_image = generate_qr_code(address, ltc_amount)

    embed = discord.Embed(title="Litecoin Payment Request", color=discord.Color.green())
    embed.add_field(name="Litecoin Address", value=f"```{address}```", inline=False)
    embed.add_field(name="Amount (LTC)", value=f"{ltc_amount:.6f} LTC", inline=False)
    embed.add_field(name="Amount (USD)", value=f"${usd_amount:.2f}", inline=False)
    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
    
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=discord.File(qr_code_image, "payment_qr.png"))

@bot.tree.command(name="calc", description="Calculate mathematical expressions")
@app_commands.describe(expression="Mathematical expression to calculate")
async def calc(interaction: discord.Interaction, expression: str):
    try:
        if not re.match(r"^[0-9+\-*/().\s]+$", expression):
            await interaction.response.send_message("Invalid expression. Please use numbers and operators only.")
            return
        
        result = eval(expression)
        await interaction.response.send_message(f"Calculated: {result}")
    
    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}")

    

bot.run(config["bot_token"])
