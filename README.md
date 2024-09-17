# Telegram Bot: main_exchangerates.py

This Telegram bot allows users to get current exchange rates between different currencies. The bot provides an easy-to-use interface to select currencies either from a list or by manually entering currency codes.

## Features

- **Currency Selection:** Users can choose currencies from a list with country flags or input currency codes manually.
- **Exchange Rate Display:** The bot fetches the latest exchange rates and displays the conversion rate between the selected currencies.
- **Error Handling:** The bot handles errors such as API request failures or invalid currency codes.

## Setup

### Prerequisites

- A Telegram bot token (You can create a bot and get the token using [BotFather](https://core.telegram.org/bots#botfather)).
- An API key from [ExchangeRatesAPI](https://exchangeratesapi.io/) to fetch the latest exchange rates.

Create a .env file in the root directory of the project and add your bot token and API key:

tg_bot_token=YOUR_TELEGRAM_BOT_TOKEN
exchange_rates_api_token=YOUR_EXCHANGE_RATES_API_TOKEN

Usage
Start the Bot: Send /start to the bot in Telegram to start using it.
Get Supported Currencies: Send /currencies to see a list of supported currencies with flags.
Get Exchange Rate: You can either select currencies from the list or enter their codes manually (e.g., USD and RUB).

# Telegram Bot: main_weather_tg_bot.py

# Telegram Weather Bot

This Telegram bot provides weather information for a specified city. Users can send the bot the name of a city, and the bot will respond with the current weather, including temperature, humidity, wind speed, and other relevant details.

## Features

- **City Weather:** Get the current weather for any city by simply sending its name.
- **Detailed Weather Report:** The bot provides temperature, feels-like temperature, weather conditions with icons, humidity, pressure, wind speed, sunrise and sunset times, and the length of the day.
- **Error Handling:** The bot provides helpful error messages if the city is not found or if there's an issue with the request.

## Setup

### Prerequisites

- A Telegram bot token (You can create a bot and get the token using [BotFather](https://core.telegram.org/bots#botfather)).
- An API key from [OpenWeatherMap](https://openweathermap.org/) to fetch weather data.

tg_bot_token=YOUR_TELEGRAM_BOT_TOKEN
open_weather_token=YOUR_OPENWEATHER_API_KEY

Usage
Start the Bot: Send /start to the bot in Telegram to start using it.
Get Weather: Send the name of a city (e.g., "Moscow" or "New York"), and the bot will reply with the current weather in that city.
