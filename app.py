from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the model
model = joblib.load("ticket_pricing_model_v6.pkl")

@app.route("/")
def index():
    return render_template("index.html", price=None)

@app.route("/predict", methods=["POST"])
def predict():
    base_price = float(request.form['base_price'])
    seat_multiplier = float(request.form['seat_multiplier'])
    tickets_sold = int(request.form['tickets_sold'])
    days_until = int(request.form['days_until'])

    tickets_allocated = 50000
    remaining_tickets = tickets_allocated - tickets_sold
    demand_factor = tickets_sold / (tickets_sold + remaining_tickets)

    # Prepare input for model
    data = pd.DataFrame([{
        "Base Price (SAR)": base_price,
        "Tickets Allocated": tickets_allocated,
        "Tickets Sold": tickets_sold,
        "Remaining Tickets": remaining_tickets,
        "Demand Factor": demand_factor,
        "Days Until Match": days_until,
        "Seat Multiplier": seat_multiplier
    }])

    predicted_price = model.predict(data)[0]
    return render_template("index.html", price=round(predicted_price, 2))

if __name__ == "__main__":
    app.run(debug=True)


