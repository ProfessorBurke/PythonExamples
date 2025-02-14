from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    
    if request.method == "POST":
        answer = request.form.get("answer")
        if answer == "B":
            response = "Well done!"
        else:
            response = "That's not correct; try again!"
    else:
        response = None
        answer = "A"
    return render_template("quiz.html", response=response,selected = answer)

@app.route("/q2")
def question2():
    return "<p>Another question would go here</p>"


if __name__ == "__main__":
    app.run(debug=True)
