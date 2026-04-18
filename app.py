from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        area = float(request.form["area"])
        bedrooms = int(request.form["bedrooms"])
        bath = int(request.form["bath"])
        quality = int(request.form["quality"])
        year = int(request.form["year"])

        input_data = pd.DataFrame([[area, bedrooms, bath, quality, year]],
                                  columns=["Area", "Bedrooms", "Full Bath", "Overall Qual", "Year Built"])

        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]

        return render_template(
            "index.html",
            prediction_text=f" Predicted Price: ₹ {int(prediction):,}"
        )

    except:
        return render_template(
            "index.html",
            prediction_text=" Please enter valid numbers!"
        )

if __name__ == "__main__":
    app.run(debug=True)