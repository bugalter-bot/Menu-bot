from aiogram import F, Router
from aiogram.types import CallbackQuery

import database as db
import keyboards as kb
from handlers.foods import _send_food_card

router = Router()


@router.callback_query(F.data == "random_menu")
async def random_menu(call: CallbackQuery):
    cats = await db.get_categories()
    await call.message.edit_text("🎲 Qaysi bo'limdan tanlaymiz?", reply_markup=kb.random_scope_kb(cats))
    await call.answer()


@router.callback_query(F.data.startswith("random_pick:"))
async def random_pick(call: CallbackQuery):
    scope = call.data.split(":")[1]
    category_id = None if scope == "all" else int(scope)
    food = await db.get_random_food(category_id)
    if not food:
        await call.answer("Bu bo'limda hali taom yo'q.", show_alert=True)
        return
    await call.message.delete()
    await _send_food_card(call.message, food, food["category_id"], extra_kb=kb.random_again_kb(scope))
    await call.answer()
