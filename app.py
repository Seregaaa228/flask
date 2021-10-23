from flask import Flask, render_template

import json

app = Flask(__name__)

with open("data.json") as file:
    data = json.load(file)


@app.route("/")
def calendar():
    return render_template("main.jinja", schedule=data)


if __name__ == "__main__":
    app.run(debug=True)
