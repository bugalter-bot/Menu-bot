from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import database as db
import keyboards as kb
from states import AddCategory
from utils import render

router = Router()


@router.callback_query(F.data == "show_categories")
async def show_categories(call: CallbackQuery):
    cats = await db.get_categories()
    await render(call, "📂 Bo'limlar:", kb.categories_kb(cats))
    await call.answer()


@router.callback_query(F.data.startswith("cat:"))
async def open_category(call: CallbackQuery):
    category_id = int(call.data.split(":")[1])
    cat = await db.get_category(category_id)
    if not cat:
        await call.answer("Bo'lim topilmadi", show_alert=True)
        return
    foods = await db.get_foods_by_category(category_id)
    text = f"📂 {cat['name']}\n\nTaomlar soni: {len(foods)}"
    await render(call, text, kb.category_detail_kb(category_id, foods))
    await call.answer()


@router.callback_query(F.data == "cat_add")
async def cat_add_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddCategory.waiting_name)
    await render(call, "Yangi bo'lim nomini yozing:")
    await call.answer()


@router.message(AddCategory.waiting_name)
async def cat_add_finish(message: Message, state: FSMContext):
    name = message.text.strip()
    cat = await db.add_category(name)
    await state.clear()
    if cat is None:
        await message.answer("Bu nomdagi bo'lim allaqachon bor.", reply_markup=kb.main_menu_kb())
        return
    cats = await db.get_categories()
    await message.answer(f"✅ '{name}' bo'limi qo'shildi.", reply_markup=kb.categories_kb(cats))


@router.callback_query(F.data.startswith("cat_del:"))
async def cat_del_confirm(call: CallbackQuery):
    category_id = int(call.data.split(":")[1])
    await render(
        call,
        "Bo'limni o'chirsangiz, ichidagi barcha taomlar ham o'chib ketadi. Davom etamizmi?",
        kb.confirm_kb(f"cat_del_yes:{category_id}", f"cat_del_no:{category_id}"),
    )
    await call.answer()


@router.callback_query(F.data.startswith("cat_del_yes:"))
async def cat_del_yes(call: CallbackQuery):
    category_id = int(call.data.split(":")[1])
    await db.delete_category(category_id)
    cats = await db.get_categories()
    await render(call, "🗑 Bo'lim o'chirildi.", kb.categories_kb(cats))
    await call.answer()


@router.callback_query(F.data.startswith("cat_del_no:"))
async def cat_del_no(call: CallbackQuery):
    category_id = int(call.data.split(":")[1])
    cat = await db.get_category(category_id)
    foods = await db.get_foods_by_category(category_id)
    await render(call, f"📂 {cat['name']}", kb.category_detail_kb(category_id, foods))
    await call.answer()
