# Import flask functions
from flask import Flask, render_template,request
import pandas as pd
import json
app = Flask(__name__)


# We want to store the html somewhere else though, not just as a giant string. 
# Enter render_template
@app.route('/')
def root(): 
    return render_template('index.html') 

@app.route('/all')
def all(): 
    with open('data/leagues.json') as f: 
        leagues = json.loads(f.read())
    with open('data/seasons.json') as f: 
        seasons = json.loads(f.read())
    with open('data/tournaments.json') as f: 
        tournaments = json.loads(f.read())
    with open('data/games.json') as f: 
        games = json.loads(f.read())
    return {
        'leagues':leagues,
        'seasons':seasons,
        'tournaments':tournaments,
        'games':games
    }

@app.route('/statsheet')
def gen_statsheet():
    print('AAAH')
    print(request.args)
    return 'sup'

# If name is main, run flask 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)