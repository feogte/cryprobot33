import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CARD_NUMBER,
    REVIEWS_CHANNEL,
    SUPPORT_USERNAME
)

from keyboards import (
    main_menu,
    crypto_menu,
    reviews_button,
    support_button,
    admin_order_buttons
)

from database import (
    create_db,
    add_order,
    add_check,
    update_status,
    get_order,
    get_stats
)

from prices import get_crypto_price


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# временное хранение выбранной крипты
user_choice = {}


# ======================================
# START
# ======================================

@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Здесь вы можете купить криптовалюту.",
        reply_markup=main_menu
    )


# ======================================
# ПОКУПКА КРИПТЫ
# ======================================

@dp.message(F.text == "💰 Купить криптовалюту")
async def buy_crypto(message: Message):

    await message.answer(
        "Выберите криптовалюту:",
        reply_markup=crypto_menu
    )


# ======================================
# USDT
# ======================================

@dp.callback_query(F.data == "buy_usdt")
async def buy_usdt(callback: CallbackQuery):

    user_choice[callback.from_user.id] = "USDT"

    price = await get_crypto_price("USDT")

    await callback.message.answer(
        f"💵 USDT\n\n"
        f"Текущий курс:\n"
        f"1 USDT = {price}₽\n\n"
        f"Напишите количество USDT:"
    )

    await callback.answer()


# ======================================
# GRAM
# ======================================

@dp.callback_query(F.data == "buy_gram")
async def buy_gram(callback: CallbackQuery):

    user_choice[callback.from_user.id] = "GRAM"

    price = await get_crypto_price("GRAM")

    await callback.message.answer(
        f"💎 GRAM\n\n"
        f"Средний курс:\n"
        f"1 GRAM = {price}₽\n\n"
        f"Напишите количество GRAM:"
    )

    await callback.answer()


# ======================================
# ВВОД КОЛИЧЕСТВА
# ======================================

@dp.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def amount_handler(message: Message):

    user_id = message.from_user.id

    if user_id not in user_choice:
        return


    crypto = user_choice[user_id]

    amount = float(message.text)

    price = await get_crypto_price(crypto)

    total = round(amount * price, 2)


    order_id = add_order(
        user_id,
        message.from_user.username,
        crypto,
        amount,
        total
    )


    await message.answer(
        f"💳 К оплате:\n\n"
        f"{total}₽\n\n"
        f"Переведите сумму на карту:\n"
        f"{CARD_NUMBER}\n\n"
        f"После оплаты отправьте чек сюда."
    )


# ======================================
# ЧЕК
# ======================================

@dp.message(F.photo)
async def check_handler(message: Message):

    user_id = message.from_user.id

    order = get_last_user_order(user_id)


    if not order:

        await message.answer(
            "❌ Сначала создайте заявку на покупку."
        )
        return


    order_id = order[0]


    add_check(
        order_id,
        message.photo[-1].file_id
    )


    await message.answer(
        "✅ Чек получен.\n\n"
        "Заявка отправлена владельцу.\n"
        "Ожидайте одобрения."
    )


    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=(
            "🔔 Новая заявка!\n\n"
            f"ID заявки: {order_id}\n"
            f"Пользователь: @{message.from_user.username}\n"
            f"Криптовалюта: {order[3]}\n"
            f"Количество: {order[4]}\n"
            f"Сумма: {order[5]}₽"
        ),
        reply_markup=admin_order_buttons(order_id)
    )


# ======================================
# ПОДДЕРЖКА
# ======================================

@dp.message(F.text == "🆘 Поддержка")
async def support(message: Message):

    await message.answer(
        "Нажмите на кнопку ниже, "
        "чтобы написать в поддержку.",
        reply_markup=support_button(
            SUPPORT_USERNAME
        )
    )
  
# ======================================
# АДМИН СТАТИСТИКА
# ======================================

@dp.message(F.text == "/stats")
async def stats(message: Message):

    if message.from_user.id != ADMIN_ID:
        return


    count = get_stats()

    await message.answer(
        f"📊 Всего заявок: {count}"
    )


# ======================================
# ЗАПУСК
# ======================================

async def main():

    create_db()

    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())
