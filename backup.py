from aiogram import F, Router
from aiogram.types import BufferedInputFile, CallbackQuery

import database as db

router = Router()


@router.callback_query(F.data == "backup")
async def backup(call: CallbackQuery):
    data = await db.export_all()
    file = BufferedInputFile(data.encode("utf-8"), filename="taomlar_backup.json")
    await call.message.answer_document(file, caption="📦 Barcha taomlarning backup fayli.")
    await call.answer()
