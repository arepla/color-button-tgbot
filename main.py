from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests


BOT_TOKEN = "BOT TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id


    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": "Hi, tap to button <tg-emoji emoji-id=\"5285430309720966085\">👍</tg-emoji>",
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "Danger button",
                        "callback_data": "btn_danger",
                        "style": "danger",
                        "icon_custom_emoji_id": "5310169226856644648"
                    },
                    {
                        "text": "Success button",
                        "callback_data": "btn_success",
                        "style": "success",
                        "icon_custom_emoji_id": "5310076249404621168"
                    }
                ],
                [
                    {
                        "text": "Primary button",
                        "callback_data": "btn_primary",
                        "style": "primary",
                        "icon_custom_emoji_id": "5285430309720966085"
                    },
                    {
                        "text": "Button",
                        "callback_data": "btn_secondary",
                        "icon_custom_emoji_id": "5285032475490273112"
                    }
                ]
            ]
        }
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("✅")
    else:
        print(f"❌ {response.text}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    button_messages = {
        "btn_danger": "⚠️ !",
        "btn_success": "✅ !",
        "btn_primary": "🔵 !",
        "btn_secondary": "⚪️ !"
    }

    chat_id = update.effective_chat.id
    message_id = query.message.message_id


    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": button_messages.get(query.data, "Неизвестная кнопка"),
        "parse_mode": "HTML"
    }

    requests.post(url, json=data)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    print("🤖 success start")
    application.run_polling()


if __name__ == '__main__':
    main()