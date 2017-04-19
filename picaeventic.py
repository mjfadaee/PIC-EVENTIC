from flask import Flask, render_template, request
from json import load
from apyori import apriori
import os

script_dir = os.path.dirname(__file__)
full_dataset_file_path = os.path.join(script_dir, './static/data/full-dataset.json')

listOfEvents =[]
usernames = []
transactions = []
bundles = []

app = Flask(__name__)


@app.route('/')
def main():
    global listOfEvents
    with open(full_dataset_file_path, 'r', encoding="utf8") as f:
        listOfEvents = load(f)

    return render_template("index.html", listOfEvents=listOfEvents, bundles=bundles)


@app.route('/', methods=['POST'])
def my_form_post():
    global listOfEvents
    global transactions
    global usernames

    username = request.form['username']
    eventID = request.form['eventID']

    usernames.append(username)
    transactions.append((username,eventID))

    # bundles = machine_learning()
    bundles = listOfEvents[0:2]

    return render_template("index.html", listOfEvents=listOfEvents,  bundles=bundles)

def machine_learning():
    global listOfEvents
    global transactions
    global usernames

    # make a list of all the user transactions
    listOfAllItems = []
    for username in set(usernames):
        itemsPerUser = []
        for transaction in transactions:
            if transaction[0] == username:
                itemsPerUser.append(transaction[1])
        listOfAllItems.append(itemsPerUser)

    # machine learning
    results = list(apriori(listOfAllItems, min_support=0.5, min_confidence=.6, min_lift=1.1, max_length=3))

    # find the best bundle
    bestBundle = []
    bestSupport = 0

    for relationRecord in results:
        bundle = relationRecord.items
        support = relationRecord.support
        if bestSupport < support:
            bestSupport = support
            bestBundle = bundle

    # translate the bestbumble to a list of events
    bestEventBundle = []
    for id in bestBundle:
        for event in listOfEvents:
            if event['id'] == id:
                bestEventBundle.append(event)

    return bestEventBundle


if __name__ == '__main__':
    app.run()
