import os
from flask import Flask, request, jsonify
from menu.drug.classifier import message_gemini as drug_classifier
from menu.drug.describer import message_gemini as drug_describer
from menu.food.classifier import message_gemini as food_classifier
from menu.food.describer import message_gemini as food_describer
from menu.duplication.classifier import message_gemini as duplication_classifier
from menu.duplication.describer import message_gemini as duplication_describer

app = Flask(__name__)

# Flask API route for classification using raw CSV text
@app.route("/drug_drug_classify", methods=["POST"])
def classify_drugs():
    try:
        raw_text = request.data.decode("utf-8").strip()
        if not raw_text:
            return jsonify({"error": "No drug list provided"}), 400

        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        if not drugs:
            return jsonify({"error": "Invalid or empty drug list"}), 400

        result = drug_classifier(drugs)
        return jsonify({"drug-drug classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500
    
@app.route("/drug_drug_describer", methods=["POST"])
def describe_drugs():
    try:
        raw_text = request.data.decode("utf-8").strip()
        if not raw_text:
            return jsonify({"error": "No drug list provided"}), 400

        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        if not drugs:
            return jsonify({"error": "Invalid or empty drug list"}), 400

        result = drug_describer(drugs)
        return jsonify({"drug-drug describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_food_classify", methods=["POST"])
def classify_food():
    try:
        raw_text = request.data.decode("utf-8").strip()
        if not raw_text:
            return jsonify({"error": "No food list provided"}), 400

        foods = [food.strip() for food in raw_text.split(",") if food.strip()]
        if not foods:
            return jsonify({"error": "Invalid or empty food list"}), 400

        result = food_classifier(foods)
        return jsonify({"drug-food classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_food_describer", methods=["POST"])
def describe_food():
    try:
        raw_text = request.data.decode("utf-8").strip()
        if not raw_text:
            return jsonify({"error": "No food list provided"}), 400

        foods = [food.strip() for food in raw_text.split(",") if food.strip()]
        if not foods:
            return jsonify({"error": "Invalid or empty food list"}), 400

        result = food_describer(foods)
        return jsonify({"drug-food describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_duplication_classify", methods=["POST"])
def classify_duplication():
    try:
        raw_text = request.data.decode("utf-8").strip()
        if not raw_text:
            return jsonify({"error": "No drug list provided"}), 400

        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        if not drugs:
            return jsonify({"error": "Invalid or empty drug list"}), 400

        result = duplication_classifier(drugs)
        return jsonify({"drug-duplication classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500
    
@app.route("/drug_duplication_describer", methods=["POST"])
def describe_duplication():
    try:
        raw_text = request.data.decode("utf-8").strip()
        if not raw_text:
            return jsonify({"error": "No drug list provided"}), 400

        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        if not drugs:
            return jsonify({"error": "Invalid or empty drug list"}), 400

        result = duplication_describer(drugs)
        return jsonify({"therapeutic-duplication describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
