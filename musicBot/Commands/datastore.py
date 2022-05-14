import asyncio

import lightbulb, hikari

plugin = lightbulb.Plugin("plugin", include_datastore=True)


@plugin.command()
@lightbulb.option(name="data", description="set to a test message", required=True)
@lightbulb.command("setdata", "Set data")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_music(ctx: lightbulb.context.Context):
    data = ctx.options.data
    plugin.d.test = data

    ctx.bot.d.data = ctx.options.data

    bData = ctx.bot.d.data

    await ctx.respond(bData)


@plugin.command()
@lightbulb.command("getdata", "Get data")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_music(ctx: lightbulb.context.Context):
    data = ctx.bot.d.bData

    await ctx.respond(f"Data = {data}")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
