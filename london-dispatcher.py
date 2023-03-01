# nohup python3 london-dispatcher.py > logs-dispatcher 2>&1 &

from env import REDIS_CLIENT, ADMIN_CHAT_ID, TOKEN, Params
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
  Application,
  CommandHandler,
  ContextTypes,
  ConversationHandler,
  MessageHandler,
  filters,
)
from utils import getParamKey, getChatParams, addChat, deleteChat


async def logStatus(context, text):
  await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  username = update.message.from_user.first_name
  WELCOME_TEXT = '''Hi, {}\! I will do my best to help you find a flat in London\. 
Are you looking flat *to rent* or *for sale*\?'''.format(username)

  reply_keyboard = [["to-rent", "for-sale"]]

  await update.message.reply_text(
    WELCOME_TEXT,
    parse_mode='MarkdownV2',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                     one_time_keyboard=True,
                                     input_field_placeholder="to-rent"),
  )

  return Params.FLAT_TYPE.value


async def flatType(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  chat_id = update.message.chat.id
  flat_type = update.message.text
  if flat_type not in ['to-rent', 'for-sale']:
    return Params.FLAT_TYPE.value

  REDIS_CLIENT.set(getParamKey(chat_id, Params.FLAT_TYPE), flat_type)

  reply_keyboard = [["0", "1", "2", "3", "4"]]
  await update.message.reply_text(
    "Enter the minimum number of bedrooms",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                     one_time_keyboard=True,
                                     input_field_placeholder="0"),
  )

  return Params.MINBEDS.value


async def minBeds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  chat_id = update.message.chat.id
  min_beds = update.message.text
  if not min_beds.isnumeric() or int(min_beds) > 4:
    return Params.MINBEDS.value

  REDIS_CLIENT.set(getParamKey(chat_id, Params.MINBEDS), min_beds)

  await update.message.reply_text("Enter the minimum price in £",
                                  reply_markup=ReplyKeyboardRemove())

  return Params.MINPRICE.value


async def minPrice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  chat_id = update.message.chat.id
  min_price = update.message.text
  if not min_price.isnumeric():
    return Params.MINPRICE.value

  REDIS_CLIENT.set(getParamKey(chat_id, Params.MINPRICE), min_price)

  await update.message.reply_text("Enter the maximum price in £")

  return Params.MAXPRICE.value


async def maxPrice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  chat_id = update.message.chat.id
  max_price = update.message.text
  if not max_price.isnumeric():
    return Params.MAXPRICE.value

  REDIS_CLIENT.set(getParamKey(chat_id, Params.MAXPRICE), max_price)

  await update.message.reply_text('''Enter the districts\. For example\:
_islington, angel, kensington, chelsea, notting\-hill, wapping, mayfair, soho, covent\-garden, hampstead, belgravia, battersea, old\-street, n1, ec1v_''',
                                  parse_mode='MarkdownV2')

  return Params.DISTRICTS.value


async def districts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  username = update.message.from_user.username
  chat_id = update.message.chat.id
  districts = update.message.text
  REDIS_CLIENT.set(getParamKey(chat_id, Params.DISTRICTS), districts)
  addChat(chat_id)
  await logStatus(
    context, 'Add bot for @{}, chat_id: {}, params: {}'.format(
      username, chat_id, str(getChatParams(chat_id))))

  await update.message.reply_text(
    "Perfect! The bot is set. You will get the first flats in 10 minutes.")

  return ConversationHandler.END


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  username = update.message.from_user.username
  chat_id = update.message.chat.id
  deleteChat(chat_id)
  await logStatus(context,
                  'Remove bot for @{}, chat_id: {}'.format(username, chat_id))
  await update.message.reply_text("Hope to see you again. Have a great day!",
                                  reply_markup=ReplyKeyboardRemove())

  return ConversationHandler.END


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # update_str = str(update.to_dict()) if isinstance(update,
  #                                                  Update) else str(update)
  print(context.chat_data(), context.user_data(), context.error)
  # await logStatus(
  #   context, '[ERROR] {}: {}, {}, {}'.format(update_str, context.error,
  #                                            str(context.chat_data()),
  #                                            str(context.user_data())))


application = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
  entry_points=[CommandHandler("start", start),
                CommandHandler("stop", stop)],
  states={
    Params.FLAT_TYPE.value: [MessageHandler(filters.ALL, flatType)],
    Params.MINBEDS.value: [MessageHandler(filters.ALL, minBeds)],
    Params.MINPRICE.value: [MessageHandler(filters.ALL, minPrice)],
    Params.MAXPRICE.value: [MessageHandler(filters.ALL, maxPrice)],
    Params.DISTRICTS.value: [MessageHandler(filters.ALL, districts)],
  },
  fallbacks=[CommandHandler("stop", stop)],
  allow_reentry=True,
)

application.add_handler(conv_handler)
application.add_error_handler(error)

application.run_polling()
