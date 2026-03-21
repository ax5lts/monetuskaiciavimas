from flask import Flask, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient
import base64
import re

app = Flask(__name__)

CLIENT = InferenceHTTPClient(
api_url-"https://serverless.roboflow.com",  api_key="8cpBNj2xGjLsIYv7sq7N"
)

def aptikti_monetas(image_data: str) -> dict:
    """Priima base64 nuotrauką, grąžina aptiktų monetų duomenis."""
    image_data = re.sub(r'^data:image/\w+;base64,', '', image_data)
    
    result = CLIENT.infer(image_data, model_id="euro-finder/1")
    
    coins = []
    total = 0.0
    
    for p in result["predictions"]:
        label = p["class"]
        value = float(label)
        coins.append({
            "x": int(p["x"]), "y": int(p["y"]),
            "label": label, "value": value
        })
        total += value
    
    return {"coins": coins, "total": round(total, 2)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aptikti", methods=["POST"])
def aptikti():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "Nėra nuotraukos"}), 400
    result = aptikti_monetas(data["image"])
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)