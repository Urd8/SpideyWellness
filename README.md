# Telegram Flowchart Bot

This Telegram bot guides users through a predefined flowchart, asking questions and providing responses based on user input.

## Features

- Multi-layer flowchart navigation
- Customizable questions and responses
- Logging of user interactions
- Data stored in a separate JSON file for easy editing

## Prerequisites

- Python 3.7+
- A Telegram Bot Token (obtain from BotFather)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Urd8/SpideyWellness.git
   cd SpideyWellness
   ```

2. Install required packages:
   ```
   pip install python-telegram-bot python-dotenv
   ```

3. Create a `.env` file in the project root and add your Telegram Bot Token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

## Usage

1. Customize the flowchart by editing `flowchart_data.json`.

2. Run the bot:
   ```
   python Bot.py
   ```

3. Start a conversation with your bot on Telegram by sending the `/start` command.

## File Structure

- `gpttest.py`: Main bot logic
- `flowchart_data.json`: Flowchart structure and content
- `.env`: Environment variables (not tracked in git)

## Customizing the Flowchart

Edit the `flowchart_data.json` file to modify the questions, options, and responses in the flowchart. The structure supports up to 4 layers of depth.

## Logging

User interactions are logged to the console. To save logs to a file, modify the logging configuration in `Bot.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
