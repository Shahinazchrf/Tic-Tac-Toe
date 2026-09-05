# app.py
# Flask web server for Tic-Tac-Toe

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Render the game page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)