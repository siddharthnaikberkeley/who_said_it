from flask import Flask, render_template, request
from flask import jsonify

import parse_messages
import os
import json

app = Flask(__name__)


@app.route('/game')
def game():
    min_len = request.args.get('min')
    max_len = request.args.get('max')
    choices = parse_messages.get_choices()
    return render_template('game.html', choices=choices)

@app.route('/get_quote')
def get_random_choice():
    quote, quote_hash = parse_messages.get_messages_for_game()
    quote['hash'] = quote_hash
    return quote

@app.route('/check')
def check():
    hash_val = request.args.get('hash')
    is_right = parse_messages.check_for_sender(hash_val)
    if is_right:
        return {}
    else:
        return {'error'}

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')