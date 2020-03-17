from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    l = userText.split(" ")
    if l[0] == 'Search':
        search = l[2]
        params = {"q": search}
        r = requests.get("https://www.bing.com/search", params=params)
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find("ol", {"id": "b_results"})
        links = results.findAll("li", {"class": "b_algo"})
        a=[]
        for item in links:
            item_text = item.find("a").text
            # a.append(item.find("a").text)
            item_href = item.find("a").attrs["href"]
            # if item_text and item_href:
            a.append(item_text)
            #a.append(item_href)
        return str(a)
    else:
        return str(english_bot.get_response(userText))

if __name__ == "__main__":
    app.run()
