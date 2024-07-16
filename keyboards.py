from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import *
from config import *

def start_keyboard(UID):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)

	b1 = KeyboardButton('🧮 Открыть меню')
	b2 = KeyboardButton('👑 Админка')

	markup.add(b1)

	if UID in aids:
		markup.add(b2)

	return markup

def menu_keyboard(UID):
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	b = InlineKeyboardButton('💖 Купить доступ', callback_data='buy_access')
	b1 = InlineKeyboardButton('✝️ Запустить бомбер', callback_data='bomber')
	b2 = InlineKeyboardButton('🧬 Мой профиль', callback_data='profile')
	b3 = InlineKeyboardButton('📓 Справочник', callback_data='helper')
	b4 = InlineKeyboardButton('💜 Запущенные бомбера', callback_data='active_bombers')
	b5 = InlineKeyboardButton('🗝 Защита номера', callback_data='whitelist')
	b6 = InlineKeyboardButton('🧲 Информация', callback_data='information')

	if Users.have_sub(UID):
		markup.add(b1)
		markup.add(b2, b3)
		markup.add(b4)
		markup.add(b5, b6)
	else:
		markup.add(b)
		markup.add(b2, b3)
		markup.add(b4)
		markup.add(b5, b6)

	return markup

def methods_pay_keyboard(price):
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	b1 = InlineKeyboardButton('🥝 QiWi', callback_data=f'buy_access:qiwi:{price}')
	b2 = InlineKeyboardButton('🧊 CryptoBot', callback_data=f'buy_access:cryptobot:{price}')
	b3 = InlineKeyboardButton('💢 Вернуться в меню', callback_data='back')

	markup.add(b1)
	markup.add(b2)
	markup.add(b3)

	return markup

def time_sub_keyboard():
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	b1 = InlineKeyboardButton('3 дня', callback_data=f'buy_access_time:80')
	b2 = InlineKeyboardButton('7 дней', callback_data=f'buy_access_time:120')
	b3 = InlineKeyboardButton('14 дней', callback_data=f'buy_access_time:200')
	b4 = InlineKeyboardButton('21 день', callback_data=f'buy_access_time:250')
	b5 = InlineKeyboardButton('30 дней', callback_data=f'buy_access_time:300')
	b6 = InlineKeyboardButton('90 дней', callback_data=f'buy_access_time:700')
	b7 = InlineKeyboardButton('💢 Вернуться в меню', callback_data='back')

	markup.add(b1, b2, b3)
	markup.add(b4, b5, b6)
	markup.add(b7)

	return markup

def admin_keyboard():
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	b1 = InlineKeyboardButton('📧 Рассылка', callback_data='mail')
	b2 = InlineKeyboardButton('💾 Выгрузка БД', callback_data='dump')
	b3 = InlineKeyboardButton('🎁 Выдать доступ', callback_data='givesub')
	b4 = InlineKeyboardButton('🥀 Забрать доступ', callback_data='takesub')

	markup.add(b1)
	markup.add(b2)
	markup.add(b3)
	markup.add(b4)

	return markup

def stop_bomber_keyboard(BID):
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	b1 = InlineKeyboardButton('🛑 Выключить бомбер', callback_data=f'stop_bomber:{BID}')

	markup.add(b1)
	return markup

def cancel_keyboard():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)

	b1 = KeyboardButton('❌ Отмена')

	markup.add(b1)
	return markup

def check_payment_keyboard(invoice_id, pay, days):
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	b1 = InlineKeyboardButton('💱 Проверить оплату', callback_data=f'check_{pay}:{invoice_id}:{days}')
	markup.add(b1)
	return markup

def active_bombers_keyboard(UID):
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	for bomb in Bombs.get_bombs_by_id(UID):
		b = InlineKeyboardButton(f'✝️ #{bomb.BID} {bomb.NUM}', callback_data=f'stop_bomber:{bomb.BID}')
		markup.add(b)

	b = InlineKeyboardButton('💢 Вернуться в меню', callback_data='back')
	markup.add(b)
	return markup

def whitelist_keyboard(UID):
	markup = InlineKeyboardMarkup(resize_keyboard=True)

	for wlist in Whitelist.get_whitelist_by_id(UID):
		b = InlineKeyboardButton(f'🗝 {wlist.NUM}', callback_data=f'delete_whitelist:{wlist.NUM}')
		markup.add(b)

	if Whitelist.get_whitelist_count_by_id(UID) < 5:
		b = InlineKeyboardButton('➕ Защитить номер', callback_data='add_whitelist')
		markup.add(b)

	b = InlineKeyboardButton('💢 Вернуться в меню', callback_data='back')
	markup.add(b)
	return markup

