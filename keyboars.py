from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# ======================================
# ГЛАВНОЕ МЕНЮ
# ======================================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💰 Купить криптовалюту")
        ],
        [
            KeyboardButton(text="⭐ Отзывы"),
            KeyboardButton(text="🆘 Поддержка")
        ]
    ],
    resize_keyboard=True
)


# ======================================
# ВЫБОР КРИПТОВАЛЮТЫ
# ======================================

crypto_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💵 USDT",
                callback_data="buy_usdt"
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 GRAM",
                callback_data="buy_gram"
            )
        ]
    ]
)


# ======================================
# КНОПКА ОТЗЫВОВ
# Ссылка берется из config.py
# ======================================

def reviews_button(channel):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐ Канал с отзывами",
                    url=channel
                )
            ]
        ]
    )


# ======================================
# КНОПКА ПОДДЕРЖКИ
# ======================================

def support_button(username):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🆘 Написать в поддержку",
                    url=f"https://t.me/{username.replace('@','')}"
                )
            ]
        ]
    )


# ======================================
# КНОПКИ АДМИНА
# ======================================

def admin_order_buttons(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Одобрить",
                    callback_data=f"approve_{order_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{order_id}"
                )
            ]
        ]
    )
