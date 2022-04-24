import fbchat
import os
from datetime import datetime
from replacements import *
import threading
import time

EMAIL = os.getenv("FB_EMAIL")
PASSWORD = os.getenv("FB_PASS")

THREAD_TYPE = "group"
THREAD_ID = "2658551390837229"

session = fbchat.Session.login(EMAIL, PASSWORD)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

thread = None
if THREAD_TYPE == "group":
    thread = fbchat.Group(session=session, id=THREAD_ID)
elif THREAD_TYPE == "user":
    thread = fbchat.User(session=session, id=THREAD_ID)

replacements = Replacements()

BARQUE = "Pan\nkiedyś stanął nad brzegiem\nszukał ludzi\ngotowych pójść za nim\nby łowić serca\nsłów bożych prawdą\n" \
        "O PAANIEE\nTO TY NA MNIE SPOJRZAAŁEEŚ\nTWOOJE UUUSTAA\nDZIŚ WYRZEKŁY ME IIMIĘĘ\n" \
        "SWOOJĄ BAARKĘĘ\nPOZOSTAWIAM NA BRZEEGUUU\nRAAZEM Z TOOOBĄĄ\nNOWY ZACZNĘ DZIŚ ŁÓW"

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

def get_date():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    return current_date

def play_barka():
    for line in BARQUE.split("\n"):
        print(line)
        thread.send_text(line)
        time.sleep(0.5)

def check_time():
    while True:
        if get_time() == "21:37":
            play_barka()

def main():
    replacements = Replacements()

    for event in listener.listen():
        if isinstance(event, fbchat.MessageEvent):
            if event.message.text == "!godzina":
                thread.send_text("Jest godzina: " + get_time())
            if event.message.text == "!zastepstwa":
                msg = event.message.text.split(" ")
                cl = msg[1]
                thread.send_text(replacements.check(get_date(), cl))
            if event.message.text == "!barka":
                play_barka()

if __name__ == '__main__':
    main = threading.Thread(target=main)
    main.start()
    barka = threading.Thread(target=check_time)
    barka.start()
    main.join()
    play_barka.join()
    session.logout()