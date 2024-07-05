import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, KeyboardButton

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

class Ring:
    
    def __init__(self, start_time: str, end_time: str):
        
        self.start_time = start_time
        self.end_time = end_time
    
    def __str__(self) -> str:
        return f"{self.start_time}-{self.end_time}"

class Schedule_Save_Manager:
    def __init__(self):
        pass
    
    def __enter__(self):
        try:
            with open("rings.txt") as f:
                for line in f.readlines():
                    key, value = line.split()
                    all_rings.all_rings[key] = value
        except FileNotFoundError:
            pass
        
    def __exit__(self, _a, _b, _c):
            with open("rings.txt", 'w') as f:
                file_string = ""
                for key, value in all_rings.all_rings.items():
                    file_string += f"{key} {value}\n"
                f.write(file_string)
            
class Rings_Schedule:
    
    def __init__(self):
        self.all_rings = {}
        
all_rings = Rings_Schedule()
    
@dp.message(Command("show_rings"))    
async def show_all_rings(message: Message):
    answer_string = "Всі дзвінки:\n"
    for key, value in all_rings.all_rings.items():
        answer_string += f"{key} - {value}\n"
    await message.answer(answer_string)
        
@dp.message(Command("add_rings"))    
async def add_rings(message: Message):
    parts = message.text.split()
    if len(parts) == 3:
        key = parts[1]
        value = parts[2]
        all_rings.all_rings[key] = value
        await message.answer("OK")
    else:
        await message.answer("Тут щось не те")
        
        
@dp.message(Command("delete_rings"))
async def delete_ring(message: Message):
    parts = message.text.split()
    if len(parts) == 2:
        key = parts[1]
        if key not in all_rings.all_rings:
            await message.answer("Такої пари нема")
        else:
            del(all_rings.all_rings[key])
            await message.answer("OK")
    else:
        await message.answer("Тут щось не те")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    with Schedule_Save_Manager():
        asyncio.run(main())