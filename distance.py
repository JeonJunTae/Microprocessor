import RPi.GPIO as GPIO
import time
import asyncio
import telegram

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

TOKEN = "6216322229:AAHnR_jcUgRuYEFKqK9LylAznZH_9GRaNys"
CHAT_ID = 6027949960

bot = telegram.Bot(token = TOKEN)

def measure_distance():
   GPIO.output(TRIG, True)
   time.sleep(0.00001)
   GPIO.output(TRIG, False)
   start_time = time.time()
   stop_time = time.time()
   while GPIO.input(ECHO) == 0:
      start_time = time.time()
   while GPIO.input(ECHO) == 1:
      stop_time = time.time()
   duration = stop_time - start_time
   distance = duration * 34300 / 2
   return distance
#https://rasino.tistory.com/349

async def main():
   try:
      while True:
         dist = measure_distance()
         print("Distance : {:.2f}cm".format(dist))
         if dist>30:
            await bot.send_message(chat_id = CHAT_ID, text = "1번 좌석이 공석입니다! \n Timer started for 10 seconds")
            timer_duration = 10
            start = time.time()
            while time.time() - start < timer_duration:
               pass
            await bot.send_message(chat_id = CHAT_ID, text = "1번 좌석의 짐을 치워주세요!")
         time.sleep(2)
   except KeyboardInterrupt:
         GPIO.cleanup()
# timer : https://parksh3641.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-python-%ED%83%80%EC%9D%B4%EB%A8%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-Timer

if __name__ == "__main__":
   loop = asyncio.get_event_loop()
   try:
      loop.run_until_complete(main())
   finally:
      loop.close()
# https://dojang.io/mod/page/view.php?id=2469
