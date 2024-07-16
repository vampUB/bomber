import asyncio
from pyqiwip2p import QiwiP2P
from aiogram.dispatcher import FSMContext
from aiocryptopay.const import InvoiceStatus
from aiogram.utils.exceptions import Throttled
from aiocryptopay import AioCryptoPay, Networks
from aiogram import Bot, Dispatcher, executor, types
# from pyqiwip2p.types import QiwiCustomer, QiwiDatetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from states import *
from bomber import *
from database import *
from keyboards import *

p2p = QiwiP2P(auth_key=QIWIP2P_TOKEN)
crypto = AioCryptoPay(token=CRYPTOPAY_TOKEN, network=Networks.MAIN_NET)
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=storage)

obj = Bomber()
# obj.loadServices()
ua_services_count = len(obj.servicesList[0])
ru_services_count = len(obj.servicesList[1])
all_services_count = ua_services_count + ru_services_count

subs = {
    80: 3,
    120: 7,
    200: 14,
    250: 21,
    300: 30,
    700: 90
}

async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer('❗️ Пожалуйста, не флудите!')

@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood, rate=1)
async def start(message: types.Message):
    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEJjSlkoEihmAAB4-w84tUzDBjiLWxsvewAAmQ6AALgo4IH_LAjcdV4gS0vBA')
    if not Users.user_exists(message.from_user.id):
        Users.create_user(message.from_user.id)
        await bot.send_message(logs_id, f'''<b>👤 Новый пользователь
🆔:</b> <code>{message.from_user.id}</code>
<b>🔗 Линк:</b> {message.from_user.get_mention()}''')
    await message.answer(f'''<b>🟪Welcome to the club!⬜️
<i>Используй кнопки, чтобы управлять ботом:</i></b>''', reply_markup=start_keyboard(message.from_user.id))

@dp.message_handler(text='👑 Админка')
@dp.throttled(anti_flood, rate=1)
async def admin(message: types.Message):
    if message.from_user.id in aids:
        await message.answer(f'''<b>👮‍♂️ Админ-панель

👥 Пользователей в боте:</b> <code>{Users.get_users_count()}</code>
<b>🤵🏼‍♂️ С доступом:</b> <code>{Users.get_subs_count()}</code>
<b>💣 Сейчас запущено бомберов:</b> <code>{Bombs.get_bombs_count()}</code>''', reply_markup=admin_keyboard())

@dp.message_handler(text='🧮 Открыть меню')
async def open_menu(message: types.Message):
    await message.answer('<b>🔯 Меню:</b>', reply_markup=menu_keyboard(message.from_user.id))

@dp.callback_query_handler(text='bomber')
@dp.throttled(anti_flood, rate=1)
async def bomber(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if not Users.have_sub(callback_query.from_user.id):
        await callback_query.message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        if Bombs.get_bombs_count_by_id(callback_query.from_user.id) == 3:
            await callback_query.message.answer(f'<b>❗️ У вас уже запущено 3 бомбера! Остановите их или дождитесь окончания циклов.</b>', reply_markup=start_keyboard(message.from_user.id))
        else:
            await callback_query.message.answer(f'<b>📞 Введите номер телефона без +</b>', reply_markup=cancel_keyboard())
            await StartBomber.number.set()

@dp.message_handler(state=StartBomber.number)
@dp.throttled(anti_flood, rate=1)
async def bomber_1(message: types.Message, state: FSMContext):
    if not Users.have_sub(message.from_user.id):
        await state.finish()
        await message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=start_keyboard(message.from_user.id))
    else:
        number = message.text

        if (number.startswith('380') and len(number) == 12) or (number.startswith('7') and len(number) == 11):
            if Whitelist.in_whitelist(number):
                await state.finish()
                await message.answer(f'<b>❗️ Номер защищен. На него нельзя запустить спам!</b>', reply_markup=start_keyboard(message.from_user.id))
                return

            async with state.proxy() as data:
                data['number'] = number

            await message.answer(f'<b>🟣 Введите количество циклов:</b>', reply_markup=cancel_keyboard())
            await StartBomber.next()
        else:
            await state.finish()
            await message.answer(f'<b>❗️ Номер должен быть без + в начале и иметь код страны 7 ил 380!</b>', reply_markup=start_keyboard(message.from_user.id))

@dp.message_handler(state=StartBomber.iterations)
async def bomber_2(message: types.Message, state: FSMContext):
    if not Users.have_sub(message.from_user.id):
        await state.finish()
        await message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=start_keyboard(message.from_user.id))
    else:
        iterations = message.text

        if (iterations.isdigit() and int(iterations) < 100 and int(iterations) > 0):
            async with state.proxy() as data:
                number = data['number']
                data['iterations'] = int(iterations)

            await state.finish()
            bomb_id = ''.join([random.choice(list('QAZWSXEDCRFVTGBYHNUJMIKOLP1029384756')) for x in range(6)])
            await bot.send_message(logs_id, f'''<b>💣 <a href="tg://user?id={message.from_user.id}">Пользователь</a> (@{message.from_user.username}) заказал бомбер на номер: {number}

🌀 Циклы: {iterations}</b>''')
            await message.answer(f'''<b>✝️ Бомбер запущен! #{bomb_id}

📞 Номер телефона:</b> <code>{number}</code>
<b>🟣 Кол-во циклов:</b> <code>{iterations}</code>

<b>❗️ Вам прийдёт сообщение об окончании спама!</b>''', reply_markup=stop_bomber_keyboard(bomb_id))
            Bombs.create_bomb(message.from_user.id, bomb_id, number, int(iterations))
            if number.startswith('380'):
                await asyncio.create_task(obj.runUA(bot, bomb_id, Bombs))
            elif number.startswith('7'):
                await asyncio.create_task(obj.runRU(bot, bomb_id, Bombs))
        else:
            await state.finish()
            await message.answer(f'<b>❗️ Количество циклов должно быть числом и не быть больше 100!</b>', reply_markup=start_keyboard(message.from_user.id))

@dp.callback_query_handler(text_startswith='buy_access:')
@dp.throttled(anti_flood, rate=1)
async def buy_access_payment(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if not Users.have_sub(callback_query.from_user.id):
        amount = int(callback_query.data.split(':')[2])
        days = subs[amount]

        if callback_query.data.split(':')[1] == "cryptobot":
            amount_final = amount / curse_usdt
            invoice = await crypto.create_invoice(asset='USDT', amount=amount_final)
            url = invoice.pay_url

            await callback_query.message.answer(f'''<b>💖 Чтобы получить доступ - оплатите счёт на {amount} RUB ({amount_final} USDT)

📌 Ссылка на оплату: {url}
❗️ После проведения оплаты, нажмите на "Проверить оплату"</b>''', reply_markup=check_payment_keyboard(invoice.invoice_id, callback_query.data.split(':')[1], days))
        else:
            bill = p2p.bill(amount=amount, lifetime=15, comment="Покупка доступа к боту")
            url = bill.pay_url

            await callback_query.message.answer(f'''<b>💖 Чтобы получить доступ - оплатите счёт на {amount} RUB

📌 Ссылка на оплату: {url}
❗️ После проведения оплаты, нажмите на "Проверить оплату"</b>''', reply_markup=check_payment_keyboard(bill.bill_id, callback_query.data.split(':')[1], days))
    else:
        await callback_query.message.answer(f'<b>❗️ У вас уже имеется доступ, используйте кнопки:</b>', reply_markup=start_keyboard(message.from_user.id))

@dp.callback_query_handler(text_startswith='buy_access_time:')
async def buy_access_time(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f'<b>👾 Выберите метод покупки доступа:</b>', reply_markup=methods_pay_keyboard(callback_query.data.split(':')[1]))

@dp.callback_query_handler(text='buy_access')
async def buy_access(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f'<b>👾 Выберите время подписки:</b>', reply_markup=time_sub_keyboard())

@dp.callback_query_handler(text_startswith='stop_bomber:')
async def stop_bomber(callback_query: types.CallbackQuery):
    Bombs.get_bomb(callback_query.data.split(':')[1]).delete_instance()
    await callback_query.message.answer(f'<b>✅ Бомбер был остановлен!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text_startswith='delete_whitelist:')
async def stop_bomber(callback_query: types.CallbackQuery):
    Whitelist.get_whitelist(callback_query.data.split(':')[1]).delete_instance()
    await callback_query.message.answer(f'<b>✅ Номер был убран!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))




@dp.callback_query_handler(text='add_whitelist')
@dp.throttled(anti_flood, rate=1)
async def add_whitelist(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if not Users.have_sub(callback_query.from_user.id):
        await callback_query.message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        if Whitelist.get_whitelist_count_by_id(callback_query.from_user.id) == 5:
            await callback_query.message.answer(f'<b>❗️ У вас уже защищено 5 номера! Удалите один из защищенных чтобы добавить новый.</b>', reply_markup=start_keyboard(message.from_user.id))
        else:
            await callback_query.message.answer(f'<b>📞 Введите номер телефона без +</b>', reply_markup=cancel_keyboard())
            await AddWhitelist.number.set()

@dp.message_handler(state=AddWhitelist.number)
@dp.throttled(anti_flood, rate=1)
async def add_whitelist_1(message: types.Message, state: FSMContext):
    if not Users.have_sub(message.from_user.id):
        await state.finish()
        await message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=start_keyboard(message.from_user.id))
    else:
        number = message.text

        if (number.startswith('380') and len(number) == 12) or (number.startswith('7') and len(number) == 11):
            if Whitelist.in_whitelist(number):
                await state.finish()
                await message.answer(f'<b>❗️ Номер уже защищен. Его нельзя добавить!</b>', reply_markup=start_keyboard(message.from_user.id))
                return

            async with state.proxy() as data:
                data['number'] = number

            Whitelist.create_whitelist(message.from_user.id, number)
            await message.answer(f'<b>✅ Номер успешно защищен.</b>', reply_markup=whitelist_keyboard(message.from_user.id))
            await state.finish()
        else:
            await state.finish()
            await message.answer(f'<b>❗️ Номер должен быть без + в начале и иметь код страны 7 ил 380!</b>', reply_markup=start_keyboard(message.from_user.id))




@dp.callback_query_handler(text='active_bombers')
@dp.throttled(anti_flood, rate=1)
async def active_bombers(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if not Users.have_sub(callback_query.from_user.id):
        await callback_query.message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        if Bombs.get_bombs_count_by_id(callback_query.from_user.id) == 0:
            await callback_query.message.answer(f'<b>❗️ У вас нет запущенных бомберов!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
        else:
            await callback_query.message.answer(f'<b>🛑 Выберите бомбер, который хотите завершить:</b>', reply_markup=active_bombers_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text='whitelist')
@dp.throttled(anti_flood, rate=1)
async def whitelist(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if not Users.have_sub(callback_query.from_user.id):
        await callback_query.message.answer(f'<b>❗️ Для продолжения оплатите доступ!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        await callback_query.message.answer(f'<b>🛑 Выберите номер, который хотите убрать из защиты:</b>', reply_markup=whitelist_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text='profile')
@dp.throttled(anti_flood, rate=1)
async def profile(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    if not Users.have_sub(callback_query.from_user.id):
        await callback_query.message.answer(f'''<b>🆔 Ваш идентификатор:</b> <code>{callback_query.from_user.id}</code>

<b>💖 Доступ:</b> <code>отсутствует</code>''', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        await callback_query.message.answer(f'''<b>🆔 Ваш идентификатор:</b> <code>{callback_query.from_user.id}</code>

<b>💖 Доступ заканчивается в:</b> <code>{Users.sub_until(callback_query.from_user.id)}</code>''', reply_markup=menu_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text='helper')
@dp.throttled(anti_flood, rate=1)
async def helper(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer(f'''<b>🔯 Сайтов в базе:</b> <code>{all_services_count} (🇺🇦{ua_services_count} / 🇷🇺{ru_services_count})</code>

<b>✝️ Для запуска бомбера, воспользуйтесь кнопкой "Запустить бомбер"

📞 Затем вводите желаемый номер телефона, на который будет запущен бомбер (поддержка кодов 7, 380)

🟣 Затем укажите количество циклов. Цикл будет длится около 3-5 минут.

❗️ Хочу подметить то, что некоторые сервисы могут не работать! 

⁉️ Если у вас возникли вопросы, то пишите @axolotl_admin</b>''', reply_markup=menu_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text='information')
@dp.throttled(anti_flood, rate=1)
async def information(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer(f'''<b>⛑ Администратор: @axolotl_admin
⛩ Канал с новостями: @axolotl_admin</b>''', reply_markup=menu_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text='back')
@dp.throttled(anti_flood, rate=1)
async def back(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEJjSlkoEihmAAB4-w84tUzDBjiLWxsvewAAmQ6AALgo4IH_LAjcdV4gS0vBA')
    await callback_query.message.answer(f'''<b>🟪Welcome to the Axolotl Bomber!⬜️
<i>Используй кнопки, чтобы управлять ботом:</i></b>''', reply_markup=start_keyboard(message.from_user.id))


@dp.callback_query_handler(text_startswith='check_cryptobot:')
@dp.throttled(anti_flood, rate=1)
async def check_cryptobot(callback_query: types.CallbackQuery):
    if not Users.have_sub(callback_query.from_user.id):
        invoices = await crypto.get_invoices(invoice_ids=callback_query.data.split(':')[1])
        if invoices[0].status == InvoiceStatus.PAID:
            await callback_query.message.delete()
            Users.give_sub(callback_query.from_user.id, int(callback_query.data.split(':')[2]))
            await bot.send_message(logs_id, f'''<b>💣 <a href="tg://user?id={message.from_user.id}">Пользователь</a> (@{message.from_user.username}) купил доступ

💈 Метод: CryptoBot</b>''')
            await callback_query.message.answer(f'<b>💗 Доступ оплачен. Приятного пользования!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
        elif invoices[0].status == InvoiceStatus.ACTIVE:
            await callback_query.answer(f'❗️ Доступ не оплачен!')
        else:
            await callback_query.message.delete()
            await callback_query.message.answer(f'<b>💘 Платёж больше не активен!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        await callback_query.message.answer(f'<b>❗️ У вас уже имеется доступ, используйте кнопки:</b>', reply_markup=menu_keyboard(callback_query.from_user.id))

@dp.callback_query_handler(text_startswith='check_qiwi:')
@dp.throttled(anti_flood, rate=1)
async def check_qiwi(callback_query: types.CallbackQuery):
    if not Users.have_sub(callback_query.from_user.id):
        status = p2p.check(callback_query.data.split(':')[1]).status
        if status == 'PAID':
            await callback_query.message.delete()
            Users.give_sub(callback_query.from_user.id, int(callback_query.data.split(':')[2]))
            await bot.send_message(logs_id, f'''<b>💣 <a href="tg://user?id={message.from_user.id}">Пользователь</a> (@{message.from_user.username}) купил доступ

💈 Метод: 🥝 QiWi</b>''')
            await callback_query.message.answer(f'<b>💗 Доступ оплачен. Приятного пользования!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
        elif status == 'WAITING':
            await callback_query.answer(f'❗️ Доступ не оплачен!')
        else:
            await callback_query.message.delete()
            await callback_query.message.answer(f'<b>💘 Платёж больше не активен!</b>', reply_markup=menu_keyboard(callback_query.from_user.id))
    else:
        await callback_query.message.answer(f'<b>❗️ У вас уже имеется доступ, используйте кнопки:</b>', reply_markup=menu_keyboard(callback_query.from_user.id))


@dp.callback_query_handler(text='dump')
@dp.throttled(anti_flood, rate=1)
async def dump(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in aids:
        await bot.send_document(callback_query.from_user.id, open('bot.db', 'rb'))

@dp.callback_query_handler(text='mail')
@dp.throttled(anti_flood, rate=1)
async def mail(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in aids:
        await Mail.photo.set()
        await callback_query.message.answer('''<b>📷 Загрузите фото рассылки

<i>Для пропуска напишите "-"</i></b>''')

@dp.message_handler(content_types=['photo'], state=Mail.photo)
async def mail2(message: types.Message, state: FSMContext):
    if message.from_user.id in aids:
        async with state.proxy() as data:
            try:
                data['photo'] = message.photo[0].file_id
            except:
                data['photo'] = None
        
        await Mail.next()
        await message.answer('''<b>✉️ Теперь введите текст рассылки

<i>Поддержка разметки "HTML"</i></b>''')

@dp.message_handler(state=Mail.photo)
async def mail2(message: types.Message, state: FSMContext):
    if message.from_user.id in aids:
        async with state.proxy() as data:
            try:
                data['photo'] = message.photo[0].file_id
            except:
                data['photo'] = None
        
        await Mail.next()
        await message.answer('''<b>✉️ Теперь введите текст рассылки

<i>Поддержка разметки "HTML"</i></b>''')

@dp.message_handler(state=Mail.description)
async def mail3(message: types.Message, state: FSMContext):
    if message.from_user.id in aids:
        async with state.proxy() as data:
            data['description'] = message.text 

            g, e = 0, 0
            for user in Users.get_users():
                try:
                    await bot.send_photo(user.UID, data['photo'], data['description'], parse_mode='html')
                    g += 1
                except:
                    try:
                        await bot.send_message(user.UID, data['description'], parse_mode='html')
                        g += 1
                    except:
                        e += 1

        await state.finish()
        await message.answer(f'''<b>⏱ Рассылка окончена!

👍 Получили сообщение:</b> <code>{g}</code>
<b>👎 Не получили:</b> <code>{e}</code>''', reply_markup=admin_keyboard())

@dp.callback_query_handler(text='givesub')
@dp.throttled(anti_flood, rate=1)
async def givesub(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in aids:
        await callback_query.message.answer('<b>🆔 Введите ID пользователя которому хотите выдать доступ:</b>', reply_markup=cancel_keyboard())
        await GiveSub.id.set()

@dp.callback_query_handler(text='takesub')
@dp.throttled(anti_flood, rate=1)
async def takesub(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in aids:
        await callback_query.message.answer('<b>🆔 Введите ID пользователя которому хотите забрать доступ:</b>', reply_markup=cancel_keyboard())
        await TakeSub.id.set()

@dp.message_handler(state=GiveSub.id)
async def givesub2(message: types.Message, state: FSMContext):
    if message.from_user.id in aids:
        async with state.proxy() as data:
            data['id'] = int(message.text)
        
        await message.answer('<b>🕰 Введите количество дней доступа:</b>', reply_markup=cancel_keyboard())
        await GiveSub.next()

@dp.message_handler(state=GiveSub.days)
async def givesub3(message: types.Message, state: FSMContext):
    if message.from_user.id in aids:
        async with state.proxy() as data:
            data['days'] = int(message.text)
            id = data['id']
            days = data['days']
        
        Users.give_sub(id, days)
        await bot.send_message(id, f'<b>💗 Вам выдан доступ на</b> <code>{days}</code> <b>дней!</b>', reply_markup=start_keyboard(message.from_user.id))
        await state.finish()
        await message.answer('<b>✅ Пользователю выдан доступ!</b>', reply_markup=admin_keyboard())

@dp.message_handler(state=TakeSub.id)
async def takesub2(message: types.Message, state: FSMContext):
    if message.from_user.id in aids:
        async with state.proxy() as data:
            data['id'] = int(message.text)
            id = data['id']
        
        Users.take_sub(id)
        await bot.send_message(id, f'<b>💔 У вас забрали доступ!</b>', reply_markup=start_keyboard(message.from_user.id))
        await state.finish()
        await message.answer('<b>✅ Пользователю забрали доступ!</b>', reply_markup=admin_keyboard())

@dp.message_handler(text='❌ Отмена', state='*')
@dp.throttled(anti_flood, rate=1)
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEJjSlkoEihmAAB4-w84tUzDBjiLWxsvewAAmQ6AALgo4IH_LAjcdV4gS0vBA')
    await message.answer(f'''<b>🟪Welcome to the club
<i>Используй кнопки, чтобы управлять ботом:</i></b>''', reply_markup=start_keyboard(message.from_user.id))

async def restart_bombers():
    for bomb in Bombs.get_bombs():
        number = bomb.NUM
        bomb_id = bomb.BID

        if number.startswith('380'):
            await asyncio.create_task(obj.runUA(bot, bomb_id, Bombs))
        elif number.startswith('7'):
            await asyncio.create_task(obj.runRU(bot, bomb_id, Bombs))

async def on_startup(dp):
    # await asyncio.create_task(restart_bombers())
    for curse in await crypto.get_exchange_rates():
        if curse.source == 'USDT' and curse.target == 'RUB':
            global curse_usdt
            curse_usdt = curse.rate

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)