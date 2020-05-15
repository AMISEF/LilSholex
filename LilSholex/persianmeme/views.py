from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from persianmeme import functions, objects, keyboards, models
from django.http import HttpResponse
import json


@csrf_exempt
@require_POST
def webhook(request):
    update = json.loads(request.body.decode())
    if 'inline_query' in update:
        user = objects.User(update['inline_query']['from']['id'])
        user.send_ad()
        user.set_username()
        user.database.save()
        if user.database.status != 'f':
            query = update['inline_query']['query']
            offset = update['inline_query']['offset']
            inline_query_id = update['inline_query']['id']
            results, next_offset = user.get_voices(query, offset)
            functions.answer_inline_query(inline_query_id, json.dumps(results), next_offset, 300)
    elif 'callback_query' in update:
        callback_query = update['callback_query']
        owner = objects.User(callback_query['from']['id'])
        query_id = callback_query['id']
        callback_data = callback_query['data'].split(':')
        try:
            message = callback_query['message']
        except KeyError:
            message = None
            message_id = None
        else:
            message_id = message['message_id']
        if callback_data[0] == 'read':
            user = objects.User(callback_data[1])
            user.database.sent_message = False
            user.send_message('پیام شما توسط مدیریت بررسی شد ✔')
            owner.delete_message(message_id)
            functions.answer_callback_query(query_id, 'Read ✅', False)
            user.database.save()
        elif callback_data[0] == 'ban':
            user = objects.User(callback_data[1])
            user.database.sent_message = False
            user.database.status = 'b'
            user.send_message('شما از استفاده از ربات محروم شدید 🚫')
            owner.delete_message(message_id)
            functions.answer_callback_query(query_id, f'User {user.database.chat_id} has been banned !', True)
            user.database.save()
        elif callback_data[0] == 'reply':
            user = objects.User(callback_data[1])
            owner.database.menu = 9
            owner.database.temp_user_id = user.database.chat_id
            owner.send_message('Please send the text which you want to be replied !', keyboards.en_back)
            owner.delete_message(message_id)
            functions.answer_callback_query(query_id, 'Replying 🔴', False)
            user.database.sent_message = False
            user.send_message('پیام ارسالی شما توسط مدیریت بررسی شد ✅')
            user.database.save()
            owner.database.save()
        elif callback_data[0] == 'accept':
            owner.delete_message(message_id)
            try:
                voice = models.Voice.objects.get(file_unique_id=message['voice']['file_unique_id'], status='p')
            except models.Voice.DoesNotExist:
                functions.answer_callback_query(query_id, 'This voice has been processed before ⚠', True)
            else:
                voice.status = 'a'
                voice.save()
                user = objects.User(instance=voice.sender)
                user.database.sent_voice = False
                user.database.save()
                functions.answer_callback_query(query_id, 'Voice has been accepted ✅', True)
                user.send_message('ویس ارسالی شما توسط مدیر ربات تایید شد ✅')
        elif callback_data[0] == 'deny':
            owner.delete_message(message_id)
            try:
                voice = models.Voice.objects.get(file_unique_id=message['voice']['file_unique_id'], status='p')
            except models.Voice.DoesNotExist:
                functions.answer_callback_query(query_id, 'This voice has been processed before ⚠', False)
            else:
                user = objects.User(instance=voice.sender)
                user.database.sent_voice = False
                user.database.save()
                voice.delete()
                functions.answer_callback_query(query_id, 'Voice has been denied ❌', False)
                user.send_message('ویس ارسالی شما توسط مدیر ربات رد شد ❌')
        elif callback_data[0] == 'delete':
            functions.delete_voice(message['voice']['file_unique_id'])
            user = objects.User(callback_data[1])
            user.database.delete_request = False
            functions.answer_callback_query(query_id, 'Voice has been Deleted ✅', True)
            owner.delete_message(message_id)
            user.send_message('ویس درخواستی شما از ربات حذف شد ✅')
            user.database.save()
        elif callback_data[0] == 'delete_deny':
            user = objects.User(callback_data[1])
            user.database.delete_request = False
            owner.delete_message(message_id)
            functions.answer_callback_query(query_id, 'Delete Request has been denied ☑', True)
            user.send_message('درخواست حذف ویس شما توسط مدیریت رد شد ❌')
            user.database.save()
        else:
            user = objects.User(callback_query['from']['id'])
            user.send_ad()
            if callback_data[0] == 'up':
                try:
                    voice = models.Voice.objects.get(voice_id=callback_data[1])
                except models.Voice.DoesNotExist:
                    pass
                else:
                    if user.database in voice.voters.all():
                        functions.answer_callback_query(query_id, 'شما قبلا به این ویس رای داده اید ❌', False)
                    else:
                        voice.voters.add(user.database)
                        voice.votes += 1
                        voice.save()
                        functions.answer_callback_query(query_id, 'شما به این ویس رای 👍 دادید !', False)
            elif callback_data[0] == 'down':
                try:
                    voice = models.Voice.objects.get(voice_id=callback_data[1])
                except models.Voice.DoesNotExist:
                    pass
                else:
                    if user.database in voice.voters.all():
                        voice.voters.remove(user.database)
                        voice.votes -= 1
                        voice.save()
                        functions.answer_callback_query(query_id, 'شما رای خود را پس گرفتید ✔', False)
                    else:
                        functions.answer_callback_query(query_id, 'شما هنوز رای نداده اید ✖', False)
            user.database.save()
    else:
        if 'message' in update:
            message = update['message']
        elif 'edited_message' in update:
            message = update['edited_message']
        else:
            return HttpResponse(status=200)
        text = message.get('text', None)
        message_id = message['message_id']
        user = objects.User(message['chat']['id'])
        user.set_username()
        if user.database.rank in ['o', 'a', 's']:
            if text == '/start':
                user.database.menu = 1
                user.send_message('Welcome to Admin Panel !', keyboards.owner, message_id)
            elif user.database.menu == 1:
                if text == 'Add Sound':
                    user.database.menu = 2
                    user.send_message('Please send the voice name to add !', keyboards.en_back)
                elif text == 'Delete Sound':
                    user.database.menu = 4
                    user.send_message('Please send the voice file which you want to delete !', keyboards.en_back)
                elif text == 'Voice Count':
                    user.send_message(functions.count_voices())
                elif text == 'Member Count':
                    user.send_message(f'All members count : {models.User.objects.count()}')
                elif text == 'Ban a User':
                    user.database.menu = 5
                    user.send_message('Please send user id .', keyboards.en_back)
                elif text == 'Unban a User':
                    user.database.menu = 6
                    user.send_message('Please send user id to unban !', keyboards.en_back)
                elif text == 'Full Ban':
                    user.database.menu = 7
                    user.send_message(
                        'Please send the user id which you want it to be full banned !', keyboards.en_back
                    )
                elif text == 'Message User':
                    if user.database.rank == 'o':
                        user.database.menu = 8
                        user.send_message('Please send Target User ID .', keyboards.en_back)
                    else:
                        user.send_message('This part is Owner only ⚠')
                elif text == 'Add Ad':
                    if user.database.rank == 'o':
                        user.database.menu = 10
                        user.send_message('Please send the Update Information .', keyboards.en_back)
                    else:
                        user.send_message('You do not have enough permissions to access this part ⚠')
                elif text == 'Delete Ad':
                    if user.database.rank == 'o':
                        user.database.menu = 11
                        user.send_message('Please send the Ad ID .', keyboards.en_back)
                elif text == 'Unchecked Voices':
                    if user.database.rank in ['o', 'a']:
                        if (pending_voices := models.Voice.objects.filter(status='p')).exists():
                            for voice in pending_voices:
                                user.send_voice(
                                    voice.file_id,
                                    f'{voice.name}\n\nFrom : {voice.sender.chat_id}\n\n'
                                    f'Username : {voice.sender.username}',
                                    keyboards.voice
                                )
                            user.send_message('Here are new voices 👆', reply_to_message_id=message_id)
                        else:
                            user.send_message('There is no more voice left !')
                    else:
                        user.send_message('You can not use this part ❌')
                elif text == 'Get User':
                    user.database.menu = 12
                    user.send_message('Please send the user_id .', keyboards.en_back)
                elif 'voice' in message:
                    search_result = functions.get_voice(message['voice']['file_unique_id'])
                    if search_result.exists():
                        target_voice_name = search_result[0].name
                        user.send_message(
                            f'Voice Name : {target_voice_name}\n\nYou can use it by typing\n\n'
                            f'@Persian_Meme_Bot {target_voice_name}\n\nin a chat 😁',
                            keyboards.use(target_voice_name)
                        )
                    else:
                        user.send_message('I could not find this voice ☹')
                else:
                    user.send_message('Unknown Command ⚠')
            elif user.database.menu == 2:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at the main menu 🔙', keyboards.owner)
                else:
                    if text:
                        if len(text) > 50:
                            user.send_message('Voice name is longer than limit !')
                        else:
                            user.database.menu = 3
                            user.database.temp_voice_name = text
                            user.send_message('Now send the voice file .')
                    else:
                        user.send_message('Please send a name !')
            elif user.database.menu == 3:
                if text == 'Back 🔙':
                    user.database.menu = 2
                    user.send_message('Please send the Voice Name .')
                else:
                    if 'voice' in message:
                        if functions.add_voice(
                                message['voice']['file_id'],
                                message['voice']['file_unique_id'],
                                user.database.temp_voice_name,
                                user.database,
                                'a'
                        ):
                            user.database.menu = 1
                            user.send_message('Voice has been added to database ✅', keyboards.owner)
                        else:
                            user.send_message('Voice is already in the database ❌')
                    else:
                        user.send_message('Please send a valid voice file !')
            elif user.database.menu == 4:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are the main menu !', keyboards.owner)
                else:
                    if 'voice' in message:
                        functions.delete_voice(message['voice']['file_unique_id'])
                        user.database.menu = 1
                        user.send_message('Voice has been deleted 🗑', keyboards.owner)
                    else:
                        user.send_message('Voice File is not Valid !')
            elif user.database.menu == 5:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at the main menu 🔙', keyboards.owner)
                else:
                    try:
                        user_id = int(text)
                    except (ValueError, TypeError):
                        user.send_message('User ID is not valid ⚠')
                    else:
                        user.database.menu = 1
                        functions.change_user_status(user_id, 'b')
                        user.send_message('User has been banned ❌', keyboards.owner)
            elif user.database.menu == 6:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at the main menu 🔙', keyboards.owner)
                else:
                    try:
                        user_id = int(text)
                    except (ValueError, TypeError):
                        user.send_message('User ID is not valid ⚠')
                    else:
                        user.database.menu = 1
                        functions.change_user_status(user_id, 'a')
                        user.send_message('User has been unbanned ☑', keyboards.owner)
            elif user.database.menu == 7:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at the main menu 🔙', keyboards.owner)
                else:
                    try:
                        user_id = int(text)
                    except (ValueError, TypeError):
                        user.send_message('User ID is not valid ⚠')
                    else:
                        user.database.menu = 1
                        functions.change_user_status(user_id, 'f')
                        user.send_message('User has been Full Banned !', keyboards.owner)
            elif user.database.menu == 8:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at the main menu !', keyboards.owner)
                else:
                    try:
                        user.database.temp_user_id = int(text)
                    except (ValueError, TypeError):
                        user.send_message('You must use a number as User ID !')
                    else:
                        user.database.menu = 9
                        user.send_message('Now send the text which you want to be delivered .')
            elif user.database.menu == 9:
                if text == 'Back 🔙':
                    user.database.menu = 8
                    user.send_message('Please send the user Chat ID .')
                else:
                    user.database.menu = 1
                    objects.User(user.database.temp_user_id).send_message(f'پیام از طرف مدیریت 👇\n\n{text}')
                    user.send_message('Message has been sent to user ✔', keyboards.owner)
            elif user.database.menu == 10:
                user.database.menu = 1
                if text == 'Back 🔙':
                    user.send_message('You are back at the main menu 🔙', keyboards.owner)
                else:
                    ad_id = models.Ad.objects.create(chat_id=user.database.chat_id, message_id=message_id).ad_id
                    user.send_message(
                        f'Update message has been submitted ✔️\nAd ID : {ad_id}', keyboards.owner
                    )
            elif user.database.menu == 11:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at the main menu 🔙', keyboards.owner)
                else:
                    try:
                        models.Ad.objects.get(ad_id=int(text)).delete()
                    except (ValueError, models.Ad.DoesNotExist):
                        user.send_message('Ad ID not found !', reply_to_message_id=message_id)
                    else:
                        user.database.menu = 1
                        user.send_message('Ad has been deleted ❌', keyboards.owner)
            elif user.database.menu == 12:
                if text == 'Back 🔙':
                    user.database.menu = 1
                    user.send_message('You are back at main menu 🔙', keyboards.owner, message_id)
                else:
                    try:
                        int(text)
                    except ValueError:
                        user.send_message('User ID must be a number !', reply_to_message_id=message_id)
                    else:
                        user.database.menu = 1
                        user.send_message(
                            f'Here is user profile 👇\n\n[{text}](tg://user?id={text})',
                            keyboards.owner,
                            message_id,
                            'Markdown'
                        )
        elif user.database.status == 'a' and user.database.rank == 'u':
            user.send_ad()
            if text == '/start':
                user.database.menu = 1
                user.send_message('به ربات Persian Meme خوش آمدید 😁', keyboards.user, message_id)
            elif user.database.menu == 1:
                if text == 'راهنما 🔰':
                    user.send_message('برای استفاده از ربات کافیست آیدی ربات @Persian_Meme_Bot را در چت تایپ کنید !')
                elif text == 'آخرین ویس ها 🆕':
                    voices_str = ''
                    for voice in models.Voice.objects.filter(status='a', voice_type='n').order_by('-voice_id')[:15]:
                        voices_str += f'⭕ {voice.name}\n'
                    user.send_message(voices_str)
                elif text == 'ارتباط با مدیریت 📬':
                    if user.database.sent_message:
                        user.send_message('پیام قبلی شما در انتظار مشاهده است ⚠')
                    else:
                        user.database.menu = 2
                        user.send_message('لطفا پیام خود را در قالب متن ارسال کنید !', keyboards.per_back)
                elif text == 'پیشنهاد ویس 🔥':
                    if user.database.sent_voice:
                        user.send_message('ویس قبلی شما در انتظار تایید است ❌')
                    else:
                        user.database.menu = 3
                        user.send_message('لطفا نام ویس پیشنهادی را ارسال کنید .', keyboards.per_back)
                elif text == 'حذف ویس ❌':
                    user.database.menu = 5
                    user.send_message(
                        'لطفا یکی از ویس های پیشنهادی خود را جهت حذف ارسال کنید', keyboards.per_back
                    )
                elif text == 'ویس های محبوب 👌':
                    voices_str = ''
                    for voice in models.Voice.objects.order_by('-votes')[:15]:
                        voices_str += f'⭕ {voice.name}\n'
                    user.send_message(voices_str)
                elif text == 'امتیازدهی ⭐':
                    user.database.menu = 6
                    user.send_message('لطفا یکی از گزینه های زیر را انتخاب کنید .', keyboards.toggle)
                elif text == 'مرتب سازی 🗂':
                    user.database.menu = 7
                    user.send_message('لطفا یکی از روش های مرتب سازی زیر را انتخاب کنید 👇', keyboards.voice_order)
                elif text == 'درخواست حذف ویس ✖':
                    if user.database.delete_request:
                        user.send_message('درخواست قبلی شما در حال بررسی است ⚠')
                    else:
                        user.database.menu = 8
                        user.send_message('لطفا ویس مورد نظر را ارسال کنید .', keyboards.per_back)
                elif text == 'حمایت مالی 💸':
                    user.database.menu = 10
                    user.send_message('لطفا مبلغ مورد نظر را به تومان وارد کنید 💸', keyboards.per_back)
                elif text == 'ویس های شخصی 🔒':
                    user.database.menu = 11
                    user.send_message('یکی از گزینه های زیر را انتخاب کنید .', keyboards.private)
                elif text == 'علاقه مندی ها ❤️':
                    user.database.menu = 15
                    user.send_message('یکی از گزینه هارا انتخاب کنید .', keyboards.private)
                elif 'voice' in message:
                    search_result = functions.get_voice(message['voice']['file_unique_id'])
                    if search_result.exists():
                        target_voice_name = search_result[0].name
                        user.send_message(
                            f'نام ویس : {target_voice_name}\n\nشما میتوانید با تایپ\n\n'
                            f'@Persian_Meme_Bot {target_voice_name}\n\n از این ویس استفاده کنید 😁',
                            keyboards.use(target_voice_name)
                        )
                    else:
                        user.send_message('نتونستم این ویس رو پیدا کنم ☹')
                else:
                    user.send_message('دستور ناشناخته ⚠')
            elif user.database.menu == 2:
                user.database.menu = 1
                if text == 'بازگشت 🔙':
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                else:
                    owner = objects.User(instance=functions.get_owner())
                    owner.send_message(
                        f'New Message from {user.database.chat_id} 👇\n\n {text}',
                        keyboards.message(user.database.chat_id)
                    )
                    user.database.sent_message = True
                    user.send_message('پیام شما به مدیریت ارسال شد ✔', keyboards.user, message_id)
            elif user.database.menu == 3:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                elif text:
                    if len(text) > 50:
                        user.send_message('نام ویس بیش از حد طولانی است ❌')
                    else:
                        user.database.menu = 4
                        user.database.temp_voice_name = text
                        user.send_message('لطفا ویس مورد نظر را ارسال کنید .')
                else:
                    user.send_message('لطفا یک متن به عنوان اسم ویس وارد کنید ⚠')
            elif user.database.menu == 4:
                if text == 'بازگشت 🔙':
                    user.database.menu = 3
                    user.send_message('لطفا نام ویس مورد نظر را ارسال کنید !')
                else:
                    if 'voice' in message:
                        if functions.add_voice(
                                message['voice']['file_id'],
                                message['voice']['file_unique_id'],
                                user.database.temp_voice_name,
                                user.database,
                                'p'
                        ):
                            user.database.sent_voice = True
                            user.database.menu = 1
                            for admin in functions.get_admins():
                                admin = objects.User(instance=admin)
                                admin.send_message('There is a new pending voice ⚠️')
                            user.send_message(
                                'ویس پیشنهادی شما برای تایید به مدیریت ارسال شد ✅', keyboards.user
                            )
                        else:
                            user.send_message('این ویس در ربات موجود میباشد ⚠', reply_to_message_id=message_id)
                    else:
                        user.send_message('لطفا یک ویس ارسال کنید ⚠')
            elif user.database.menu == 5:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                else:
                    if 'voice' in message:
                        if (result_voice := models.Voice.objects.filter(
                                file_unique_id=message['voice']['file_unique_id'],
                                status='a', sender=user.database,
                                voice_type='n'
                        )).exists():
                            result_voice.delete()
                            user.database.menu = 1
                            user.send_message('ویس شما با موفقیت حذف شد 🗑', keyboards.user)
                        else:
                            user.send_message('ویس ارسالی متعلق به شما نبوده و یا در ربات موجود نمیباشد ❌')
                    else:
                        user.send_message('لطفا یک ویس ارسال کنید 🔴')
            elif user.database.menu == 6:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                elif text == 'روشن 🔛':
                    user.database.vote = True
                    user.database.menu = 1
                    user.send_message('سیستم امتیازدهی برای شما روشن شد 🔛', keyboards.user)
                elif text == 'خاموش 🔴':
                    user.database.vote = False
                    user.database.menu = 1
                    user.send_message('سیستم امتیازدهی برای شما خاموش شد 🔴', keyboards.user)
                else:
                    user.send_message('انتخاب نامعتبر ⚠')
            elif user.database.menu == 7:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                elif text == 'جدید به قدیم':
                    user.database.voice_order = '-voice_id'
                    user.database.menu = 1
                    user.send_message('مرتب سازی ویس های تغییر کرد ✅', keyboards.user)
                elif text == 'قدیم به جدید':
                    user.database.voice_order = 'voice_id'
                    user.database.menu = 1
                    user.send_message('مرتب سازی ویس های تغییر کرد ✅', keyboards.user)
                elif text == 'بهترین به بدترین':
                    user.database.voice_order = '-votes'
                    user.database.menu = 1
                    user.send_message('مرتب سازی ویس های تغییر کرد ✅', keyboards.user)
                elif text == 'بدترین به بهترین':
                    user.database.voice_order = 'votes'
                    user.database.menu = 1
                    user.send_message('مرتب سازی ویس های تغییر کرد ✅', keyboards.user)
                else:
                    user.send_message('دستور نامعتبر ⚠')
            elif user.database.menu == 8:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                else:
                    if 'voice' in message and functions.get_voice(message['voice']['file_unique_id']).exists():
                        owner = objects.User(instance=functions.get_owner())
                        user.database.menu = 1
                        user.delete_request = True
                        user.send_message('درخواست شما با موفقیت ثبت شد ✅', keyboards.user, message_id)
                        owner.send_voice(
                            message['voice']['file_id'], f'Delete Request from : {user.database.chat_id}',
                            keyboards.delete_voice(user.database.chat_id)
                        )
                    else:
                        user.send_message('لطفا یک ویس ارسال کنید ⚠')
            elif user.database.menu == 10:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما در صفحه ی اصلی هستید .', keyboards.user)
                else:
                    try:
                        donate = int(text)
                    except (ValueError, TypeError):
                        user.send_message('مبلغ وارد شده معتبر نیست ✖️')
                    else:
                        user.database.menu = 1
                        user.send_message(
                            'برای حمایت مالی از دکمه ی زیر استفاده کنید ❤️',
                            keyboards.donate(donate)
                        )
                        user.send_message('☝️☝️☝️', keyboards.user)
            elif user.database.menu == 11:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                elif text == 'افزودن ⏬':
                    if user.database.private_voices.count() <= 30:
                        user.database.menu = 12
                        user.send_message('لطفا نام ویس را ارسال کنید .', keyboards.per_back)
                    else:
                        user.send_message('شما حداکثر تعداد ویس های شخصی را ارسال کرده اید ⚠️')
                elif text == 'حذف 🗑':
                    user.database.menu = 13
                    user.send_message('ویس مورد نظر را ارسال کنید .', keyboards.per_back)
                else:
                    user.send_message('دستور نامعتبر ⚠️')
            elif user.database.menu == 12:
                if text == 'بازگشت 🔙':
                    user.database.menu = 11
                    user.send_message('یکی از گزینه هارا انتخاب کنید .', keyboards.private)
                else:
                    if text:
                        if len(text) > 50:
                            user.send_message('نام طولانی تر از حد مجاز است ❌')
                        else:
                            user.database.temp_voice_name = text
                            user.database.menu = 14
                            user.send_message('لطفا ویس را ارسال کنید .')
                    else:
                        user.send_message('لطفا یک نام وارد کنید ⚠️')
            elif user.database.menu == 13:
                if text == 'بازگشت 🔙':
                    user.database.menu = 11
                    user.send_message('یکی از گزینه هارا انتخاب کنید .', keyboards.private)
                else:
                    if 'voice' in message and (
                            current_voice := functions.get_voice(message['voice']['file_unique_id'], voice_type='p')
                    ).exists():
                        if current_voice[0] in user.database.private_voices.all():
                            current_voice[0].delete()
                            user.database.menu = 11
                            user.send_message('ویس مورد نظر از ربات حذف شد !', keyboards.private)
                        else:
                            user.send_message('ویس مورد نظر از ویس های شخصی شما نیست ❌')
                    else:
                        user.send_message('ویس ارسالی معتبر نیست ❌')
            elif user.database.menu == 14:
                if text == 'بازگشت 🔙':
                    user.database.menu = 12
                    user.send_message('نام ویس را ارسال کنید .')
                else:
                    if 'voice' in message:
                        if not functions.get_voice(message['voice']['file_unique_id']).exists():
                            user.database.private_voices.create(
                                file_id=message['voice']['file_id'],
                                file_unique_id=message['voice']['file_unique_id'],
                                status='a',
                                voice_type='p',
                                sender=user.database,
                                name=user.database.temp_voice_name
                            )
                            user.database.menu = 11
                            user.send_message('این ویس به لیست ویس های شما اضافه شد ✅', keyboards.private)
                        else:
                            user.send_message('این ویس در ربات موجود است ❌')
                    else:
                        user.send_message('لطفا یک ویس ارسال کنید ✖️')
            elif user.database.menu == 15:
                if text == 'بازگشت 🔙':
                    user.database.menu = 1
                    user.send_message('شما به منوی اصلی بازگشتید 🔙', keyboards.user)
                elif text == 'افزودن ⏬':
                    if user.database.favorite_voices.count() <= 30:
                        user.database.menu = 16
                        user.send_message('لطفا ویس مورد نظر را ارسال کنید .', keyboards.per_back)
                    else:
                        user.send_message('شما حداکثر تعداد ویس های مورد علاقه را اضافه کرده اید ⚠️')
                elif text == 'حذف 🗑':
                    user.database.menu = 17
                    user.send_message('ویس مورد نظر را ارسال کنید .', keyboards.per_back)
                else:
                    user.send_message('دستور نامعتبر ⚠️')
            elif user.database.menu == 16:
                if text == 'بازگشت 🔙':
                    user.database.menu = 15
                    user.send_message('🔙', keyboards.private)
                else:
                    if 'voice' in message:
                        current_voice = functions.get_voice(message['voice']['file_unique_id'])
                        if current_voice.exists():
                            if current_voice[0] not in user.database.favorite_voices.all():
                                user.database.favorite_voices.add(current_voice[0])
                                user.database.menu = 15
                                user.send_message(
                                    'ویس مورد نظر به لیست علاقه مندی های شما اضافه شد ✔️',
                                    keyboards.private
                                )
                            else:
                                user.send_message('ویس در لیست موجود است ❌')
                        else:
                            user.send_message('این ویس در ربات موجود نیست ❌')
                    else:
                        user.send_message('لطفا یک ویس ارسال کنید !')
            elif user.database.menu == 17:
                if text == 'بازگشت 🔙':
                    user.database.menu = 15
                    user.send_message('🔙', keyboards.private)
                else:
                    if 'voice' in message:
                        current_voice = functions.get_voice(message['voice']['file_unique_id'])
                        if current_voice.exists():
                            user.database.favorite_voices.remove(current_voice[0])
                            user.database.menu = 15
                            user.send_message('ویس از لیست حذف شد !', keyboards.private)
                        else:
                            user.send_message('این ویس در ربات موجود نیست !')
                    else:
                        user.send_message('لطفا یک ویس ارسال کنید !')
        user.database.save()
    return HttpResponse('okay')
