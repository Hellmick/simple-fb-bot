from fbchat import Client
from fbchat.models import *
from zastepstwa import Zastepstwa
from datetime import datetime
from sqlite3 import connect, Error, Row
import sys


settings = {
    'email': "",
    'password': "",
    'thread_id': "2658551390837229",
    'thread_type': ThreadType.GROUP,
    'default_class': "3 H",
}

sql = {
    'create_table': """ CREATE TABLE IF NOT EXISTS scoreboard (
                           id text PRIMARY KEY,
                           score integer NOT NULL
                       ); """,
    'find_by_id': "SELECT * FROM scoreboard WHERE id=?",
    'insert_winner': "INSERT INTO scoreboard(id,score) VALUES(?,1)",
    'update_score': "UPDATE scoreboard SET score=? WHERE id=?",
    'select_all': "SELECT * FROM scoreboard",
}

class PopeBot(Client, Zastepstwa):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.conn = None
        self.winners = set()
        self.today = False
        settings['thread_id'] = self.uid
        settings['thread_type'] = ThreadType.USER

    def connect(self):
        try:
            self.conn = connect(".\\papiez.db")
            self.conn.row_factory = Row
            cur = self.conn.cursor()
            cur.execute(sql['create_table'])
        except Error as e:
            print(e)

    def count_save(self):
        for winner in self.winners:
            self.connect()
            cur = self.conn.cursor()
            res = cur.execute(sql['find_by_id'], (winner,)).fetchone()
            cur.execute(sql['insert_winner'], (winner,)) if not res \
                else cur.execute(sql['update_score'], (int(res["score"])+1, winner,))
            self.conn.commit()
            self.conn.close()
            print('Data saved successfully.')

    def get_leaderboard(self):
        msg = "Papież leaderboard:\n"
        self.connect()
        cur = self.conn.cursor()
        res = cur.execute(sql['select_all']).fetchall()
        self.conn.close()
        for person in res:
            msg += person["id"] + ": " + str(person["score"]) + "\n"

        return msg

    def fetch_pope(self, message):
        if "papiez" in message.text.lower() or "papież" in message.text.lower() or "papierz" in message.text.lower():
            self.winners = set(self.winners)
            self.winners.add(client.fetchUserInfo(message.author)[message.author].name)

    def creampie_with_it(self, message, current_time):
        if current_time == "21:37":
            self.fetch_pope(message)

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        message = message_object.text.lower()
        now = datetime.now()

        if thread_id == settings['thread_id']:
            if "!godzina" == message:
                current_time = now.strftime("%H:%M")
                self.send(Message(text="Jest godzina " + current_time), thread_id=settings['thread_id'],
                          thread_type=settings['thread_type'])

            elif "!zastepstwa" in message[0:11]:
                self.get_text("http://zastepstwa.zse.bydgoszcz.pl")
                if len(message) >= 12 and message[11] == " ":
                    self.send(Message(text=self.check(now.strftime("%d/%m/%y"), cl=message[12:15])),
                              thread_id=settings['thread_id'], thread_type=settings['thread_type'])
                else:
                    self.send(Message(text=self.check(now.strftime("%d/%m/%y"), cl=settings['default_class'])),
                              thread_id=settings['thread_id'], thread_type=settings['thread_type'])

            elif "!scoreboard" == message:
                self.send(Message(text=self.get_leaderboard()),
                          thread_id=settings['thread_id'], thread_type=settings['thread_type'])

            elif "bzdawka" in message or "bzdax" in message:
                self.send(Message(text="to kurwa jebana zdradziecka takich trzeba pałować"),
                          thread_id=settings['thread_id'], thread_type=settings['thread_type'])

            self.creampie_with_it(message_object, current_time)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('bot <email> <password>')
    settings['email'] = sys.argv[1]
    settings['password'] = sys.argv[2]
    client = PopeBot(settings['email'], settings['password'])
    while client.doOneListen():
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time == "21:37" and not client.today:
            client.send(Message(text="Papież"), thread_id=settings['thread_id'], thread_type=settings['thread_type'])
            client.today = True
        if current_time == "21:38" and client.today:
            client.count_save()
            client.winners = {}
            client.today = False
