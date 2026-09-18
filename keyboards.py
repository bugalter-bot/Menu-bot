from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def main_menu_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📂 Bo'limlar", callback_data="show_categories")
    b.button(text="📋 Hammasi", callback_data="show_all_foods")
    b.button(text="🎲 Random", callback_data="random_menu")
    b.button(text="🔍 Qidirish", callback_data="search_start")
    b.button(text="📦 Backup", callback_data="backup")
    b.button(text="➕ Bo'lim qo'shish", callback_data="cat_add")
    b.adjust(2, 2, 2)
    return b.as_markup()


def categories_kb(categories, with_add=True) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for c in categories:
        b.button(text=c["name"], callback_data=f"cat:{c['id']}")
    if with_add:
        b.button(text="➕ Bo'lim qo'shish", callback_data="cat_add")
    b.button(text="⬅️ Bosh menu", callback_data="back_main")
    b.adjust(1)
    return b.as_markup()


def category_detail_kb(category_id: int, foods) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for f in foods:
        b.button(text=f["name"], callback_data=f"food:{f['id']}")
    b.button(text="➕ Taom qo'shish", callback_data=f"food_add:{category_id}")
    b.button(text="🗑 Bo'limni o'chirish", callback_data=f"cat_del:{category_id}")
    b.button(text="⬅️ Bo'limlar", callback_data="show_categories")
    b.adjust(1)
    return b.as_markup()


def food_detail_kb(food_id: int, category_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✏️ Nomi", callback_data=f"edit_name:{food_id}")
    b.button(text="🖼 Rasmi", callback_data=f"edit_image:{food_id}")
    b.button(text="📝 Retsepti", callback_data=f"edit_recipe:{food_id}")
    b.button(text="🗑 O'chirish", callback_data=f"food_del:{food_id}")
    b.button(text="⬅️ Orqaga", callback_data=f"cat:{category_id}")
    b.adjust(3, 1, 1)
    return b.as_markup()


def confirm_kb(yes_cb: str, no_cb: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Ha", callback_data=yes_cb)
    b.button(text="❌ Yo'q", callback_data=no_cb)
    b.adjust(2)
    return b.as_markup()


def skip_kb(callback_data: str = "skip") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="⏭ O'tkazib yuborish", callback_data=callback_data)
    return b.as_markup()


def random_scope_kb(categories) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🎲 Barchasidan", callback_data="random_pick:all")
    for c in categories:
        b.button(text=c["name"], callback_data=f"random_pick:{c['id']}")
    b.button(text="⬅️ Bosh menu", callback_data="back_main")
    b.adjust(1)
    return b.as_markup()


def random_again_kb(scope) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🎲 Yana", callback_data=f"random_pick:{scope}")
    b.button(text="⬅️ Bosh menu", callback_data="back_main")
    b.adjust(1)
    return b.as_markup()


def all_foods_kb(foods) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for f in foods:
        b.button(text=f["name"], callback_data=f"food:{f['id']}")
    b.button(text="⬅️ Bosh menu", callback_data="back_main")
    b.adjust(1)
    return b.as_markup()
