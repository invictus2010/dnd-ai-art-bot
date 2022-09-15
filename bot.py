from fileinput import filename
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image
import warnings
import os
import io
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

load_dotenv()

stability_api = client.StabilityInference(
    key=os.environ['STABLE_DIFFUSION_TOKEN'],
    verbose=True,
)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    description="Make art.",
    intents=intents,
)


@bot.command()
async def dream(ctx, *, prompt):
    msg = await ctx.send(f"“{prompt}”\n> Generating...")
    answers = stability_api.generate(prompt=prompt)
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                msg = await ctx.send(
                    "You have triggered the filter, please try again")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                arr = io.BytesIO(artifact.binary)
                img.save(arr, format='PNG')
                arr.seek(0)
                file = discord.File(arr, filename='art.png')
                await msg.edit(content=f"“{prompt}” \n")
                await ctx.send(file=file)


bot.run(os.environ["DISCORD_TOKEN"])
