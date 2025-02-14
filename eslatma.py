from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

# Eslatma ma'lumotlarini saqlash
reminders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Salom! Men sizning shaxsiy eslatma botingizman. \n"
        "Eslatma qo'shish uchun /add komandasini ishlating.\n"
        "Misol: /add 14:30 Kitob o'qish"
    )

async def add_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.message.chat_id
        args = context.args

        if len(args) < 2:
            await update.message.reply_text(
                "Iltimos, vaqt va eslatma matnini kiriting. \nMisol: /add 14:30 Kitob o'qish"
            )
            return

        time_str = args[0]
        message = ' '.join(args[1:])
        reminder_time = datetime.strptime(time_str, "%H:%M").time()

        if user_id not in reminders:
            reminders[user_id] = []

        reminders[user_id].append((reminder_time, message))
        await update.message.reply_text(f"Eslatma qo'shildi: {time_str} - {message}")
    except ValueError:
        await update.message.reply_text("Noto'g'ri vaqt formatini kiriting. To'g'ri format: HH:MM")

async def check_reminders(application: Application) -> None:
    now = datetime.now()
    for user_id, user_reminders in list(reminders.items()):
        for reminder in user_reminders[:]:
            reminder_time, message = reminder
            if reminder_time.hour == now.hour and reminder_time.minute == now.minute:
                await application.bot.send_message(chat_id=user_id, text=f"Eslatma: {message}")
                user_reminders.remove(reminder)

def main() -> None:
    # Bot token
    TOKEN = "7632752675:AAHJxrve0e2bzZgrp0iHOKljN3xTduTxfzI"

    # Create Application
    application = Application.builder().token(TOKEN).build()

    # Har bir daqiqada eslatmalarni tekshirish
    application.job_queue.run_repeating(
        lambda _: application.create_task(check_reminders(application)),
        interval=60,
        first=0
    )

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_reminder))

    # Run the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
