import telegram
from flask import Flask, request
import os

# Replace YOUR_TOKEN with your bot's API token
bot = telegram.Bot(token="6193333968:AAHiRXlfMeSfGpmoKhhwezQ9dDPjXsEQiuY")

app = Flask(__name__)


@app.route("/http://127.0.0.1:5000", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print("received")
    # Process the message
    message = update.message.text
    # Do something with the message, such as respond with a message
    bot.send_message(
        chat_id=update.message.chat_id, text="Received message: " + message
    )
    return "ok"


if __name__ == "__main__":
    # Replace YOUR_URL with the public URL of your server
    bot.setWebhook(url="/https://06be-77-29-28-186.eu.ngrok.io")
    app.run()
