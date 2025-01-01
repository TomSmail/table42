from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Serve the HTML file
    return render_template("index.html")

@app.route("/reservations")
def get_reservations():
    return render_template("reservations.html")

if __name__ == "__main__":
    app.run(debug=True)