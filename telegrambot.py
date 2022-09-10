import telebot
import config
import datacollector
import prediction
from telebot import types

import prediction732

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Live игры", callback_data='getLiveMatches'))
    markup.add(types.InlineKeyboardButton("Maтчи на сегодня", callback_data='getTodayMatches'))

    bot.send_message(message.chat.id, 'Получение списков матчей', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'getLiveMatches':
                markup = types.InlineKeyboardMarkup(row_width=1)
                getmatches = types.InlineKeyboardButton("Назад", callback_data='back')
                live_games = datacollector.get_games("online")
                live_games.update(datacollector.get_games("draft"))
                for match in live_games:
                    markup.add(types.InlineKeyboardButton(match, callback_data=live_games[match]))

                markup.add(getmatches)
                if len(live_games) == 0:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Матчи еще не начались или идет стадия драфтов",
                                          reply_markup=markup)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Выбрать конкретный матч",
                                          reply_markup=markup)
            elif call.data == 'back':
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton("Live игры", callback_data='getLiveMatches'))
                markup.add(types.InlineKeyboardButton("Maтчи на сегодня", callback_data='getTodayMatches'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Получение списков матчей", reply_markup=markup)

            elif call.data == 'getTodayMatches':
                markup = types.InlineKeyboardMarkup(row_width=1)
                getmatches = types.InlineKeyboardButton("Назад", callback_data='back')
                live_games = datacollector.get_games("waiting")
                for match in live_games:
                    markup.add(types.InlineKeyboardButton(match, callback_data='back'))

                markup.add(getmatches)
                if len(live_games) == 0:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="На сегодня матчей нет",
                                          reply_markup=markup)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Матчи на сегодня",
                                          reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                getmatches = types.InlineKeyboardButton("Назад", callback_data='back')
                markup.add(getmatches)
                try:
                    datacollector.get_match_info(call.data)
                    pred = prediction.get_prediction(call.data)
                    pred732 = prediction732.get_prediction(call.data)
                    result = "\nBASE:"\
                        "\ndire_win_probability: " + pred['dire_win_probability'] + \
                        " \nradiant_win_probability: " + pred['radiant_win_probability'] + \
                        "\n7.32:"\
                        "\ndire_win_probability: " + pred732['dire_win_probability'] + \
                         " \nradiant_win_probability: " + pred732['radiant_win_probability'] + \
                         " \ntime: " + str(pred['time'])
                    bot.send_message(chat_id=call.message.chat.id,
                                 text=result,
                                 reply_markup=markup)
                except Exception as e:
                    print(repr(e))
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Матч еще на стадии драфта",
                                  reply_markup=markup)

    except Exception as e:
        print(repr(e))

# RUN
bot.polling(none_stop=True)
