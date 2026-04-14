from flask import Flask, render_template, request
import pickle
import pandas as pd

# Initialize app
app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input
        data = list(request.form.values())

        # Check if all fields are filled
        if len(data) != 11 or "" in data:
            return render_template('index.html',
                                   prediction_text="⚠️ Please enter all 11 values")

        # Convert input into DataFrame with column names
        df = pd.DataFrame([data], columns=[
            "Timestamp", "CAN_ID", "DLC",
            "Data0", "Data1", "Data2", "Data3",
            "Data4", "Data5", "Data6", "Data7"
        ])

        # Convert data (same as training)
        df = df.astype(str)
        df = df.apply(lambda col: pd.factorize(col)[0])

        # Predict
        prediction = model.predict(df)

        # Result formatting
        if prediction[0] == 1:
            result = "🚨 Attack Detected!"
        else:
            result = "✅ Normal Activity"

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        # Handle unexpected errors
        return render_template('index.html',
                               prediction_text="⚠️ Error: Check input format")


# Run app
if __name__ == "__main__":
    app.run(debug=True)