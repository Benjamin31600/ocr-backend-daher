import os
from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np

app = Flask(__name__)

# Initialisation d'EasyOCR pour le français et l'anglais
reader = easyocr.Reader(['fr', 'en'])

@app.route("/")
def home():
    return "Serveur OCR Daher en ligne !"

@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    # Lire le fichier image en mémoire et le convertir en image avec OpenCV
    file_bytes = file.read()
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Exécuter l'OCR via EasyOCR
    results = reader.readtext(img, detail=0)
    text = "\n".join(results)

    return jsonify({"text": text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
