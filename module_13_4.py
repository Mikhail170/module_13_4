from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


api = "7721417736:AAFGUAn2ezjLIh-LBa2g46GdiOftdPCkTHE"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def fsm_age_handler(message, state: FSMContext):
    await state.update_data(age_param=message.text)
    await message.answer('Введите свой рост')
    await UserState.next()


@dp.message_handler(state=UserState.growth)
async def fsm_growth_handler(message, state: FSMContext):
    await state.update_data(growth_param=message.text)
    await message.answer('Введите свой вес')
    await UserState.next()


@dp.message_handler(state=UserState.weight)
async def fsm_weight_handler(message, state: FSMContext):
    await state.update_data(weight_param=message.text)
    data = await state.get_data()
    age = int(data['age_param'])
    growth = int(data['growth_param'])
    weight = int(data['weight_param'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша дневная норма калорий: {calories} ккал')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
