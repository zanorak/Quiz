import os
import time
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session

app = Flask(__name__)

app.secret_key=os.urandom(16)

questions = [
    {
        "question": "Who is buried in Grant's tomb?",
        "answers": [
            "George Washington",
            "Slab of Granite",
            "Ulysses S. Grant",
        ],
        "correct": 3
    },
    {
        "question": "What is the only thing you can put in a barrel to make it lighter?",
        "answers": [
            "Air",
            "Apples",
            "A hole",
        ],
        "correct": 3
    },
    {
        "question": "What do you get when you divide 20 by half and add 10?",
        "answers": [
            "10",
            "20",
            "30",
        ],
        "correct": 2
    },
    {
        "question": "How do you fill a pipe with water that is open at both ends?",
        "answers": [
            "Pour water in really fast",
            "Put one end in a pool and suck it up like straw",
            "Give up and throw it into the pool",
        ],
        "correct": 3
    },
    {
        "question": "If you combined 3 leaf piles from your back yard with the 4 leaf piles in your front yard, how many piles would you have?",
        "answers": [
            "1",
            "3",
            "4",
            "7",
        ],
        "correct": 1
    },
    {
        "question": "What color is an airplane's black box?",
        "answers": [
            "Gray",
            "Black",
            "Orange",
        ],
        "correct": 3
    },
    {
        "question": "What is the only English word that is always spelled incorrectly?",
        "answers": [
            "pneumonoultramicroscopicsilicovolcanoconiosis",
            "antidisestablishmentarianism",
            "incorrectly",
            "supercalifragilisticexpialidocious",
        ],
        "correct": 3
    },
]


@app.route('/', methods=['GET', 'POST'])
def renderMain():
    currQuest = session.get("currQuest")
    if request.method == 'POST':
        if session.get("answers") is None:
            session["answers"] = request.form.getlist('answer') # the first one will start the list 
        else:
            answers = session.get("answers")
            answers.append( request.form.get('answer') )
            session["answers"] = answers
        currQuest += 1
        session["currQuest"] = currQuest
        # redirect to the main page so a reload does not resubmit
        return redirect(url_for("renderMain"))


    elif request.method == 'GET':
        if session.get("currQuest") is None:
            session["currQuest"] = 0
            session["startTime"] = time.time()
            currQuest = 0

    if currQuest < len(questions):
        return render_template('question.html', question = questions[currQuest])

    else:
        elapsedTime = time.time() - session.get("startTime")
        return render_template('finished.html', elapsedTime = elapsedTime, questions = questions, numQuest = len(questions))

@app.route('/retake')
def retake():
    session.clear() #clears variable values and creates a new session
    return redirect(url_for("renderMain"))

