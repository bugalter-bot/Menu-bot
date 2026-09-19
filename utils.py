from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup


async def render(call: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup | None = None):
    """Callback bosilganda xabarni yangilaydi.

    Agar joriy xabarni matn sifatida tahrirlab bo'lmasa (masalan, u rasm/caption
    bo'lsa yoki matn allaqachon bir xil bo'lsa), eski xabarni o'chirib, o'rniga
    yangi matnli xabar yuboradi — shunda "orqaga"/"bosh menu" kabi tugmalar
    har doim ishlaydi.
    """
    try:
        await call.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest:
        try:
            await call.message.delete()
        except TelegramBadRequest:
            pass
        await call.message.answer(text, reply_markup=reply_markup)
