from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher.router import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
tg_bot_token = os.getenv('tg_bot_token')
exchange_rates_api_token= os.getenv('exchange_rates_api_token')


# Словарь флагов по кодам валют
currency_flags = {
    'AED': '🇦🇪', 'AFN': '🇦🇫', 'ALL': '🇦🇱', 'AMD': '🇦🇲', 'ANG': '🇳🇱', 'AOA': '🇦🇴',
    'ARS': '🇦🇷', 'AUD': '🇦🇺', 'AWG': '🇦🇼', 'AZN': '🇦🇿', 'BAM': '🇧🇦', 'BBD': '🇧🇧',
    'BDT': '🇧🇩', 'BGN': '🇧🇬', 'BHD': '🇧🇭', 'BIF': '🇧🇮', 'BMD': '🇧🇲', 'BND': '🇧🇳',
    'BOB': '🇧🇴', 'BRL': '🇧🇷', 'BSD': '🇧🇸', 'BTC': '₿', 'BTN': '🇧🇹', 'BWP': '🇧🇼',
    'BYN': '🇧🇾', 'BYR': '🇧🇾', 'BZD': '🇧🇿', 'CAD': '🇨🇦', 'CDF': '🇨🇩', 'CHF': '🇨🇭',
    'CLP': '🇨🇱', 'CNY': '🇨🇳', 'COP': '🇨🇴', 'CRC': '🇨🇷', 'CUC': '🇨🇺', 'CUP': '🇨🇺',
    'CZK': '🇨🇿', 'DJF': '🇩🇯', 'DKK': '🇩🇰', 'DOP': '🇩🇴', 'DZD': '🇩🇿', 'EGP': '🇪🇬',
    'ERN': '🇪🇷', 'ETB': '🇪🇹', 'EUR': '🇪🇺', 'FJD': '🇫🇯', 'FKP': '🇫🇰', 'GBP': '🇬🇧',
    'GEL': '🇬🇪', 'GGP': '🇬🇬', 'GHS': '🇬🇭', 'GIP': '🇬🇮', 'GMD': '🇬🇲', 'GNF': '🇬🇳',
    'GTQ': '🇬🇹', 'GYD': '🇬🇾', 'HKD': '🇭🇰', 'HNL': '🇭🇳', 'HRK': '🇭🇷', 'HTG': '🇭🇹',
    'HUF': '🇭🇺', 'IDR': '🇮🇩', 'ILS': '🇮🇱', 'IMP': '🇮🇲', 'INR': '🇮🇳', 'IQD': '🇮🇶',
    'IRR': '🇮🇷', 'ISK': '🇮🇸', 'JEP': '🇯🇪', 'JMD': '🇯🇲', 'JOD': '🇯🇴', 'JPY': '🇯🇵',
    'KES': '🇰🇪', 'KGS': '🇰🇬', 'KHR': '🇰🇭', 'KMF': '🇰🇲', 'KPW': '🇰🇵', 'KRW': '🇰🇷',
    'KWD': '🇰🇼', 'KYD': '🇰🇾', 'KZT': '🇰🇿', 'LAK': '🇱🇦', 'LBP': '🇱🇧', 'LKR': '🇱🇰',
    'LRD': '🇱🇷', 'LSL': '🇱🇸', 'LTL': '🇱🇹', 'LVL': '🇱🇻', 'LYD': '🇱🇾', 'MAD': '🇲🇦',
    'MDL': '🇲🇩', 'MGA': '🇲🇬', 'MKD': '🇲🇰', 'MMK': '🇲🇲', 'MNT': '🇲🇳', 'MOP': '🇲🇴',
    'MRO': '🇲🇷', 'MUR': '🇲🇺', 'MVR': '🇲🇻', 'MWK': '🇲🇼', 'MXN': '🇲🇽', 'MYR': '🇲🇾',
    'MZN': '🇲🇿', 'NAD': '🇳🇦', 'NGN': '🇳🇬', 'NIO': '🇳🇮', 'NOK': '🇳🇴', 'NPR': '🇳🇵',
    'NZD': '🇳🇿', 'OMR': '🇴🇲', 'PAB': '🇵🇦', 'PEN': '🇵🇪', 'PGK': '🇵🇬', 'PHP': '🇵🇭',
    'PKR': '🇵🇰', 'PLN': '🇵🇱', 'PYG': '🇵🇾', 'QAR': '🇶🇦', 'RON': '🇷🇴', 'RSD': '🇷🇸',
    'RUB': '🇷🇺', 'RWF': '🇷🇼', 'SAR': '🇸🇦', 'SBD': '🇸🇧', 'SCR': '🇸🇨', 'SDG': '🇸🇩',
    'SEK': '🇸🇪', 'SGD': '🇸🇬', 'SHP': '🇸🇭', 'SLL': '🇸🇱', 'SOS': '🇸🇴', 'SRD': '🇸🇷',
    'STD': '🇸🇹', 'SVC': '🇸🇻', 'SYP': '🇸🇾', 'SZL': '🇸🇿', 'THB': '🇹🇭', 'TJS': '🇹🇯',
    'TMT': '🇹🇲', 'TND': '🇹🇳', 'TOP': '🇹🇴', 'TRY': '🇹🇷', 'TTD': '🇹🇹', 'TWD': '🇹🇼',
    'TZS': '🇹🇿', 'UAH': '🇺🇦', 'UGX': '🇺🇬', 'USD': '🇺🇸', 'UYU': '🇺🇾', 'UZS': '🇺🇿',
    'VEF': '🇻🇪', 'VND': '🇻🇳', 'VUV': '🇻🇺', 'WST': '🇼🇸', 'XAF': '🇨🇲', 'XCD': '🇰🇳',
    'XOF': '🇸🇳', 'XPF': '🇵🇫', 'YER': '🇾🇪', 'ZAR': '🇿🇦', 'ZMK': '🇿🇲', 'ZMW': '🇿🇲',
    'ZWL': '🇿🇼'
}

bot = Bot(token=tg_bot_token)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Хранение временного состояния выбора валюты
user_state = {}

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне коды двух валют (например, USD и RUB) или выбери из списка.\n"
                        "Чтобы увидеть список поддерживаемых валют с флагами, отправь команду /currencies")

@router.message(Command("currencies"))
async def list_currencies(message: Message):
    try:
        # Запрос к API для получения курсов валют относительно евро
        url = f"https://api.exchangeratesapi.io/v1/latest?access_key={exchange_rates_api_token}"
        r = requests.get(url)
        data = r.json()

        if not data.get("success", False):
            error_info = data.get("error", {}).get("info", "Неизвестная ошибка")
            await message.reply(f"Ошибка: {error_info}")
            return

        # Получение списка поддерживаемых валют
        available_currencies = list(data["rates"].keys())
        available_currencies.sort()

        # Создание клавиатуры с кнопками
        keyboard = InlineKeyboardBuilder()
        for currency in available_currencies:
            flag = currency_flags.get(currency, "")
            keyboard.button(text=f"{flag} {currency}", callback_data=currency)

        # Настройка клавиатуры: размещение кнопок по 3 в строке
        keyboard.adjust(3)
        await message.reply("Выберите первую валюту или введите её вручную:", reply_markup=keyboard.as_markup())

    except Exception as e:
        await message.reply(f"\U00002620 Произошла ошибка при получении списка валют \U00002620\nОшибка: {str(e)}")

@router.callback_query()
async def handle_currency_selection(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    # Если это первый выбор, запоминаем его и предлагаем выбрать вторую валюту
    if user_id not in user_state:
        user_state[user_id] = {'base_currency': callback_query.data}
        await callback_query.message.edit_text(f"Вы выбрали первую валюту: {callback_query.data}. Теперь выберите вторую валюту или введите её вручную.")

        url = f"https://api.exchangeratesapi.io/v1/latest?access_key={exchange_rates_api_token}"
        r = requests.get(url)
        data = r.json()

        available_currencies = list(data["rates"].keys())
        available_currencies.sort()

        keyboard = InlineKeyboardBuilder()
        for currency in available_currencies:
            flag = currency_flags.get(currency, "")
            keyboard.button(text=f"{flag} {currency}", callback_data=currency)

        keyboard.adjust(3)
        await callback_query.message.answer("Выберите вторую валюту или введите её вручную:", reply_markup=keyboard.as_markup())
    else:
        base_currency = user_state[user_id]['base_currency']
        target_currency = callback_query.data

        await process_currency_exchange(callback_query.message, base_currency, target_currency)

        # Очищаем состояние пользователя
        del user_state[user_id]

    await callback_query.answer()

@router.message()
async def handle_text_input(message: Message):
    user_id = message.from_user.id

    # Проверка, ввёл ли пользователь первую валюту
    if user_id not in user_state:
        user_state[user_id] = {'base_currency': message.text.strip().upper()}
        await message.reply(f"Вы ввели первую валюту: {message.text.strip().upper()}. Теперь введите вторую валюту или выберите её из списка.")
    else:
        base_currency = user_state[user_id]['base_currency']
        target_currency = message.text.strip().upper()

        await process_currency_exchange(message, base_currency, target_currency)

        # Очищаем состояние пользователя
        del user_state[user_id]

async def process_currency_exchange(message: Message, base_currency: str, target_currency: str):
    try:
        # Запрашиваем курс обмена
        url = f"https://api.exchangeratesapi.io/v1/latest?access_key={exchange_rates_api_token}"
        r = requests.get(url)
        data = r.json()

        rate_base_to_eur = data["rates"].get(base_currency)
        rate_target_to_eur = data["rates"].get(target_currency)

        if rate_base_to_eur and rate_target_to_eur:
            exchange_rate = rate_target_to_eur / rate_base_to_eur
            await message.reply(f"Курс {base_currency} к {target_currency} на сегодня: {exchange_rate}")
        else:
            await message.reply(f"Не удалось найти курс обмена для {base_currency} или {target_currency}")
    except Exception as e:
        await message.reply(f"\U00002620 Произошла ошибка при получении курса валют \U00002620\nОшибка: {str(e)}")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
