import discord
from discord import File
from discord.ext import commands
import json
import os
os.system('cls')
import requests
import random
import time
import aiohttp
import io
import asyncio
import discord
import datetime
from discord.ext import commands
import qrcode
import requests
from io import BytesIO
import json
import re
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)
class PurchaseView(discord.ui.View):
    def __init__(self, ltc_address, qr_code):
        super().__init__()
        self.ltc_address = ltc_address
        self.qr_code = qr_code

    @discord.ui.button(label="Get LTC Address", style=discord.ButtonStyle.primary)
    async def ltc_address_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{self.ltc_address}")

    @discord.ui.button(label="Get LTC QR Code", style=discord.ButtonStyle.primary)
    async def ltc_qr_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(file=self.qr_code)

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
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





bot.admins = config["admin_id"]
bot.owners = config["owner_id"]
bot.staff = config["staff_id"] 
@bot.command()
async def checkcpn(ctx):
    if ctx.author.id not in bot.staff:
        await ctx.send("You do not have permission to use this command.")
        return
    response = requests.get(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/coupons?page=1&search=&orderColumn=id&orderDirection=asc',headers=headers)
    data = response.json()
    embed = discord.Embed(title="Available Coupons", color=discord.Color.green())

    for coupon in data['data']:
        coupon_id = coupon.get('id', 'No ID available')
        coupon_code = coupon.get('code', 'No code available')
        discount = coupon.get('discount', 'No discount available')
        product_name = coupon['products'][0].get('name', 'No product name available')
        
        embed.add_field(
            name=f"<:identity:1326256999691845633> | Code: {coupon_id}\n<:Voucher:1326159334941659157> | Coupon Code: {coupon_code}",
            value=f"<:discount:1326159417405866047> | Discount: {discount}%\n<:stock:1322253893026971699> | Product: {product_name}",
            inline=False
        )

    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
    
    await ctx.send(embed=embed)
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="<:Tools_2:1326132401688019065> | Help Menu", description="List of commands available", color=discord.Color.blue())
    embed.add_field(name=".bal", value="Check Balance of the sellauth.", inline=True)
    embed.add_field(name=".payout", value="Withdraw Balance from sellauth.", inline=True)
    embed.add_field(name=".getstock ", value="Withdraw stock out of sellauth.", inline=True)
    embed.add_field(name=".invoice ", value="Check Invoice ID , Fetch details.", inline=True)
    embed.add_field(name=".payment ", value="Create a Payment Invoice.", inline=True)
    embed.add_field(name=".process ", value="Process unpaid invoice manually.", inline=True)
    embed.add_field(name=".restock ", value="Restock any product which is low on stock or outofstock", inline=True)
    embed.add_field(name=".stock ", value="Check Products which are in stock.", inline=True)
    embed.add_field(name=".replace ", value="Replace the particular product.", inline=True)
    embed.add_field(name=".calc ", value="Calculate the amounts with the expression.", inline=True)
    embed.add_field(name=".checkcpn ", value="Checks if there is some discount coupon available.    ", inline=True)
    embed.add_field(name=".restocknotif ", value="Sends restock notification to restock channel.", inline=True)
    embed.add_field(name=".createcoupon ", value="To create a discount coupon.", inline=True)
    embed.add_field(name=".coupondelete ", value="To delete a discount coupon.", inline=True)
    embed.add_field(name=".couponedit ", value="To edit a discount coupon.", inline=True)
    embed.add_field(name=".update ", value="To update a product price and information.", inline=True)
    embed.add_field(name=".purchase ", value="To purchase a product directly via discord.", inline=True)
    embed.add_field(name=".getdelivery ", value="To get delivery of the product directly via discord.", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1318481149777150015/a_9fb7ec7c6b752452808dd6b7a902ff33.gif?size=1024")
    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")

    await ctx.send(embed=embed)
@bot.command()
async def calc(ctx, expression: str):
    try:
        if not re.match(r"^[0-9+\-*/().\s]+$", expression):
            await ctx.send("Invalid expression. Please use numbers and operators only.")
            return
        
        result = eval(expression)
        
        await ctx.send(f"Calculated: {result}")
    
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
@bot.command()
async def couponedit(ctx, id, CodeName, productid, discountamnt):
    if ctx.author.id not in bot.admins:
        await ctx.send("You are not authorized for this command.")
        return
    json_data = {
        'id': id,
        'code': f'{CodeName}',
        'global': 0,
        'discount': f'{discountamnt}',
        'type': 'percentage',
        'products': [
            productid,
        ],
    }

    response = requests.put(
        f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/coupons/{id}/update',
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        embed = discord.Embed(title="```💴``` | Sellauth Coupon:", color=discord.Color.green())
        embed.add_field(name="<:user:1326112782122225684> | User: ", value=f"<@{ctx.author.id}>", inline=False)
        embed.add_field(name="<:voucher:1326245770055389187> | Edited Coupon: ", value=f"{id}", inline=False)
        embed.add_field(name="<:discount:1326159417405866047> | Discount: ", value=f"{discountamnt}%", inline=False)
        embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
        await ctx.send(embed=embed)
@bot.command()
async def check(ctx, transaction_id: str):
    if ctx.author.id not in bot.staff:
        await ctx.send("You do not have permission to use this command.")
        return
    url = f"https://api.blockcypher.com/v1/ltc/main/txs/{transaction_id}?limit=50&includeHex=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        await ctx.send("Transaction not found or invalid ID.")
        return
    
    data = response.json()
    
    address = config["address"]
    transaction_hash = data["hash"]
    block_hash = data["hash"]
    total_value = 0
    
    for output in data["outputs"]:
        if address in output["addresses"]:
            total_value += output["value"]
    
    ltc_price = get_ltc_price()
    value_in_ltc = total_value / 100000000 
    value_in_usd = value_in_ltc * ltc_price
    
    embed = discord.Embed(title=f"Transaction Details: ", color=discord.Color.green())
    embed.add_field(name="Block Hash", value=block_hash, inline=False)
    embed.add_field(name="Total Value in LTC", value=f"{value_in_ltc:.6f} LTC", inline=False)
    embed.add_field(name="Total Value in USD", value=f"${value_in_usd:.2f}", inline=False)
    embed.add_field(name=f"Address Received:", value=f"{address}", inline=False)
    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
    
    await ctx.send(embed=embed)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

headers = {
    'Authorization': f'Bearer {config["sellauth_api"]}'
}
@bot.command()
async def payment(ctx, amount: str):
    if ctx.author.id not in bot.staff:
        await ctx.send("You do not have permission to use this command.")
        return
    cleaned_amount = re.sub(r"[^\d.]", "", amount)
    
    try:
        usd_amount = float(cleaned_amount)
    except ValueError:
        await ctx.send("Invalid amount. Please provide a valid number.")
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
    await ctx.send(embed=embed)
    await ctx.send(file=discord.File(qr_code_image, "payment_qr.png"))

with open('config.json', 'r') as f:
    config = json.load(f)

@bot.command()
async def restocknotif(ctx):
    if ctx.author.id not in bot.staff:
        await ctx.send("You do not have permission to use this command.")
        return
    channel_id = config["restockchannelID"]  
    channel = bot.get_channel(channel_id)
    params = {
        'page': '1',
        'search': '',
        'orderColumn': 'id',
        'orderDirection': 'asc',
    }
    
    response = requests.get(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products', headers=headers, params=params)
    
    if response.status_code != 200:
        await ctx.send(f"Failed to retrieve stock data. Error: {response.status_code}")
        return

    data = response.json()
    embed = discord.Embed(title="<:shop:1326128875759079475> | Sellauth Stock", color=discord.Color.green())

    for product in data['data']:
        product_name = product['name']
        stock = product['stock_count'] if product['stock_count'] is not None else "Not Available"
        price = product['price'] if product['price'] is not None else "Not Available"
        products_sold = product['products_sold']
        path = product['path']

        autobuy_link = f"https://mralts.mysellauth.com/product/{path}"


        embed.add_field(
            name=product_name,
            value=f"**<:stock:1322253893026971699> | Stock:** {stock}\n"
                  f"**<:Money:1326113026184708136> | Price:** ${price}\n"
                  f"**<:restocked:1326118109790343170> | Sold:** {products_sold}\n"
                  f"**Autobuy:** [Link]({autobuy_link})",  
            inline=False
        )

    embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
    await ctx.send("Sucessfully sent the product message.")
    await channel.send(embed=embed)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)

async def stock(ctx):
    params = {
        'page': '1',
        'search': '',
        'orderColumn': 'id',
        'orderDirection': 'asc',
    }
    
    response = requests.get(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products', headers=headers, params=params)
    
    if response.status_code != 200:
        await ctx.send(f"Failed to retrieve stock data. Error: {response.status_code}")
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
    await ctx.send(embed=embed)
@stock.error
async def stock_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Try again in {round(error.retry_after, 1)} seconds.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
@bot.command()
async def getstock(ctx,productid):
    if ctx.author.id not in bot.owners:
        await ctx.send("You do not have permission to use this command.")
        return

    response = requests.get(
        f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products/{productid}/deliverables',
        headers={
            'sec-ch-ua-platform': '"Windows"',
            'Authorization': f'Bearer {config["sellauth_api"]}',
            'Referer': 'https://dashboard.mysellauth.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
        }
    )

    if response.status_code == 200:
        deliverables = response.json()
        deliverables_text = "\n".join([str(d) for d in deliverables])
        
        file = io.StringIO(deliverables_text)
        file.name = "deliverables.txt"
        
        await ctx.author.send("Here are the deliverables:", file=discord.File(file))
        await ctx.send("Deliverables file has been sent to your DM.")
    else:
        await ctx.send(f"Failed to fetch deliverables: {response.text}")
@bot.command()
async def invoice(ctx, invoice_id: str):
    if ctx.author.id not in bot.admins:
        await ctx.send("You do not have permission to use this command.")
        return
    try:
        invoice_id = invoice_id.split('-')[1]
    except IndexError:
        await ctx.send("Invalid invoice ID format. Please use the format: xxxxxxxxxxxxxxxx-xxxxxxxxxxxx")
        return

    shop_response = requests.get('https://api.sellauth.com/v1/shops', headers=headers)
    log_data = {
        "content": f"User {ctx.author.name} ({ctx.author.id}) requested Invoice: {invoice_id}.",
        "embeds": [
            {
                "title": "Invoice Command Used",
                "description": f"User: {ctx.author.name} ({ctx.author.id})\n Requested Invoice Details: {invoice_id} ",
                "color": 5814783 
            }
        ]
    }
    if shop_response.status_code == 200:
        shops = shop_response.json()

        if len(shops) > 1:
            shop_list = "\n".join([f"{idx + 1}: {shop['name']} (ID: {shop['id']})" for idx, shop in enumerate(shops)])
            await ctx.send(f"Multiple shops found:\n{shop_list}\nPlease enter the number corresponding to the desired shop.")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

            try:
                user_response = await bot.wait_for('message', check=check, timeout=30.0)
                selected_index = int(user_response.content) - 1
                
                if 0 <= selected_index < len(shops):
                    shop_id = shops[selected_index]['id']
                else:
                    await ctx.send("Invalid selection. Please try again.")
                    return
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. Please try again.")
                return
        else:
            shop_id = shops[0]['id']
    else:
        await ctx.author.send("Failed to get shop ID")
        return

    invoice_url = f"https://api.sellauth.com/v1/shops/{shop_id}/invoices/{invoice_id}"
    invoice_response = requests.get(invoice_url, headers=headers)

    if invoice_response.status_code == 200:
        invoice_details = invoice_response.json()
        extracted_details = {
            "id": invoice_details.get("id"),
            "created_at": invoice_details.get("created_at"),
            "completed_at": invoice_details.get("completed_at"),
            "gateway": invoice_details.get("gateway"),
            "email": invoice_details.get("email"),
            "status": invoice_details.get("status"),
            "price": invoice_details.get("price"),
            "currency": invoice_details.get("currency"),
            "product_name": invoice_details.get("product", {}).get("name"),
        }

        deliverables = invoice_details.get("delivered")

        if deliverables:
            deliverables_filename = f"deliverable/deliverables_{invoice_id}.txt"
            with open(deliverables_filename, "w") as file:
                if isinstance(deliverables, list):
                    file.write('\n'.join(deliverables))
                else:
                    file.write(deliverables)
            webhook_url = config["webhook1"]
            formatted_invoice_details = json.dumps(extracted_details, indent=4)
            await ctx.author.send(f"Invoice Details:\n```json\n{formatted_invoice_details}\n```")
            requests.post(webhook_url, data=json.dumps(log_data), headers={"Content-Type": "application/json"})
            await ctx.author.send(file=discord.File(deliverables_filename))

            os.remove(deliverables_filename)
        else:
            formatted_invoice_details = json.dumps(extracted_details, indent=4)
            await ctx.author.send(f"Invoice Details:\n```json\n{formatted_invoice_details}\n```")
            requests.post(webhook_url, data=json.dumps(log_data), headers={"Content-Type": "application/json"})
            await ctx.author.send("No deliverables found.")
    else:
        await ctx.author.send("Failed to get invoice details")

@bot.command()
async def replace(ctx, invoice_id, numberofaccounts):
    if ctx.author.id not in bot.admins:
        await ctx.send("You do not have permission to use this command.")
        return 
    
    try:
        if '-' in numberofaccounts:
            start, end = map(int, numberofaccounts.split('-'))
            if start > end:
                await ctx.send("Invalid range. Start should be less than or equal to end.")
                return
            replacements = {str(i): 'STOCK' for i in range(start, end + 1)}
            json_data = {'replacements': replacements}
            response_post = requests.post(
                f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/invoices/{invoice_id}/replace-delivered',
                headers=headers,
                json=json_data,
            )
            if response_post.status_code == 500:
                embed = discord.Embed(title="<:restart:1326150218630168587> | Replace Product:", color=discord.Color.green())
                embed.add_field(name="<:user:1326112782122225684> | User:", value=f"<@{ctx.author.id}>", inline=False)
                embed.add_field(name="<:stock:1326150850476769330> | Replaced: ", value=f"Number Of Account: {numberofaccounts}", inline=False)
                embed.add_field(name="<:shop:1326128875759079475> | Invoice ID: ", value=f"{invoice_id}", inline=False)
                embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
                await ctx.send(embed=embed)  
            else:
                print(f"Error: {response_post.status_code}, {response_post.text}")
        else:
            replacements = {str(numberofaccounts): 'STOCK'}
            json_data = {'replacements': replacements}
            response_post = requests.post(
                f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/invoices/{invoice_id}/replace-delivered',
                headers=headers,
                json=json_data,
            )
            if response_post.status_code == 500:
                embed = discord.Embed(title="<:restart:1326150218630168587> | Replace Product:", color=discord.Color.green())
                embed.add_field(name="<:user:1326112782122225684> | User:", value=f"<@{ctx.author.id}>", inline=False)
                embed.add_field(name="<:stock:1326150850476769330> | Replaced: ", value=f"Number Of Account: {numberofaccounts}", inline=False)
                embed.add_field(name="<:shop:1326128875759079475> | Invoice ID: ", value=f"{invoice_id}", inline=False)
                embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
                await ctx.send(embed=embed)  
            else:
                print(f"Error: {response_post.status_code}, {response_post.text}")

    except ValueError:
        await ctx.send("Invalid input. Please provide a valid range like `1-10` or a single number.")
@bot.command()
async def restock(ctx,productid):
    if ctx.author.id not in bot.owners:
        await ctx.send("You do not have permission to use this command.")
        return

    await ctx.send("Please upload the restock file.")

    def check(message):
        return message.author == ctx.author and len(message.attachments) > 0

    try:
        message = await bot.wait_for('message', check=check, timeout=120)

        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            file_content = await attachment.read()

            try:
                deliverables = file_content.decode('utf-8').splitlines()
            except UnicodeDecodeError:
                await ctx.send("The file format is not supported or is corrupted.")
                return

            json_data = {'deliverables': [d.strip() for d in deliverables if d.strip()]}
            valid_lines = [line for line in deliverables if line.strip()]
            valid_lines_count = len(valid_lines)
            response = requests.put(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products/{productid}/deliverables/append', 
                                    headers={
                                        'sec-ch-ua-platform': '"Windows"',
                                        'Authorization': f'Bearer {config["sellauth_api"]}',
                                        'Referer': 'https://dashboard.mysellauth.com/',
                                        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                                        'sec-ch-ua-mobile': '?0',
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json',
                                    }, 
                                    json=json_data)

            if response.status_code == 200:
                embed = discord.Embed(title="<:stock:1322253893026971699> | Stock Update:", color=discord.Color.green())
                embed.add_field(name="<:user:1326112782122225684> | User:", value=f"<@{ctx.author.id}>", inline=False)
                embed.add_field(name="<:product:1322253931027365889> | Restocked: ", value=f"Product: {productid}", inline=False)
                embed.add_field(name="<:restocked:1326118109790343170> | Amount: ", value=f"{valid_lines_count}", inline=False)
                embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Failed to restock: {response.text}")
        else:
            await ctx.send("No file attached. Please upload a valid file.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to upload the file. Please try again.")

@bot.command()
async def deletecoupon(ctx,id):
    if ctx.author.id not in bot.admins:
        await ctx.send("You do not have permission to use this command.")
        return
    
    response = requests.delete(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/coupons/{id}', headers=headers)
    if response.status_code == 200:
        embed = discord.Embed(title="```💴``` | Sellauth Coupon:", color=discord.Color.green())
        embed.add_field(name="<:user:1326112782122225684> | User: ", value=f"<@{ctx.author.id}>", inline=False)
        embed.add_field(name="<:voucher:1326245770055389187> | Deleted Coupon: ", value=f"{id}", inline=False)
        embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
        await ctx.send(embed=embed) 
@bot.command()
async def createcoupon(ctx, discount, code, *products):

    if ctx.author.id not in bot.admins:
        await ctx.send("You do not have permission to use this command.")
        return

    json_data = {
        'type': "percentage",
        'discount': discount,
        'global': False,
        'code': code,
        'max_uses': '',
        'expiration_date': '',
        'allowed_emails': '',
        'products': products,
    }

    json_str = json.dumps(json_data, indent=4)
    response = requests.post(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/coupons', headers=headers, json=json.loads(json_str))
    print(response.text)
    
    if response.status_code == 200:
        embed = discord.Embed(title="```💷``` | Sellauth Coupons:", color=discord.Color.green())
        embed.add_field(name="<:user:1326112782122225684> | User:", value=f"<@{ctx.author.id}>", inline=False)
        embed.add_field(name="<:voucher:1326245770055389187> | Coupon Created: ", value=f"{code}", inline=False)
        embed.add_field(name="<:Money:1326113026184708136> | Discount", value=f"{discount}%", inline=False)
        embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
        await ctx.send(embed=embed)
    else: 
        await ctx.send(f"Error creating coupon: {response.status_code}")
@bot.command()
async def update(ctx, product_id: int, new_price: str):
    if ctx.author.id not in bot.owners:
        await ctx.send("You do not have permission of this.")
        return
    fetch_url = f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products/{product_id}'
    
    response = requests.get(fetch_url, headers=headers)
    data = response.json()
    stock = data['stock_count']
    proudctname = data['name'] 
    if response.status_code == 200:
        json_data = response.json()
        json_data['price'] = new_price
        if not json_data['variants']:
            json_data['variants'] = [{
                'id': None,
                'type': 'single',
                'price': new_price,
            }]
        else:
            json_data['variants'][0]['price'] = new_price
        
        put_url = f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/products/{product_id}/update'
        
        put_response = requests.put(put_url, headers=headers, json=json_data)
        if put_response.status_code == 200:
            embed = discord.Embed(title="```💷``` | Sellauth Product:", color=discord.Color.green())
            embed.add_field(name="<:stock:1322253893026971699> | Product Name:", value=f"{proudctname}", inline=False)
            embed.add_field(name="<:voucher:1326245770055389187> | New Price: ", value=f"{new_price}", inline=False)
            embed.add_field(name="<:Money:1326113026184708136> | Stock: ", value=f"{stock}", inline=False)
            embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Error updating product {product_id}: {put_response.status_code}")
    else:
        await ctx.send(f"Error fetching product data for {product_id}: {response.status_code}")


@bot.command()
async def bal(ctx):
    if ctx.author.id not in bot.staff:
        await ctx.send("You do not have permission to use this command.")
        return    
    response = requests.get(
        f"https://api.sellauth.com/v1/shops/{config['shop_id']}/payouts/balances",
        headers={'Authorization': f'Bearer {config["sellauth_api"]}'},
    )
    data = response.json()
    print(response.text)
    BalanceLTC = data["ltc"]["ltc"]
    BalanceUSD = data["ltc"]["usd"]
    if ctx.author.id in bot.admins:
        embed = discord.Embed(title="```💴``` | Wallet Balance:", color=discord.Color.green())
        embed.add_field(name="<:user:1326112782122225684> | Wallet User:", value=f"MR ALTS", inline=False)
        embed.add_field(name="<a:ltcan:1326108601273815071> | Balance (LTC)", value=f"{BalanceLTC:.6f} LTC", inline=False)
        embed.add_field(name="<:Money:1326113026184708136> | Balance (USD)", value=f"${BalanceUSD:.2f}", inline=False)
        embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
        await ctx.send(embed=embed)

@bot.command()
async def payout(ctx, ltcaddy: str, amount_in_usd: float):
    if ctx.author.id not in bot.owners:
        await ctx.send("You do not have permission to use this command.")
        return

    ltc_price = get_ltc_price()
    if ltc_price is None:
        await ctx.send("Unable to fetch the current LTC price.")
        return
    
    amount_in_ltc = amount_in_usd / ltc_price
    amount_in_ltc = round(amount_in_ltc, 6)

    if amount_in_ltc < 0.001:  
        await ctx.send("Amount is too low for payout. Minimum payout amount is 0.001 LTC.")
        return

    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Authorization': f'Bearer {config["sellauth_api"]}',
        'Referer': 'https://dashboard.mysellauth.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'currency': 'ltc',
        'address': ltcaddy,
        'amount': amount_in_ltc,
        'tfa_code': '',
    }
    log_data = {
        "content": f"User {ctx.author.name} ({ctx.author.id}) requested payout of {amount_in_usd}.",
        "embeds": [
            {
                "title": "Payout Command Used",
                "description": f"User: {ctx.author.name} ({ctx.author.id})\n Requested Payout: ${amount_in_usd} ",
                "color": 5814783 
            }
        ]
    }
    try:
        response = requests.post(f'https://api-internal.sellauth.com/v1/shops/{config["shop_id"]}/payouts/payout', headers=headers, json=json_data)
        data = response.json()
        transaction_id = data['payout']['transaction_id']
        transactionid = transaction_id['result']
        if response.status_code == 200:
            embed = discord.Embed(title="```💶``` | Payout Request:", color=discord.Color.green())
            embed.add_field(name="<:details:1326108726461202452> | LTC Address: ", value=f"{ltcaddy}", inline=False)
            embed.add_field(name="<a:ltcan:1326108601273815071> | Requested Amount (LTC): ", value=f"{amount_in_ltc:.6f} LTC", inline=False)
            embed.add_field(name="<:usd:1326108519870627923> | Requested Amount (USD): ", value=f"${amount_in_usd:.2f}", inline=False)
            embed.add_field(name="<:payment:1326108443576107051> | Transaction ID: ", value=f"{transactionid}", inline=False)
            embed.set_footer(text="Powered by MR ALTS", icon_url="https://cdn.discordapp.com/avatars/1278919288870273024/a_0d6cf77b7d144815fb230d8103ae0296.gif?size=1024")
            await ctx.send(embed=embed)
            webhook_url = config["webhook1"]
            requests.post(webhook_url, data=json.dumps(log_data), headers={"Content-Type": "application/json"})
        else:
            await ctx.send(f"Failed to process payout: {response.text}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def stats(ctx):
    response = requests.get('https://api-internal.sellauth.com/v1/shops/1700/analytics?start=2024-01-17T18:30:00.000Z&end=2025-01-21T17:19:23.861Z&excludeManual=0&excludeArchived=0&currency=USD',headers=headers,)
    data = response.json()
    total_orders = data["orders"]
    total_revenue = data["revenue"]
    total_customers = data["customers"]
    total_percentage_orders = data["ordersChange"]
    total_percentage_revenue_change = data["revenueChange"]
    total_customer_percntage_change = data["customersChange"]

    embed = discord.Embed(title="Sellauth Statistic", color=discord.Color.green())

    embed.add_field(name=f"<:stock:1322253893026971699> | Total Orders: ", value=f"{total_orders}", inline=False)
    embed.add_field(name=f"<:percentage:1331317481226113064> | Total Order Percentage: ", value=f"{total_percentage_orders}%", inline=False)
    embed.add_field(name=f"<:income:1331317848471109653> | Total Revenue: ", value=f"${total_revenue}", inline=False)
    embed.add_field(name=f"<:percentage:1331317481226113064> | Total Revenue Percentage: ", value=f"{total_percentage_revenue_change}%", inline=False)
    embed.add_field(name=f"<:customerservice:1331318192043462677> | Total Customers: ", value=f"{total_customers}", inline=False)
    embed.add_field(name=f"<:Voucher:1326159334941659157> | Total Customer Percentage: ", value=f"{total_customer_percntage_change}%", inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def purchase(ctx, couponcode, email, amount):
    productid = 51891
    json_data = {
        'product': productid,
        'coupon': couponcode,
        'email': email,
        'custom_fields': {},
        'gateway': 'LTC',
        'amount': amount,
    }

    response = requests.post('https://api-internal.sellauth.com/v1/invoice/create', json=json_data)
    if response.status_code == 200 and 'url' in response.json():
        url = response.json()['url']
        invoice_id = url.split('/')[-1]
        response2 = requests.get(f'https://api-internal.sellauth.com/v1/invoice/{invoice_id}')
        invoice_data = response2.json().get('invoice', {})
        
        eemail = invoice_data.get('email', 'N/A')
        status = invoice_data.get('status', 'N/A')
        price = invoice_data.get('price', 'N/A')
        currency = invoice_data.get('currency', 'N/A')
        LTC_address = invoice_data.get('crypto_address', 'N/A')
        LTC_amount = invoice_data.get('crypto_amount', 'N/A')

        embed = discord.Embed(title="Purchase Invoice", color=discord.Color.green())

        embed.add_field(name=f"<:identity:1326256999691845633> | Code: {couponcode}", value="", inline=False)
        embed.add_field(name=f"<:voucher:1326245770055389187> | Coupon Code: {couponcode}", value="", inline=False)
        embed.add_field(name=f"<:discount:1326159417405866047> | Discount: N/A", value="", inline=False)
        embed.add_field(name=f"<:stock:1322253893026971699> | Product: Minecraft Java & Bedrock Edition [No Name Set]", value="", inline=False)
        embed.add_field(name=f"<:email:1330232670399238235> | Email: {eemail}", value="", inline=False)
        embed.add_field(name=f"<:Voucher:1326159334941659157> | Invoice: ", value=f"[{invoice_id}](https://mralts.mysellauth.com/invoice/show/{invoice_id})", inline=False)
        embed.add_field(name=f"<a:loading8:1317014683546419331> | Status: {status}", value="", inline=False)
        embed.add_field(name=f"<:Money:1326113026184708136> | Price: ${price}", value="", inline=False)
        embed.add_field(name=f"<a:ltcan:1326108601273815071> | Currency: {currency}", value="", inline=False)
        embed.add_field(name=f"<:price:1330237249513721947> | LTC Amount: {LTC_amount}", value="", inline=False)

        ltc_address = invoice_data.get('crypto_address', '')
        if ltc_address:
            qr = qrcode.make(ltc_address)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            file = discord.File(buffer, filename="qr_code.png")
    
            view = PurchaseView(ltc_address, file)

            try:
                dm_channel = await ctx.author.create_dm()
                await dm_channel.send(embed=embed, view=view)
                await ctx.reply("I have sent you a DM with your invoice!")
            except discord.Forbidden:
                await ctx.reply("I couldn't send you a DM. Please ensure DMs are enabled for this server.")
        else:
            view = PurchaseView(None, None)
            await ctx.send(embed=embed, view=view)

    else:
        await ctx.send("Invoice creation failed.")
@bot.command()
async def process(ctx, invoice_id: str, cashapp_receipt_id: str = None):
    if ctx.author.id in bot.admins:
        print(f"User {ctx.author.name} ({ctx.author.id}) initiated a process command for invoice ID {invoice_id}.")

        try:
            invoice_id = invoice_id.split('-')[1]
            invoice_id = invoice_id.lstrip('0')
            print(f"Extracted invoice ID: {invoice_id}")
        except IndexError:
            await ctx.send("Invalid invoice ID format. Please use the format: xxxxxxxxxxxxxxxx-xxxxxxxxxxxx")
            print("Error: Invalid invoice ID format.")
            return

        shop_response = requests.get('https://api.sellauth.com/v1/shops', headers=headers)
        print(f"Shop response status code: {shop_response.status_code}")

        if shop_response.status_code == 200:
            shops = shop_response.json()

            if len(shops) > 1:
                shop_list = "\n".join([f"{idx + 1}: {shop['name']} (ID: {shop['id']})" for idx, shop in enumerate(shops)])
                await ctx.send(f"Multiple shops found:\n{shop_list}\nPlease enter the number corresponding to the desired shop.")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

                try:
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    selected_index = int(user_response.content) - 1
                    
                    if 0 <= selected_index < len(shops):
                        shop_id = shops[selected_index]['id']
                    else:
                        await ctx.send("Invalid selection. Please try again.")
                        return
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to respond. Please try again.")
                    return
            else:
                shop_id = shops[0]['id']
        else:
            await ctx.author.send("Failed to get shop ID")
            return

        process_url = f"https://api-internal.sellauth.com/v1/shops/{shop_id}/invoices/{invoice_id}/process"
        print(f"Processing URL: {process_url}")

        process_response = requests.get(process_url, headers=headers)
        print(f"Process response status code: {process_response.status_code}")

        if process_response.status_code == 200:
            await ctx.send(f"Processed {invoice_id}")
            await ctx.author.send(f"Invoice {invoice_id} processed successfully.")
            print(f"Invoice {invoice_id} processed successfully.")

        else:
            await ctx.author.send(f"Failed to process invoice {invoice_id}.")
            print(f"Error: Failed to process invoice {invoice_id}. Status code: {process_response.status_code}")
        
        log_data = {
            "content": f"User {ctx.author.name} ({ctx.author.id}) processed invoice {invoice_id}.",
            "embeds": [
                {
                    "title": "Process Command Executed",
                    "description": f"User: {ctx.author.name} ({ctx.author.id})\nInvoice ID: {invoice_id}\nProcess Status: {process_response.status_code}",
                    "color": 5814783 
                }
            ]
        }
        webhook_url = config["webhook2"]
        requests.post(webhook_url, data=json.dumps(log_data), headers={"Content-Type": "application/json"})

    else:
        print(f"User {ctx.author.name} ({ctx.author.id}) is not authorized to use this command.")
        await ctx.send("You are not authorized to use this command.")
        
        log_data = {
            "content": f"Unauthorized access attempt by {ctx.author.name} ({ctx.author.id}).",
            "embeds": [
                {
                    "title": "Unauthorized Access Attempt",
                    "description": f"User: {ctx.author.name} ({ctx.author.id}) tried to execute the process command.",
                    "color": 16711680
                }
            ]
        }
        requests.post(webhook_url, data=json.dumps(log_data), headers={"Content-Type": "application/json"})
        
@bot.command()
async def getdelivery(ctx, invoice_id):
    url = f"https://api-internal.sellauth.com/v1/invoice/{invoice_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    delivered = data.get('invoice', {}).get('delivered', None)

    if delivered:
        try:
            delivered_list = json.loads(delivered)
            delivered_str = ', '.join(delivered_list)
        except json.JSONDecodeError:
            delivered_str = "Invalid delivery format."

        file_name = f"{invoice_id}_stock_info.txt"
        with open(file_name, 'w') as file:
            file.write(f"{delivered_str}\n")

        try:
            await ctx.author.send(file=discord.File(file_name))
            await ctx.send(f"Stock information for invoice {invoice_id} has been sent to your DMs.")
        except discord.errors.Forbidden:
            await ctx.send("I can't send DMs to you. Please ensure your DMs are open.")
    else:
        await ctx.send("No stock information found for this invoice ID.")

bot.run(config["bot_token"])

