from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🍽 Salom! Bu — sening shaxsiy taomlar menyung.\n\nNima qilamiz?",
        reply_markup=kb.main_menu_kb(),
    )


@router.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text("🍽 Bosh menu:", reply_markup=kb.main_menu_kb())
    except Exception:
        await call.message.answer("🍽 Bosh menu:", reply_markup=kb.main_menu_kb())
    await call.answer()
