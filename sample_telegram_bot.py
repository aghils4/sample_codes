import asyncio
from telegram import *
from telegram.ext import *
from flask import Flask,request,Response
token='your token'
app=Flask(__name__)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """
    sample function for handle start command in bot
    :param update:
    :param context:
    :return:
    """
    pass


# build app for telegram bot
application = ApplicationBuilder().pool_timeout(1000).connect_timeout(1000).token(token).build()
application.add_handler(CommandHandler('start',start))


# connect to telegram and get updates
async def robconnect(update):
    await application.initialize()
    await application.process_update(update)
    await application.shutdown()


@app.route('/',methods=['GET','POST'])
def main():
    if request.method=='POST':
        update=Update.de_json(request.get_json(force=True),application.bot)
        asyncio.run(robconnect(update))
        print(update)
        return Response('ok',status=200)
    else:
        return 'nok'

# run app by flask
if __name__ == '__main__':
    app.run(debug=True,port=2000)