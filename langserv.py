"""Web service that accepts a text and returns its language code."""

from flask import Flask
from flask import request, jsonify
import langdetect as ld
import pycountry
import os

app = Flask(__name__)

# flask --app langserv.py run --host 0.0.0.0

@app.route("/")
def hello_world():
    """Returns a description of the web service."""
    return "Hello!! This is an app to detect the language of a document"


@app.route("/detect", methods=['GET'])
def detect():
    """Identifies the language of the text."""
    query = request.args.get('text')
    language = ld.detect(query)
    return language

@app.route("/instance")
def instance():
    dirs = os.listdir('/var/lib/cloud/instances/')
    return dirs[0]

#i want to create the endpoint to obtain the complete name of the language using the code in a json format.
@app.route("/detect_name") 
def detect_name():
    text = request.args.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    code = ld.detect(text)
    try:
        language = pycountry.languages.get(alpha_2=code)
        name = language.name if language else "Unknown"
    except KeyError:
        name = "Unknown"
    return jsonify({"code": code, "language": name})

#endpoint to show stats about the text such as n. of characters and n. of words
@app.route("/texts_stats", methods=['GET'])
def texts_stats():
    text = request.args.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    char_count = len(text)
    word_count = len(text.split())

    return jsonify({
        "text": text,
        "character_count": char_count,
        "word_count": word_count
    })


if __name__ == "__main__":
    app.run(debug=True)