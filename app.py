import telebot
from config import TOKEN, keys
from extensions import ConvException, CurrencyConv

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):

    text_message = '''
    Привет! Для пересчёта валюты введите команду в формате:\n <откуда> <куда> <сколько>\n
Посмотреть доступные валюты: /values'''

    bot.reply_to(message, text_message)

@bot.message_handler(commands=['values'])
def values_message(message: telebot.types.Message):
    text_message = 'Доступные валюты:'
    for key in keys.keys():
        text_message = '\n'.join((text_message, key, ))
    bot.reply_to(message, text_message)

@bot.message_handler(content_types=['text', ])
def conv_message(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvException('Неверные параметры')
        quote, base, amount = values
        total = CurrencyConv.conv(quote, base, amount)
    except ConvException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Программная ошибка:\n{e}')
    else:
        text = f'{float(amount):.2f} {keys[quote]} ({quote}) стоят {total:.2f} {keys[base]} ({base})'
        bot.send_message(message.chat.id, text)

bot.polling()