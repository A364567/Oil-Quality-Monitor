from flask import Flask, request, jsonify
import joblib
import numpy as np
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load("model.joblib")
features = ["Temperature (C)", "Viscosity (cSt)", "Turbidity", "Oil_Humidity_percent"]

def viscosity_from_temp_vogel(temp_c):
    T = temp_c + 273.15
    A = 2e-5
    B = 1500
    C = -120
    return round(A * math.exp(B / (T + C)), 2)

latest_data = []

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        if "Viscosity (cSt)" not in data or data["Viscosity (cSt)"] is None:
            if "oil_temperature_C" in data and data["oil_temperature_C"] is not None:
                data["Viscosity (cSt)"] = viscosity_from_temp_vogel(data["oil_temperature_C"])
            else:
                data["Viscosity (cSt)"] = 45.0
        
        values = [float(data.get(f, 0.0)) for f in features]
        X = np.array(values).reshape(1, -1)
        
        prediction_value = float(model.predict(X)[0])
        
        if prediction_value < 30:
            label = "Excellent"
            status = "🟢"
        elif prediction_value < 60:
            label = "Good"
            status = "🟡"
        elif prediction_value < 80:
            label = "Fair"
            status = "🟠"
        else:
            label = "Poor"
            status = "🔴"
        
        result = {
            "predicted_value": round(prediction_value, 2),
            "label": label,
            "status": status,
            "data": data
        }
        
        latest_data.append(result)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/latest", methods=["GET"])
def get_latest():
    return jsonify(latest_data[-20:])

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "model_type": "regression"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)