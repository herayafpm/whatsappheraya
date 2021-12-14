from time import sleep
from whatsapp import WhatsApp
whatsapp = WhatsApp(100, session="mysession")
while(True):
    user_names = whatsapp.unread_usernames(scrolls=100)
    for name in user_names:
        messages = whatsapp.get_last_message_for(name)
        messgaes_len = len(messages)
        latest_msg = messages[messgaes_len-1]
        if(latest_msg == 'Hai'):
            whatsapp.send_message('Halo')
        if(latest_msg == 'Cuk'):
            whatsapp.send_message('Ya')
        whatsapp.tutup_tab_user()