import os
import concurrent.futures
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from waitress import serve
# Import all existing Gemini functions
from menu.drug.classifier import stream_output as drug_classifier
from menu.drug.describer import stream_output as drug_describer
from menu.food.classifier import stream_output as food_classifier
from menu.food.describer import stream_output as food_describer
from menu.duplication.classifier import stream_output as duplication_classifier
from menu.duplication.describer import stream_output as duplication_describer

load_dotenv()
app = Flask(__name__)

def parse_input(data):
    """
    Parse input in the format "selected_meds=med1,med2,med3"
    """
    if not data or "selected_meds=" not in data:
        return None, "Invalid input format. Expected 'selected_meds=med1,med2,med3'"
    
    try:
        # Split on 'selected_meds=' and take the second part
        meds_str = data.split("selected_meds=")[1].strip()
        # Create a single string with medications separated by commas
        formatted_input = f"{meds_str}"
        
        return formatted_input, None
        
    except Exception as e:
        return None, f"Error parsing input: {str(e)}"

def run_endpoint_function(func, items, endpoint_name):
    """
    Safely execute endpoint functions with error handling
    """
    try:
        # Pass the formatted string directly to the function
        result = func(items)
        # Ensure result is JSON serializable
        if isinstance(result, set):
            result = list(result)
        return {endpoint_name: result}
    except Exception as e:
        return {f"{endpoint_name}_error": str(e)}

@app.route("/parallel_aggregate", methods=["POST"])
def parallel_aggregate_endpoints():
    """
    Parallel processing of all endpoint functions
    """
    try:
        # Get raw input data
        raw_text = request.data.decode("utf-8").strip()
        
        # Parse input
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        # Define endpoint tasks with their corresponding functions and names
        endpoint_tasks = [
            (drug_classifier, items, "drug-drug classification"),
            (drug_describer, items, "drug-drug describer"),
            (food_classifier, items, "drug-food classification"),
            (food_describer, items, "drug-food describer"),
            (duplication_classifier, items, "drug-duplication classification"),
            (duplication_describer, items, "therapeutic-duplication describer")
        ]
        
        # Parallel processing using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(run_endpoint_function, func, items, name)
                for func, items, name in endpoint_tasks
            ]
            
            concurrent.futures.wait(futures)
            
            results = {}
            for future in futures:
                results.update(future.result())
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"aggregate_error": f"Internal Server Error: {str(e)}"}), 500

@app.route("/drug_drug_classify", methods=["POST"])
def classify_drugs():
    try:
        raw_text = request.data.decode("utf-8").strip()
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        result = drug_classifier(items)
        return jsonify({"drug-drug classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_drug_describer", methods=["POST"])
def describe_drugs():
    try:
        raw_text = request.data.decode("utf-8").strip()
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        result = drug_describer(items)
        return jsonify({"drug-drug describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_food_classify", methods=["POST"])
def classify_food():
    try:
        raw_text = request.data.decode("utf-8").strip()
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        result = food_classifier(items)
        return jsonify({"drug-food classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_food_describer", methods=["POST"])
def describe_food():
    try:
        raw_text = request.data.decode("utf-8").strip()
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        result = food_describer(items)
        return jsonify({"drug-food describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_duplication_classify", methods=["POST"])
def classify_duplication():
    try:
        raw_text = request.data.decode("utf-8").strip()
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        result = duplication_classifier(items)
        return jsonify({"drug-duplication classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_duplication_describer", methods=["POST"])
def describe_duplication():
    try:
        raw_text = request.data.decode("utf-8").strip()
        items, error = parse_input(raw_text)
        if error:
            return jsonify({"error": error}), 400

        result = duplication_describer(items)
        return jsonify({"therapeutic-duplication describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT"))