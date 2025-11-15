class SendMessagesUser:
    @staticmethod
    def ADS_SUBMIT(language):
        if language == 'en':
            return 'Subscribe'
        elif language == 'ru':
            return "Подписываться"
        elif language == 'hy':
            return 'Բաժանորդագրվել'

    @staticmethod
    def outer_message(language):
        if language == 'en':
            return """
Սխալ Որոնում ❗️

Աուդիո և վիդեո որոնելու համար պետք է օգտացործել 👇
@vid կամ @SkachatsYouTubebot

Այսպես 👇
@vid Xcho
@SkachatsYoutubebot Xcho
                """
        elif language == 'ru':
            return """
Սխալ Որոնում ❗️

Աուդիո և վիդեո որոնելու համար պետք է օգտացործել 👇
@vid կամ @SkachatsYouTubebot

Այսպես 👇
@vid Xcho
@SkachatsYoutubebot Xcho
                """
        elif language == 'hy':
            return """
Սխալ Որոնում ❗️

Աուդիո և վիդեո որոնելու համար պետք է օգտացործել 👇
@vid կամ @SkachatsYouTubebot

Այսպես 👇
@vid Xcho
@SkachatsYoutubebot Xcho
            """

    @staticmethod
    def start(language):
        """
в поле "отправить электронное письмо" введите @vid или
@SkachatsYouTubebot и найдите видео:

Например: 👇
@vid Хcho
@SkachatsYouTubebot Xcho
        """
        if language == 'en':
            return ["""
Downloading from YouTube and TikTok 🚀

❗️3 ways to download a song or video from YouTube. 👇

<blockquote>
1. @vid name (song or video)
2. @SkachatsYouTubebot name (song or video)
3. You can simply write the name of the song or video 
</blockquote>

❗️Way to download a song or video from TikTok. 👇

<blockquote>
Just send a link from TikTok. 
</blockquote>

🤖Contact us for any inquiries - @symananger
                    """, "start.jpg"]

        elif language == 'ru':
            return ["""
Загрузка с Youtube и TikTok 🚀

❗️3 Способ загрузить песню и видео с YouTube. 👇

<blockquote>
1. @vid имя (песня или видео)
2. @SkachatsYouTubebot имя (песня или видео)
3. И вы можете просто написать        название песни или видео
</blockquote>

❗️Способ загрузить песню и видео из TikTok. 👇

<blockquote>
Просто отправьте ссылку из TikTok
</blockquote>

🤖Свяжитесь с нами по всем вопросам - @symananger
                    """, "start.jpg"]

        elif language == 'hy':
            return ["""
Ներբեռնում YouTube-ից և TikTok-ից 🚀

❗️3 եղանակ՝ ներբեռնելու երգ կամ վիդեո YouTube-ից։ 👇

<blockquote>
1. @vid անուն (երգ կամ վիդեո)
2. @SkachatsYouTubebot անուն (երգ կամ վիդեո)
3. Կարող եք պարզապես գրել երգի կամ վիդեոյի անունը 
</blockquote>

❗️Երգ կամ վիդեո ներբեռնելու ձև TikTok-ից։ 👇
\n
<blockquote>
Ուղղակի ուղարկեք հղումը TikTok-ից։
</blockquote>

🤖Հարցերի համար կապ հաստատեք մեզ հետ - @symananger
                    """, "start.jpg"]

    @staticmethod
    def help(language):
        if language == 'en':
            return ["""
To learn more - @sy_info 🌐
""", "help_ru.png"]

        elif language == 'ru':
            return ["""
узнать больше - @sy_info 🌐
""", "help_ru.png"]

        elif language == 'hy':
            return ["""
Ավելին իմանալու համար - @sy_info 🌐
""", "help_hy.png"]

    @staticmethod
    def channel_add(language):
        if language == 'en':
            return "Channel is added"
        elif language == 'ru':
            return "Канал добавлен"
        elif language == 'hy':
            return "Ալիքն ավելացված է"

    @staticmethod
    def channel_added(language):
        if language == 'en':
            return "Channel is already added"
        elif language == 'ru':
            return "Канал уже добавлен"
        elif language == 'hy':
            return "Ալիքն արդեն ավելացված է"

    @staticmethod
    def send_video_data(language):
        if language == 'ru':
            return """
{title}
{loading_bar}
✅  144p: слабый
✅  360p: слабый
🚀  480p: нормальный
⚡️  720p: высокий
⚡️ 1080p: очень высокий

возможности загрузки ↓
"""
        elif language == 'hy':
                return """
{title}
{loading_bar}
✅  144p: թույլ
✅  360p: թույլ
🚀  480p: նորմալ
⚡️  720p: բարձր
⚡️ 1080p: շատ բարձր

ներբեռնման հնարավորություններ ↓
"""
        else:
            return """
{title}
{loading_bar}
✅  144p: weak
✅  360p: weak
🚀  480p: normal
⚡️  720p: high
⚡️ 1080p: very high

download options ↓
"""

    @staticmethod
    def send_video_data_is_loading_now(language):
        if language == 'ru':
            return """
{title}
{loading_bar}
✅  144p: слабый
✅  360p: слабый
🚀  480p: нормальный
⚡️  720p: высокий
⚡️ 1080p: очень высокий
"""
        elif language == 'hy':
            return """
{title}
{loading_bar}
✅  144p: թույլ
✅  360p: թույլ
🚀  480p: նորմալ
⚡️  720p: բարձր
⚡️ 1080p: շատ բարձր
"""
        else:
            return """
{title}
{loading_bar}
✅  144p: weak
✅  360p: weak
🚀  480p: normal
⚡️  720p: high
⚡️ 1080p: very high
"""

    @staticmethod
    def sending_loading(language):
        if language == "en":
            return ["loading", "sending"]
        elif language == "ru":
            return ["скачивание", "отправка"]
        else:
            return ["ներբեռնում", 'փոխանցում']

    @staticmethod
    def back_to_menu(language):
        if language == "en":
            return "back "
        elif language == "ru":
            return "назад "
        else:
            return "հետ "
    @staticmethod
    def send_effects_edit(data, language):
        if language == 'en':
            return f'''
🚫 Our editor is not working at this moment

〢 Echo - {data.get('reverb') or 0}
〢 Bass - {data.get('bass') or 0}
〢 8D effect - {data.get('effect_8d') or 0}
〢 Sound pitch - {data.get('pitch') or 0}
〢 Speed - {data.get('speed') or 0}
'''
        elif language == 'ru':
            return f'''
🚫 Наш эдитор сейчас не работает

〢 Эхо - {data.get('reverb') or 0}
〢 Басс - {data.get('bass') or 0}
〢 8D эффект - {data.get('effect_8d') or 0}
〢 Высота звука - {data.get('pitch') or 0}
〢 Скорость - {data.get('speed') or 0}
'''
        elif language == 'hy':
            return f'''
🚫 Այս պահին մեր էդիթորը չի աշխատում

〢 Արձագանք - {data.get('reverb') or 0}
〢 Բաս - {data.get('bass') or 0}
〢 8D էֆֆեկտ - {data.get('effect_8d') or 0}
〢 Ձայնի բարձրություն - {data.get('pitch') or 0}
〢 Արագություն - {data.get('speed') or 0}
'''


    @staticmethod
    def send_effects_edit_help(language):
        if language == 'en':
            return '''
Try out a tool to better understand how it works.

∵Changing the echo
With this tool, you can change the echo of a song.

∴ Bass boost
This tool allows you to enhance the bass of the song.

∵ Changing the pitch of the sound
This tool allows you to change the pitch of a song (pitching the sound, making the sound higher or lower).

∴ Changing the 8D effect
This tool makes the song more realistic.

∵ Changing the audio speed
With this tool, you can speed up or slow down the music.

After clicking the "✅ Confirm" button, the bot will send you a new audio file with your changes.
'''
        elif language == 'ru':
            return '''
Испробуй инструмент для лучшего понимания его работы.

∵ Изменение эхо
С помощью этого инструмента ты можешь изменить эхо песни.

∴ Усиление баса
Данный инструмент позволяет усилить бас песни.

∵ Изменение высоты звука
Данный инструмент позволяет менять высоту песни (питчинг звука, сделать звук выше или ниже).

∴ Изменение 8D эффекта
Этот инструмент делает музыку реалистичнее.

∵ Изменение скорости аудио
С помощью этого инструмента можешь ускорить или замедлить музыку.

После нажатия кнопки "✅ Подтвердить" бот отправит тебе новый аудифайл с твоими изменениями.
            '''
        elif language == 'hy':
            return '''
Օգտագործիր գործիքը, որպեսզի հասկանաս ինչպես է այն աշխատում։

∵ Արձագանքի փոփոխություն
Այս գործիքի միջոցով կարող ես փոխել երգի արձագանքը։

∴ Բասի ուժգնություն
Այս գործիքը թույլ է տալիս ուժեղացնել երգի բասը։

∵ Երաժշտության ձայնի փոփոխություն
Այս գործիքը թույլ է տալիս փոփոխել ձայնի բարձրությունը (Փիթչինգ, դարձնել այն ավելի ցածր կամ բարձր).

∴ 8D էֆֆեկտի փոփոխություն
Այս գործիքը դարձնում է երգն ավելի իրական։

∵ Երաժշտության արագություն
Այս գործիքը թույլ է տալիս փոփոխել երաժշտության արագությունը (Դարձնել այն ավելի արագ կամ դանդաղ)

Սեղմելով "✅ Հաստատել" բոտը կուղարկի նոր աուդիո ֆայլ ձեր փոփոխություններով։
            '''

    @staticmethod
    def send_effect_edit_instruction(language):
        if language == 'en':
            return '''
🔊 By pressing the desired button you can magnify the echo.

To cancel changes, click on the button "🚫".
                    '''
        elif language == 'ru':
            return '''
🔊 Нажав на желаемую кнопки ты можешь увеличивать эхо.

Для отмены изменений нажмите на кнопку "🚫".
                    '''
        elif language == 'hy':
            return '''
🔊 Սեղմելով ցանկալի կոճակը կարող ես ավելացնել արձագանքը.

Փոփոխությունները չեղարկելու համար սեղմեք կոճակը "🚫".
                    '''

    @staticmethod
    def loading(emojis, language):
        if language == 'en':
            return f" Video is uploading {emojis}"
        elif language == 'ru':
            return f"Видео загружается {emojis}"
        elif language == 'hy':
            return f"Տեսանյութը ներբեռնվում է {emojis}"

    @staticmethod
    def language(language):
        if language == 'en':
            return "Choose a language"
        elif language == 'ru':
            return "Выберите язык"
        elif language == 'hy':
            return "Ընտրեք լեզուն"

    @staticmethod
    def channel(language):
        if language == 'en':
            return """
Привет, дорогой подписчик. 🤖

На этом канале мы будем держать вас в курсе событий, связанных с ботом 🌐      
            """
        elif language == 'ru':
            return """
Привет, дорогой подписчик. 🤖

На этом канале мы будем держать вас в курсе событий, связанных с ботом 🌐
            """
        elif language == 'hy':
            return """
Привет, дорогой подписчик. 🤖

На этом канале мы будем держать вас в курсе событий, связанных с ботом 🌐
            """

    @staticmethod
    def change_language(language_p, language):
        if language == 'en':
            return f"You've changed the language to {language_p}"
        elif language == 'ru':
            return f"Вы изменили язык на {language_p}"
        elif language == 'hy':
            return f"Դուք փոխել եք լեզուն {language_p}"

    @staticmethod
    def follow_tg_channel(language):
        if language == 'en':
            return f"""
Please subscribe to this channel to use the bot
                    """

        elif language == 'ru':
            return f"""
Пожалуйста, подпишитесь на этот канал, чтобы использовать бота
                    """

        elif language == 'hy':
            return f"""
Խնդրում ենք բաժանորդագրվել այս ալիքին, որպեսզի օգտվեք բոտից
                    """
    @staticmethod
    def not_follow_channel(language):
        if language == 'en':
            return '''You don't have any channels that you subscribe to, send a link to the video to subscribe and click '''
        elif language == 'ru':
            return '''У вас нет каналов, на которые вы подписаны, отправьте ссылку на видео, чтобы подписаться, и нажмите '''
        elif language == 'hy':
            return '''Դուք չունեք ալիքներ, որոնց հետևում եք, հետևելու համար ուղարկեք տեսանյութի հղումը և սեղմեք '''

    @staticmethod
    def send_audio(language):
        if language == 'en':
            return '''<a href="https://t.me/SkachatsYouTubebot">🤖 The bot that downloads videos and songs from TikTok and YouTube.</a>'''
        elif language == 'ru':
            return '''<a href="https://t.me/SkachatsYouTubebot">🤖 Бот, который загружает видео и песни из TikTok и YouTube.</a>'''
        elif language == 'hy':
            return '''<a href="https://t.me/SkachatsYouTubebot">🤖 Բոտ որը ներբերնում է վիդեո և երգ TikTok - ից և Youtube - ից:</a>'''

    @staticmethod
    def send_video(language):
        if language == 'en':
            return '''
<a href="https://t.me/SkachatsYouTubebot">🤖 The bot that downloads videos and songs from TikTok and YouTube.</a>

back to menu ↓
'''
        elif language == 'ru':
            return '''
<a href="https://t.me/SkachatsYouTubebot">🤖 Бот, который загружает видео и песни из TikTok и YouTube.</a>

назад на меню ↓
'''
        elif language == 'hy':
            return '''
<a href="https://t.me/SkachatsYouTubebot">🤖 Բոտ որը ներբերնում է վիդեո և երգ TikTok-ից և Youtube-ից:</a>

հետ դեպի մենյու ↓
'''

    def send_video_tiktok(language):
        if language == 'en':
            return '''
<a href="https://t.me/SkachatsYouTubebot">🤖 The bot that downloads videos and songs from TikTok and YouTube.</a>

download the audio recording ↓
'''
        elif language == 'ru':
            return '''
<a href="https://t.me/SkachatsYouTubebot">🤖 Бот, который загружает видео и песни из TikTok и YouTube.</a>

скачать аудиозапись ↓
'''
        elif language == 'hy':
            return '''
<a href="https://t.me/SkachatsYouTubebot">🤖 Բոտ որը ներբերնում է վիդեո և երգ TikTok-ից և Youtube-ից:</a>

ներբեռնել աուդիո ձայնագրությունը ↓
'''

    @staticmethod
    def send_transcription(language):
        if language == 'en':
            return "The function is not working at the moment"
        elif language == 'ru':
            return "В данный момент функция не работает"
        elif language == 'hy':
            return "Այս պահին ֆունկցիան չի գործում"


    @staticmethod
    def send_search(language):
        if language == 'en':
            return "in the field, respond to the @vid or @SkachatsYouTubebot community request and find the video ‼️‼️"
        elif language == 'ru':
            return "в поле отправить сообщение напишите @vid или @SkachatsYouTubebot и найдите видео ‼️‼️"
        elif language == 'hy':
            return "նամակ ուղարկելու դաշտում գրեք @vid կամ @SkachatsYouTubebot և փնտրեք վիդեոն ‼️‼️"


    @staticmethod
    def send_video_region_error(language):
        if language == 'en':
            return "this youtube video is unavailable. it could be visibility or region restricted. try another one!"
        elif language == 'ru':
            return "это видео недоступно на YouTube. возможно, оно недоступно для просмотра или ограничено в регионе. попробуйте другое!"
        elif language == 'hy':
            return "այս տեսանյութը հասանելի չէ YouTube-ում: հնարավոր է, որ այն տեսանելի չէ կամ սահմանափակ է տարածաշրջանում: փորձեք մեկ այլ!"

    @staticmethod
    def send_search_error(language):
        if language == 'en':
            return """
There is an error in your search ❗
Try again 🔁
            """
        elif language == 'ru':
            return """
В вашем поиске ошибка ❗️
Попробуйте еще раз 🔁
            """
        elif language == 'hy':
            return """
Ձեր որոնման մեջ կա սխալ ❗️
փորձեք կրկին 🔁
            """

    @staticmethod
    def download_process(language, type_d):
        if language == 'en' and type_d == "video":
            return ["Download", "MB", "Sending video, wait"]
        elif language == 'ru' and type_d == "video":
            return ["Загрузка", "МБ", "Отправлю видео, подождите"]
        elif language == 'hy' and type_d == "video":
            return ["Ներբեռնում", "ՄԲ", "Ուղարկում եմ տեսանյութը, սպասեք"]

        if language == 'en' and type_d == "audio":
            return ["Download", "MB", "Sending audio, wait"]
        elif language == 'ru' and type_d == "audio":
            return ["Загрузка", "МБ", "Отправлю аудио, подождите"]
        elif language == 'hy' and type_d == "audio":
            return ["Ներբեռնում", "ՄԲ", "Ուղարկում եմ աուդիոն, սպասեք"]

        if language == 'en' and type_d == "text":
            return ["Download", "MB", "Sending text, wait"]
        elif language == 'ru' and type_d == "text":
            return ["Загрузка", "МБ", "Отправлю текст, подождите"]
        elif language == 'hy' and type_d == "text":
            return ["Ներբեռնում", "ՄԲ", "Ուղարկում եմ տեկստը, սպասեք"]

class SendKeyboardsName:
    @staticmethod
    def start(language):
        if language == 'en':
            return ['news YoutubeBot 🌐', "Subscribe to channel 🔔"]
        elif language == 'ru':
            return ['новости YoutubeBot 🌐', "Подписаться на канал 🔔"]
        elif language == 'hy':
            return ['Նորություները YoutubeBot - ի', "Բաժանորդագրվել ալիքին 🔔"]

    @staticmethod
    def back_to_main(language):
        if language == 'en':
            return "back"
        elif language == 'ru':
            return "назад"
        elif language == 'hy':
            return "հետ"
    @staticmethod
    def edit_mp3(language):
        if language == 'en':
            return '⚙️ Change'
        elif language == 'ru':
            return '⚙️ Изменить'
        elif language == 'hy':
            return '⚙️ Փոխել'

    @staticmethod
    def audio_edit_buttons(language):
        if language == 'en':
            return ['❔Help', '🔊 Echo', '🎧 8D effect', '🎸 Bass', '🎵 Sound pitch', '🕔 Speed', '✅ Approve']
        elif language == 'ru':
            return ['❔ Помощь', '🔊 Эхо', '🎧 8D эффект', '🎸 Басс', '🎵 Высота звука', '🕔 Скорость',
                    '✅ Подтвердить']
        elif language == 'hy':
            return ['❔ Օգնություն', '🔊 Արձագանք', '🎧 8D էֆֆեկտ', '🎸 Բաս', '🎵 Ձայնի բարձրություն',
                    '🕔 Արագություն', '✅ Հաստատել']

    @staticmethod
    def back(language):
        if language == 'en':
            return '◀️ Back'
        elif language == 'ru':
            return '◀️ Назад'
        elif language == 'hy':
            return '◀️ Հետ'

    @staticmethod
    def follow(language):
        if language == 'en':
            return ['notif', 'delete 🗑', 'next ▶️']
        elif language == 'ru':
            return ['notif', 'delete 🗑', 'next ▶️']
        elif language == 'hy':
            return ['notif', 'delete 🗑', 'next ▶️']

    @staticmethod
    def music(language):
        if language == 'en':
            return "Free Music 🚀"
        elif language == 'ru':
            return "Бесплатная музыка 🚀"
        elif language == 'hy':
            return "Անվճար երաժշտություն 🚀"
