from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import bd
from keyboards import *
from bd import *
from aiogram.dispatcher import FSMContext
import logging
import texts
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class TaskState(StatesGroup):
    task = State()
    task_ = State()
    id = State()
    # status = State()


@dp.message_handler(commands=["start", "старт"])
async def start(message: types.Message):
    await message.answer(f"Привет, {message['chat']['first_name']}")
    await message.answer(text=texts.WELCOME_TEXT, reply_markup=start_kb)


@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.answer(text='ИНФОРМАЦИЯ:')
    await message.answer(text=texts.ABOUT)
    await message.delete()


@dp.message_handler(text='Список задач')
async def list_task(message):
    await message.answer('Список текущих задач:')
    id_ = message['chat']['id']
    results = bd.get_all_tasks(id_)
    if len(results) == 0:
        await message.answer(text='Список с задачами отсутствует')
    else:
        for result in results:
            number = result[0]
            task = result[4]
            if result[5] == 0:
                stat_ = '*'
            elif result[5] == 1:
                stat_ = ''
            msg = f'{number}| {task} | {stat_} '
            await message.answer(text=msg, reply_markup=work_kb)


@dp.message_handler(text='Добавить задачу')
async def add_tasks(message):
    await message.answer('Новая задача:')
    await TaskState.task.set()


@dp.message_handler(state=TaskState.task)
async def set_task(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    user_id = message['chat']['id']
    username = message['chat']['username']
    first_name = message['chat']['first_name']
    task = message.text
    bd.add_task(user_id, username, first_name, task)
    await message.answer(text='Задача добавлена')
    await state.finish()


@dp.callback_query_handler(text='edit')
async def edit(call):
    idx = str(call.message['text']).find('|')
    id_ = int(str(call.message['text'])[:idx])
    TaskState.id = id_
    task_old = call.message.text
    await call.message.answer(f"Отредактируйте задачу {id_}:")
    await call.message.answer(text=task_old)
    await TaskState.task_.set()
    await call.answer()


@dp.message_handler(state=TaskState.task_)
async def set_task_(message: types.Message, state: FSMContext):
    await state.update_data(task_=message.text)
    task_new = message.text
    id_ = TaskState.id
    bd.edit_task(id_, task_new)
    await message.answer(text='Задача отредактирована')
    await state.finish()


@dp.callback_query_handler(text='delete')
async def delete_task(call):
    idx = str(call.message['text']).find('|')
    id_ = int(str(call.message['text'])[:idx])
    bd.delete_task(id_)
    await call.message.answer(f'Задача {id_} удалена!!!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
