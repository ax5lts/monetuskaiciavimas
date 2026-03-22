from flask import Flask, render_template, request, jsonify
import re
import requests

app = Flask(__name__)

API_KEY = "8cpBNj2xGjLsIYv7sq7N"
MODEL_ID = "euro-finder/1"

def aptikti_monetas(image_data: str) -> dict:
    """Priima base64 nuotrauką, grąžina aptiktų monetų duomenis."""
    image_data = re.sub(r'^data:image/\w+;base64,', '', image_data)
    
    response = request.post(
        f"https://detect.roboflow.com/{MODEL_ID}",
        params={"api_key": API_KEY},
        data=image_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    result = response.json()
    coins = []
    total = 0.0
    
    for p in result.get("predictions", []):
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