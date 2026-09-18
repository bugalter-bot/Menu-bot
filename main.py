import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

import config
import database as db
from handlers import backup, categories, common, foods, random_pick, search
from middleware import AdminOnlyMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.message.middleware(AdminOnlyMiddleware())
dp.callback_query.middleware(AdminOnlyMiddleware())

dp.include_router(common.router)
dp.include_router(categories.router)
dp.include_router(foods.router)
dp.include_router(random_pick.router)
dp.include_router(search.router)
dp.include_router(backup.router)


async def health(request):
    # UptimeRobot shu endpointga ping tashlaydi
    return web.Response(text="OK")


async def on_startup(app: web.Application):
    await db.init_db()
    if config.WEBHOOK_URL:
        await bot.set_webhook(config.WEBHOOK_URL)
        logging.info("Webhook o'rnatildi: %s", config.WEBHOOK_URL)
    else:
        logging.warning("WEBHOOK_HOST berilmagan — webhook o'rnatilmadi.")


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await db.close_db()


def main():
    app = web.Application()
    app.router.add_get("/health", health)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
