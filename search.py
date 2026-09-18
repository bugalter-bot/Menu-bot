from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import database as db
import keyboards as kb
from states import SearchFood

router = Router()


@router.callback_query(F.data == "search_start")
async def search_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFood.waiting_query)
    await call.message.edit_text("🔍 Qidirilayotgan taom nomini yozing:")
    await call.answer()


@router.message(SearchFood.waiting_query)
async def search_run(message: Message, state: FSMContext):
    query = message.text.strip()
    results = await db.search_foods(query)
    await state.clear()
    if not results:
        await message.answer("Hech narsa topilmadi.", reply_markup=kb.main_menu_kb())
        return
    await message.answer(
        f"🔍 Topildi: {len(results)} ta", reply_markup=kb.all_foods_kb(results)
    )
