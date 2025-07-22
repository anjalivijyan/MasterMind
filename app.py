from flask import Flask, render_template, request
from mastermind import run_simulations

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_colors = int(request.form["num_colors"])
        code_length = int(request.form["code_length"])
        allow_repeats = request.form.get("allow_repeats") == "yes"
        mode = request.form["mode"]
        num_simulations = int(request.form["num_simulations"])

        stats = run_simulations(
            num_colors=num_colors,
            code_length=code_length,
            allow_repeats=allow_repeats,
            mode=mode,
            num_simulations=num_simulations
        )

        return render_template("results.html", stats=stats)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)