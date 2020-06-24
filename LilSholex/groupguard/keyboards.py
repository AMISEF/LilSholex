admin = {'keyboard': [
    ['Users', 'Groups'],
    ['Ban Group', 'Ban User'],
    ['Unban Group', 'Unban User'],
    ['Add Ad', 'Delete Ad']
], 'resize_keyboard': True}
en_back = {'keyboard': [['Back 🔙']], 'resize_keyboard': True}
en_user = {
    'keyboard': [['Add to Group', 'Support'], ['Help 🆘', 'Language 📖'], ['Validation 🔐']], 'resize_keyboard': True
}
fa_user = {
    'keyboard': [['اضافه کردن به گروه ⏬', 'پشتیبانی 👨‍💻'], ['راهنما 📕', 'زبان 📖'], ['احراز هویت 🔐']], 'resize_keyboard': True
}
en_lang = {'keyboard': [['فارسی 🇮🇷', 'English 🇺🇸'], ['Back 🔙']], 'resize_keyboard': True}
fa_lang = {'keyboard': [['فارسی 🇮🇷', 'English 🇺🇸'], ['بازگشت 🔙']], 'resize_keyboard': True}
en_number = {'keyboard': [[{'text': 'Share ☎️', 'request_contact': True}], ['Back 🔙']], 'resize_keyboard': True}
fa_number = {'keyboard': [[{'text': 'اشتراک ☎️', 'request_contact': True}], ['بازگشت 🔙']], 'resize_keyboard': True}
verify_number = {'inline_keyboard': [[{'text': 'Verify ☎️', 'url': 't.me/SholexBot'}]]}
fa_help = {'keyboard': [['دستورات کلی 👨', 'دستورات ادمین 💂‍♀️'], ['دستورات سازنده 👨‍💻'], ['بازگشت 🔙']], 'resize_keyboard': True}
en_help = {'keyboard': [['General 👨', 'Admin 💂‍♀️'], ['Creator 👨‍💻'], ['Back 🔙']], 'resize_keyboard': True}
fa_login = {'inline_keyboard': [[{'text': 'چت خصوصی 💬', 'url': 't.me/SholexBot'}]]}
en_login = {'inline_keyboard': [[{'text': 'Private Chat 💬', 'url': 't.me/SholexBot'}]]}


def invite(link):
    return {'inline_keyboard': [[{'text': 'Join ⏬', 'url': link}]]}


def support(link):
    return {'inline_keyboard': [[{'text': 'Support Bot ⏬', 'url': link}]]}


def verify(verify_id):
    return {'inline_keyboard': [[{'text': 'Verify ☑️', 'callback_data': str(verify_id)}]]}

def inline_panel(chat_id, from_id, user, group):
    return {'en': {'inline_keyboard': [
        [{'text': 'Link lock', 'callback_data': 'none'},
         {'text': group.database.link_lock, 'callback_data': f'change_link_lock|{chat_id}'}],

        [{'text': 'Id lock', 'callback_data': 'none'},
         {'text': group.database.id_lock, 'callback_data': f'change_id_lock|{chat_id}'}],

        [{'text': 'Sharp lock', 'callback_data': 'none'},
         {'text': group.database.sharp_lock, 'callback_data': f'change_sharp_lock|{chat_id}'}],

        [{'text': 'Text lock', 'callback_data': 'none'},
         {'text': group.database.text_lock, 'callback_data': f'change_text_lock|{chat_id}'}],

        [{'text': 'Forward lock', 'callback_data': 'none'},
         {'text': group.database.forward_lock, 'callback_data': f'change_forward_lock|{chat_id}'}],

        [{'text': 'Image lock', 'callback_data': 'none'},
         {'text': group.database.image_lock, 'callback_data': f'change_image_lock|{chat_id}'}],

        [{'text': 'Video lock', 'callback_data': 'none'},
         {'text': group.database.video_lock, 'callback_data': f'change_video_lock|{chat_id}'}],

        [{'text': 'Document lock', 'callback_data': 'none'},
         {'text': group.database.document_lock, 'callback_data': f'change_document_lock|{chat_id}'}],

        [{'text': 'Sticker lock', 'callback_data': 'none'},
         {'text': group.database.sticker_lock, 'callback_data': f'change_sticker_lock|{chat_id}'}],

        [{'text': 'Location lock', 'callback_data': 'none'},
         {'text': group.database.location_lock, 'callback_data': f'change_location_lock|{chat_id}'}],

        [{'text': 'Phone Number lock', 'callback_data': 'none'},
         {'text': group.database.phone_number_lock, 'callback_data': f'change_phone_number_lock|{chat_id}'}],

        [{'text': 'Voice Message lock', 'callback_data': 'none'},
         {'text': group.database.voice_message_lock, 'callback_data': f'change_voice_message_lock|{chat_id}'}],

        [{'text': 'Video Message lock', 'callback_data': 'none'},
         {'text': group.database.video_message_lock, 'callback_data': f'change_video_message_lock|{chat_id}'}],

        [{'text': 'Gif lock', 'callback_data': 'none'},
         {'text': group.database.gif_lock, 'callback_data': f'change_gif_lock|{chat_id}'}],

        [{'text': 'Poll lock', 'callback_data': 'none'},
         {'text': group.database.poll_lock, 'callback_data': f'change_poll_lock|{chat_id}'}],

        [{'text': 'Game lock', 'callback_data': 'none'},
         {'text': group.database.game_lock, 'callback_data': f'change_game_lock|{chat_id}'}],

        [{'text': 'English lock', 'callback_data': 'none'},
         {'text': group.database.english_lock, 'callback_data': f'change_english_lock|{chat_id}'}],

        [{'text': 'Persian lock', 'callback_data': 'none'},
         {'text': group.database.persian_lock, 'callback_data': f'change_persian_lock|{chat_id}'}],

        [{'text': 'Contact lock', 'callback_data': 'none'},
         {'text': group.database.contact_lock, 'callback_data': f'change_contact_lock|{chat_id}'}],

        [{'text': 'Bot lock', 'callback_data': 'none'},
         {'text': group.database.bot_lock, 'callback_data': f'change_bot_lock|{chat_id}'}],

        [{'text': 'Services lock', 'callback_data': 'none'},
         {'text': group.database.services_lock, 'callback_data': f'change_services_lock|{chat_id}'}],

        [{'text': 'Inline Keyboard lock', 'callback_data': 'none'},
         {'text': group.database.inline_keyboard_lock, 'callback_data': f'change_inline_keyboard_lock|{chat_id}'}]
    ]},

        'fa': {'inline_keyboard': [
            [{'text': 'قفل لینک', 'callback_data': 'none'},
             {'text': group.database.link_lock, 'callback_data': f'change_link_lock|{chat_id}'}],

            [{'text': 'قفل آیدی', 'callback_data': 'none'},
             {'text': group.database.id_lock, 'callback_data': f'change_id_lock|{chat_id}'}],

            [{'text': 'قفل هشتگ', 'callback_data': 'none'},
             {'text': group.database.sharp_lock, 'callback_data': f'change_sharp_lock|{chat_id}'}],

            [{'text': 'قفل متن', 'callback_data': 'none'},
             {'text': group.database.text_lock, 'callback_data': f'change_text_lock|{chat_id}'}],

            [{'text': 'قفل فوروارد', 'callback_data': 'none'},
             {'text': group.database.forward_lock, 'callback_data': f'change_forward_lock|{chat_id}'}],

            [{'text': 'قفل عکس', 'callback_data': 'none'},
             {'text': group.database.image_lock, 'callback_data': f'change_image_lock|{chat_id}'}],

            [{'text': 'قفل فیلم', 'callback_data': 'none'},
             {'text': group.database.video_lock, 'callback_data': f'change_video_lock|{chat_id}'}],

            [{'text': 'قفل فایل', 'callback_data': 'none'},
             {'text': group.database.document_lock, 'callback_data': f'change_document_lock|{chat_id}'}],

            [{'text': 'قفل استیکر', 'callback_data': 'none'},
             {'text': group.database.sticker_lock, 'callback_data': f'change_sticker_lock|{chat_id}'}],

            [{'text': 'قفل مکان', 'callback_data': 'none'},
             {'text': group.database.location_lock, 'callback_data': f'change_location_lock|{chat_id}'}],

            [{'text': 'قفل شماره تلفن', 'callback_data': 'none'},
             {'text': group.database.phone_number_lock, 'callback_data': f'change_phone_number_lock|{chat_id}'}],

            [{'text': 'قفل ویس', 'callback_data': 'none'},
             {'text': group.database.voice_message_lock, 'callback_data': f'change_voice_message_lock|{chat_id}'}],

            [{'text': 'قفل ویدیو مسیج', 'callback_data': 'none'},
             {'text': group.database.video_message_lock, 'callback_data': f'change_video_message_lock|{chat_id}'}],

            [{'text': 'قفل گیف', 'callback_data': 'none'},
             {'text': group.database.gif_lock, 'callback_data': f'change_gif_lock|{chat_id}'}],

            [{'text': 'قفل نظرسنجی', 'callback_data': 'none'},
             {'text': group.database.poll_lock, 'callback_data': f'change_poll_lock|{chat_id}'}],

            [{'text': 'قفل بازی', 'callback_data': 'none'},
             {'text': group.database.game_lock, 'callback_data': f'change_game_lock|{chat_id}'}],

            [{'text': 'قفل انگلیسی', 'callback_data': 'none'},
             {'text': group.database.english_lock, 'callback_data': f'change_english_lock|{chat_id}'}],

            [{'text': 'قفل فارسی', 'callback_data': 'none'},
             {'text': group.database.persian_lock, 'callback_data': f'change_persian_lock|{chat_id}'}],

            [{'text': 'قفل مخاطب', 'callback_data': 'none'},
             {'text': group.database.contact_lock, 'callback_data': f'change_contact_lock|{chat_id}'}],

            [{'text': 'قفل ربات ها', 'callback_data': 'none'},
             {'text': group.database.bot_lock, 'callback_data': f'change_bot_lock|{chat_id}'}],

            [{'text': 'قفل سرویس تلگرام', 'callback_data': 'none'},
             {'text': group.database.services_lock, 'callback_data': f'change_services_lock|{chat_id}'}],

            [{'text': 'قفل دکمه شیشه ای', 'callback_data': 'none'},
             {'text': group.database.inline_keyboard_lock, 'callback_data': f'change_inline_keyboard_lock|{chat_id}'}]
        ]}
    }

def manage_panel(chat_id, reply_id, user, group):
    muted_text = group.translate('manage_panel_mute_text')['T']
    if not group.get_chat_member(
        reply_id
    ).get('can_send_messages', None):
        muted_text = group.translate('manage_panel_mute_text')['F']
    return {'en': {'inline_keyboard': [
        [{'text': 'Warn count(s)', 'callback_data': 'none'},
         {'text': group.get_warns(user.database).count, 'callback_data': 'none'}],

        [{'text': 'Add warn', 'callback_data': 'AddwarnU|'+str(reply_id)}],

        [{'text': 'Delete all warns', 'callback_data': 'DeleteallwarnsU|'+str(reply_id)}],

        [{'text': 'Ban', 'callback_data': 'BanU|'+str(reply_id)},
         {'text': 'Unban', 'callback_data': 'UnbanU|'+str(reply_id)}],

        [{'text': muted_text['en'], 'callback_data': '{}U|{}'.format(muted_text['en'], reply_id)}]
    ]},
        'fa': {'inline_keyboard': [
            [{'text': 'تعداد اخطار ها', 'callback_data': 'none'},
             {'text': group.get_warns(user.database).count, 'callback_data': 'none'}],

            [{'text': 'اخطار', 'callback_data': 'AddwarnU|' + str(reply_id)}],

            [{'text': 'پاکسازی اخطار ها', 'callback_data': 'DeleteallwarnsU|' + str(reply_id)}],

            [{'text': 'بن', 'callback_data': 'BanU|' + str(reply_id)},
             {'text': 'آن بن', 'callback_data': 'UnbanU|' + str(reply_id)}],

            [{'text': muted_text['fa'], 'callback_data': '{}U|{}'.format(muted_text['en'], reply_id)}]
        ]}
}
