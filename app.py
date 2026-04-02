import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

ALLOWED_USER_ID = 1436611268625563681

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="restock", description="Restock an item")
@app_commands.describe(
    item_name="Name of the item",
    item_image="Image URL",
    item_price="Price of the item",
    item_stock="Stock amount"
)
async def restock(interaction: discord.Interaction, item_name: str, item_image: str, item_price: str, item_stock: int):
    
    if interaction.user.id != ALLOWED_USER_ID:
        await interaction.response.send_message("❌ You are not allowed.", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"{item_name} Restocked",
        description=f"We restocked **{item_name}**. Purchase instantly\n\n🛒 **Buy Now**",
        color=discord.Color.green()
    )

    embed.add_field(name="Item", value=item_name, inline=True)
    embed.add_field(name="Price", value=f"${item_price}", inline=True)
    embed.add_field(name="Stock", value=str(item_stock), inline=True)

    embed.set_image(url=item_image)
    embed.set_footer(text="Stock Updated")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="review", description="Send a review")
@app_commands.describe(
    rating="Rating out of 5",
    feedback="Feedback message",
    item="Item name"
)
async def review(interaction: discord.Interaction, rating: int, feedback: str, item: str):

    stars = "⭐" * max(1, min(rating, 5))

    embed = discord.Embed(
        title="New Feedback",
        description="You have just received a new feedback!",
        color=discord.Color.blurple()
    )

    embed.add_field(name="Rating", value=stars, inline=False)
    embed.add_field(name="Feedback", value=feedback, inline=False)
    embed.add_field(name="Item", value=item, inline=False)

    embed.set_footer(text="Customer Review")

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)