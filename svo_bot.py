from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,  # Используем filters вместо Filters
    ConversationHandler,
    ContextTypes,
)

# Определяем состояния для ConversationHandler
FIO, PHONE = range(2)

# Ваш chat_id (замените на ваш реальный chat_id)
MY_CHAT_ID = 495383721  # Укажите ваш chat_id здесь

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Привет! Давай зарегистрируем тебя. Введи свое ФИО:")
    return FIO

# Обработчик для получения ФИО
async def get_fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['fio'] = update.message.text
    await update.message.reply_text(f"Спасибо, {context.user_data['fio']}! Теперь введи свой номер телефона:")
    return PHONE

# Обработчик для получения номера телефона
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone'] = update.message.text

    # Отправляем пользователю подтверждение
    await update.message.reply_text(
        f"Ты успешно зарегистрирован!\nФИО: {context.user_data['fio']}\nТелефон: {context.user_data['phone']}"
    )

    # Отправляем информацию вам
    await context.bot.send_message(
        chat_id=MY_CHAT_ID,
        text=f"Новый пользователь зарегистрирован:\nФИО: {context.user_data['fio']}\nТелефон: {context.user_data['phone']}"
    )

    return ConversationHandler.END

# Обработчик команды /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END

def main() -> None:
    # Вставьте сюда ваш токен
    application = Application.builder().token("6331123145:AAGRs5H8RS0TJaXiZ7Y44wuvsn9kKzOV1AE").build()

    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()