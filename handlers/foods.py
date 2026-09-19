from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import render

import database as db
import keyboards as kb
from states import AddFood, EditFood

router = Router()


async def _send_food_card(target, food, category_id, extra_kb=None):
    """target — Message (answer/answer_photo qila oladigan) obyekt."""
    text = f"🍲 <b>{food['name']}</b>"
    if food["recipe"]:
        text += f"\n\n📝 {food['recipe']}"
    markup = extra_kb or kb.food_detail_kb(food["id"], category_id)
    if food["image_file_id"]:
        await target.answer_photo(food["image_file_id"], caption=text, reply_markup=markup)
    else:
        await target.answer(text, reply_markup=markup)


# ---------- ro'yxatlar ----------

@router.callback_query(F.data == "show_all_foods")
async def show_all_foods(call: CallbackQuery):
    foods = await db.get_all_foods()
    if not foods:
        await call.answer("Hali taom yo'q.", show_alert=True)
        return
    await render(call, f"📋 Hammasi ({len(foods)} ta):", kb.all_foods_kb(foods))
    await call.answer()


@router.callback_query(F.data.startswith("food:"))
async def show_food(call: CallbackQuery):
    food_id = int(call.data.split(":")[1])
    food = await db.get_food(food_id)
    if not food:
        await call.answer("Taom topilmadi", show_alert=True)
        return
    await call.message.delete()
    await _send_food_card(call.message, food, food["category_id"])
    await call.answer()


# ---------- taom qo'shish (FSM) ----------

@router.callback_query(F.data.startswith("food_add:"))
async def food_add_start(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    await state.update_data(category_id=category_id)
    await state.set_state(AddFood.waiting_name)
    await call.message.edit_text("Taom nomini yozing:")
    await call.answer()


@router.message(AddFood.waiting_name)
async def food_add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddFood.waiting_image)
    await message.answer("Rasm yuboring (yoki o'tkazib yuboring):", reply_markup=kb.skip_kb())


@router.message(AddFood.waiting_image, F.photo)
async def food_add_image(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(image_file_id=file_id)
    await state.set_state(AddFood.waiting_recipe)
    await message.answer("Retseptni yozing (yoki o'tkazib yuboring):", reply_markup=kb.skip_kb())


@router.callback_query(AddFood.waiting_image, F.data == "skip")
async def food_add_image_skip(call: CallbackQuery, state: FSMContext):
    await state.update_data(image_file_id=None)
    await state.set_state(AddFood.waiting_recipe)
    await call.message.edit_text("Retseptni yozing (yoki o'tkazib yuboring):", reply_markup=kb.skip_kb())
    await call.answer()


async def _finish_add_food(state: FSMContext):
    data = await state.get_data()
    food = await db.add_food(
        data["category_id"], data["name"], data.get("image_file_id"), data.get("recipe")
    )
    await state.clear()
    return food, data["category_id"]


@router.message(AddFood.waiting_recipe)
async def food_add_recipe(message: Message, state: FSMContext):
    await state.update_data(recipe=message.text.strip())
    food, category_id = await _finish_add_food(state)
    foods = await db.get_foods_by_category(category_id)
    await message.answer(
        f"✅ '{food['name']}' qo'shildi.",
        reply_markup=kb.category_detail_kb(category_id, foods),
    )


@router.callback_query(AddFood.waiting_recipe, F.data == "skip")
async def food_add_recipe_skip(call: CallbackQuery, state: FSMContext):
    await state.update_data(recipe=None)
    food, category_id = await _finish_add_food(state)
    foods = await db.get_foods_by_category(category_id)
    await call.message.edit_text(
        f"✅ '{food['name']}' qo'shildi.",
        reply_markup=kb.category_detail_kb(category_id, foods),
    )
    await call.answer()


# ---------- taom o'chirish ----------

@router.callback_query(F.data.startswith("food_del:"))
async def food_del_confirm(call: CallbackQuery):
    food_id = int(call.data.split(":")[1])
    await call.message.answer(
        "Rostdan ham o'chirilsinmi?",
        reply_markup=kb.confirm_kb(f"food_del_yes:{food_id}", f"food_del_no:{food_id}"),
    )
    await call.answer()


@router.callback_query(F.data.startswith("food_del_yes:"))
async def food_del_yes(call: CallbackQuery):
    food_id = int(call.data.split(":")[1])
    food = await db.get_food(food_id)
    category_id = food["category_id"]
    await db.delete_food(food_id)
    foods = await db.get_foods_by_category(category_id)
    await call.message.edit_text("🗑 Taom o'chirildi.")
    await call.message.answer("📂 Bo'lim:", reply_markup=kb.category_detail_kb(category_id, foods))
    await call.answer()


@router.callback_query(F.data.startswith("food_del_no:"))
async def food_del_no(call: CallbackQuery):
    await call.message.edit_text("Bekor qilindi.")
    await call.answer()


# ---------- taomni tahrirlash ----------

@router.callback_query(F.data.startswith("edit_name:"))
async def edit_name_start(call: CallbackQuery, state: FSMContext):
    food_id = int(call.data.split(":")[1])
    await state.update_data(food_id=food_id)
    await state.set_state(EditFood.waiting_new_name)
    await call.message.answer("Yangi nomini yozing:")
    await call.answer()


@router.message(EditFood.waiting_new_name)
async def edit_name_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.update_food_field(data["food_id"], "name", message.text.strip())
    food = await db.get_food(data["food_id"])
    await state.clear()
    await message.answer("✅ Nomi yangilandi.")
    await _send_food_card(message, food, food["category_id"])


@router.callback_query(F.data.startswith("edit_image:"))
async def edit_image_start(call: CallbackQuery, state: FSMContext):
    food_id = int(call.data.split(":")[1])
    await state.update_data(food_id=food_id)
    await state.set_state(EditFood.waiting_new_image)
    await call.message.answer("Yangi rasmni yuboring:")
    await call.answer()


@router.message(EditFood.waiting_new_image, F.photo)
async def edit_image_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    file_id = message.photo[-1].file_id
    await db.update_food_field(data["food_id"], "image_file_id", file_id)
    food = await db.get_food(data["food_id"])
    await state.clear()
    await message.answer("✅ Rasm yangilandi.")
    await _send_food_card(message, food, food["category_id"])


@router.callback_query(F.data.startswith("edit_recipe:"))
async def edit_recipe_start(call: CallbackQuery, state: FSMContext):
    food_id = int(call.data.split(":")[1])
    await state.update_data(food_id=food_id)
    await state.set_state(EditFood.waiting_new_recipe)
    await call.message.answer("Yangi retseptni yozing:")
    await call.answer()


@router.message(EditFood.waiting_new_recipe)
async def edit_recipe_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.update_food_field(data["food_id"], "recipe", message.text.strip())
    food = await db.get_food(data["food_id"])
    await state.clear()
    await message.answer("✅ Retsept yangilandi.")
    await _send_food_card(message, food, food["category_id"])
