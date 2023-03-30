import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.bot_db import sql_command_all_id
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from config import bot, ADMINS


async def hb(bot: Bot):
    user_ids = await sql_command_all_id()
    for user_ids in user_ids:
        await bot.send_message(user_ids[0], "Happy birthday!")


async def send_message_date(bot: Bot):
    await bot.send_message(ADMINS[0], "DATE TRIGGER!")


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone='Asia/Bishkek')
    scheduler.add_job(
        hb,
        trigger=DateTrigger(
            run_date=datetime.datetime(year=datetime.datetime.now().year, month=8, day=4, hour=0, minute=0)
        ),
        kwargs={"bot": bot},
    )

    scheduler.start()

