import telegram
import asyncio
from telegram.ext import Application, CommandHandler, Updater, MessageHandler
from telegram.ext import filters
import asyncio


async def start(update, context):
   await context.bot.send_message(chat_id = update.message.chat.id, text =  "안녕하세요 \n 광운대학교 도서관 근로장학생 알림이 입니다. \n 알림이 오면 좌석번호를 확인하시고 짐을 치워주세요!")

def main():
   TOKEN = "6216322229:AAHnR_jcUgRuYEFKqK9LylAznZH_9GRaNys"
   application = Application.builder().token(TOKEN).build()
   application.add_handler(CommandHandler('start', start))
   application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), start))
   application.run_polling()
   # 2018732041_전준태_Assignment_14.py

if __name__ == "__main__":
   main()
