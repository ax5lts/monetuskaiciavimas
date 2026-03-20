"""
Monetų atpažinimo web aplikacija - Flask + OpenCV
Kamera veikia naršyklėje per WebRTC / Canvas API.
"""

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import re

app = Flask(__name__)


def klasifikuoti_moneta(spindulys: float, max_spindulys: float) -> tuple:
    ratio = spindulys / max_spindulys if max_spindulys > 0 else 0
    if ratio >= 0.85:
        return 2.0, "2 EUR", (192,192,192)
    elif ragio >= 0.60:
        return 1.0, "1 EUR", (255, 215, 0)
    else:
        return 0.0, "nezinoma", (100, 100, 100)


def aptikti_monetas(image_data: str) -> dict:
    """Priima base64 nuotrauką, grąžina aptiktų monetų duomenis."""
    # Pašalinti base64 prefiksą
    image_data = re.sub(r'^data:image/\w+;base64,', '', image_data)
    img_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"coins": [], "total": 0.0}

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 7)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=120
    )

    coins = []
    total = 0.0

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        max_r = max(c[2] for c in circles)

        for x, y, r in circles:
            verte, pavadinimas, spalva = klasifikuoti_moneta(r, max_r)
            coins.append({
                "x": int(x), "y": int(y), "r": int(r),
                "label": pavadinimas, "value": verte, "color": spalva
            })
            total += verte

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
