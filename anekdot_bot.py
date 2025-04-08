import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Функция для получения случайной шутки с rzhunemogu.ru
def get_random_joke():
    url = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"
    try:
        response = requests.get(url)
        response.encoding = 'windows-1251'  # Устанавливаем правильную кодировку
        if response.status_code == 200:
            # Убираем лишние символы из ответа
            joke_text = response.text.replace('{"content":"', '').replace('"}', '')
            return joke_text
        else:
            return "Не удалось получить шутку. Ошибка при запросе к API."
    except Exception as e:
        return f"Не удалось получить шутку. Ошибка: {e}"

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот, который рассказывает анекдоты. Напиши /joke, чтобы получить случайный анекдот.')

# Команда /joke
async def joke(update: Update, context: CallbackContext) -> None:
    joke_text = get_random_joke()
    await update.message.reply_text(joke_text)

def main() -> None:
    # Вставьте сюда ваш токен
    token = '6331123145:AAGRs5H8RS0TJaXiZ7Y44wuvsn9kKzOV1AE'
    
    # Создаем приложение с помощью ApplicationBuilder
    application = ApplicationBuilder().token(token).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("joke", joke))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()