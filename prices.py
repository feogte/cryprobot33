import aiohttp


# ======================================
# ПОЛУЧЕНИЕ КУРСА USDT
# ======================================

async def get_usdt_price():

    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=tether"
            "&vs_currencies=rub"
        )

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                data = await response.json()

                price = data["tether"]["rub"]

                return round(price, 2)


    except Exception:

        # Если API временно не работает
        return None



# ======================================
# ПОЛУЧЕНИЕ СРЕДНЕЙ ЦЕНЫ GRAM
# ======================================

async def get_gram_price():

    # Средняя цена GRAM
    # Можно изменить позже вручную

    average_price = 20

    return average_price



# ======================================
# ПОЛУЧЕНИЕ ЛЮБОГО КУРСА
# ======================================

async def get_crypto_price(crypto):

    if crypto == "USDT":
        return await get_usdt_price()


    elif crypto == "GRAM":
        return await get_gram_price()


    return None
