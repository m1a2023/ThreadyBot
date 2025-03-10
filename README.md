# How to Run Telegram Bot Development Server

---

### 1) Get Telegram Bot API Key

You can obtain it from [BotFather](https://t.me/botfather) or request it from the development team.

---

### 2) Set Up Environment Variables

Ensure that your Telegram bot token is stored as an environment variable.

**On Windows (PowerShell):**

```powershell
$env:THREADY_BOT="your_bot_api_key"
```

**On Linux/macOS (Bash):**

```bash
export THREADY_BOT="your_bot_api_key"
```

---

### 3) Install Dependencies

Ensure you have Python installed, then install the required dependencies:

```bash
pip install python-telegram-bot --upgrade
```

---

### 4) Run the Bot

Pass the token explicitly:

```bash
python src/main.py $THREADY_BOT
```

Or pass token directly (recomended):

```
python src/main.py TG_API_TOKEN
```

---

### 5) Debugging Issues

- Ensure the bot token is correctly set in environment variables.
- Restart your terminal if the environment variable is not recognized.

---

### 6) Stopping the Bot

To stop the bot, use `Ctrl + C` in the terminal.
