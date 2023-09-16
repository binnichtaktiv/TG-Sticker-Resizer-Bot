# Telegram Image Resizer Bot

A simple Telegram bot designed to automatically resize images to the correct dimensions for sending to the Sticker Bot.

## Features

- Auto-resizes images to 512x512 pixels.
- Supports processing of a single image at a time.
- Integrated error handling for Telegram API rate limits.

## Requirements

- Python 3.x
- `telebot` library: A framework for building Telegram bots.
- `PIL` (Python Imaging Library): Allows for the opening, manipulating, and saving of many different image file formats.

## Installation and Setup

1. **Python & Pip Installation**

   Ensure Python and Pip are installed. You can download Python [here](https://www.python.org/downloads/).

2. **Install Libraries**

   After installing Python and Pip, install the required libraries using:
```pip install pyTelegramBotAPI Pillow```


3. **Bot Token**

Replace `"YOUR_BOT_TOKEN_HERE"` in the script with your Telegram bot token obtained from the [@BotFather](https://t.me/botfather).

4. **Run the Bot**

Execute the bot using the command:
python <filename>.py

## Usage

- Start a conversation with the bot and send an image.
- The bot will process and return the image to you in the correct size and format.
