# Import flask functions
from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)


# We want to store the html somewhere else though, not just as a giant string. 
# Enter render_template
@app.route('/')
def root(): 
    return render_template('index.html') 

@app.route('/all')
def all(): 
    return {
        'leagues':["USQ","MLQ","IQA"],
        'seasons':["USQ8","USQ9","USQ10","USQ11","USQ12","USQ13","USQ15","USQ2023"],
        'tournaments':["USQ Cup 15"],
        'games':["TEXAS v UVA 140-125*"]
    }
 

# If name is main, run flask 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)