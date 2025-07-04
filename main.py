from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import anadir, proximos, pasados, help_command, start, conv_handler
from config import TOKEN

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anadir", anadir))
    app.add_handler(CommandHandler("proximos", proximos))
    app.add_handler(CommandHandler("pasados", pasados))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
