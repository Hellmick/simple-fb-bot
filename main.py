from fbchat import Client
from fbchat.models import ThreadType, Message
from datetime import datetime
import zastepstwa

password = "#########"
email = "#########"
client = Client(email, password)

thread_id = "##############"
thread_type = ThreadType.GROUP


while True:
    now = datetime.now()

    messages = client.fetchThreadMessages(thread_id=thread_id, limit=1)
    if "!godzina" in messages[0].text:
        current_time = now.strftime("%H:%M")
        client.send(Message(text="Jest godzina " + current_time), thread_id=thread_id, thread_type=thread_type)
    if "!zastepstwa" in messages[0].text[0:11]:
        cl = "2 HG"
        if len(messages[0].text) >= 12:
            if messages[0].text[11] == " ":
                cl = messages[0].text[12:15]
        client.send(Message(text=zastepstwa.check(zastepstwa.getText("http://zastepstwa.zse.bydgoszcz.pl"), now.strftime("%d/%m/%y"), cl)), thread_id=thread_id, thread_type=thread_type)