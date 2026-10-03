# Telegram Currency Price Bot

A Python-based Telegram bot that collects free-market currency prices from multiple online sources and provides users with a consolidated price using the median of available values.

The bot supports multiple currencies, displays the price reported by each source, and calculates a median value to reduce the effect of inconsistent or anomalous source prices.

## Features

* 💵 Support for multiple currencies:

  * USD
  * EUR
  * GBP
  * AED
* 🪙 Support for selected coin and gold prices
* 🌐 Collects prices from multiple online sources
* 📊 Calculates the median price from available sources
* ⏱️ Displays the time each source responded
* ❌ Handles unavailable sources without stopping the entire request
* 🎛️ Telegram inline keyboard for easier interaction
* ⚡ Uses asynchronous execution to fetch prices from multiple sources efficiently
* ☁️ Deployed using a Telegram webhook on Render
* 🔐 Bot token is stored as an environment variable rather than being committed to the repository

## How It Works

When a user requests a currency price, the bot sends requests to multiple price sources.

For example:

```text
                    /price usd
                         │
                         ▼
                  ┌─────────────┐
                  │ Telegram Bot │
                  └──────┬──────┘
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           TGJU       AlanChand     Bitpin
             │           │           │
             └───────────┼───────────┘
                         ▼
                 Available prices
                         │
                         ▼
                      Median
                         │
                         ▼
                    Telegram
                         │
                         ▼
                       User
```

If one of the sources is unavailable, the bot uses the prices returned by the remaining sources.

## Example

A request such as:

```text
/price usd
```

can produce a response containing:

```text
TGJU       → 252,620
AlanChand  → 253,300
Bitpin     → 253,000

Median     → 253,000
```

The exact values depend on the current market and source availability.

## Technologies

* **Python**
* **python-telegram-bot**
* **asyncio**
* **Requests**
* **BeautifulSoup**
* **Git / GitHub**
* **Render**

## Project Structure

```text
telegram-dollar-bot/
│
├── main.py
├── requirements.txt
├── .gitignore
│
├── sources/
│   ├── ...
│   └── ...
│
└── README.md
```

The `sources` package contains the individual price-fetching implementations, while `main.py` handles the Telegram bot and coordinates the returned data.

## Asynchronous Price Collection

The bot uses Python's `asyncio` to handle multiple price requests efficiently.

Because some source functions use synchronous HTTP requests, `asyncio.to_thread()` is used to execute them without blocking the bot's main asynchronous flow.

Multiple requests can then be started using `asyncio.gather()`.

Conceptually:

```python
results = await asyncio.gather(
    asyncio.to_thread(source_1.get_price, currency),
    asyncio.to_thread(source_2.get_price, currency),
    asyncio.to_thread(source_3.get_price, currency)
)
```

This allows the bot to collect prices from multiple sources without waiting for each source to finish before starting the next one.

## Environment Variables

Sensitive configuration is kept outside the source code.

The bot uses environment variables such as:

```text
BOT_TOKEN
BOT_MODE
RENDER_URL
PORT
```

For local development, the bot can run in polling mode.

For deployment, it can run in webhook mode.

Example:

```text
BOT_MODE=polling
```

or:

```text
BOT_MODE=webhook
```

The Telegram bot token should never be committed to GitHub.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/parsashkv/telegram-dollar-bot.git
cd telegram-dollar-bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the bot token

Set the required environment variables locally.

For example:

```text
BOT_TOKEN=your_telegram_bot_token
BOT_MODE=polling
```

Do not commit your actual token to GitHub.

### 5. Run the bot

```bash
python main.py
```

## Deployment

The bot is deployed as a Web Service on Render.

In webhook mode, Telegram sends incoming updates directly to the deployed application instead of the application repeatedly polling Telegram for new updates.

The deployment uses:

```text
BOT_MODE=webhook
```

and the Render service URL is provided through:

```text
RENDER_URL
```

The application also uses the `PORT` environment variable provided by the hosting platform.

## Security

Sensitive files and local configuration are excluded from Git using `.gitignore`.

Examples include:

```text
.venv/
__pycache__/
*.pyc
config.py
.env
.idea/
```

The Telegram bot token is provided through an environment variable and is not stored in the GitHub repository.

## Current Status

The bot is deployed and running through Telegram webhook infrastructure.

Repository:

https://github.com/parsashkv/telegram-dollar-bot
