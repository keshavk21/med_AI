import os
import concurrent.futures
from flask import Flask, request, jsonify

# Import all existing Gemini functions
from menu.drug.classifier import message_gemini as drug_classifier
from menu.drug.describer import message_gemini as drug_describer
from menu.food.classifier import message_gemini as food_classifier
from menu.food.describer import message_gemini as food_describer
from menu.duplication.classifier import message_gemini as duplication_classifier
from menu.duplication.describer import message_gemini as duplication_describer

app = Flask(__name__)

def safe_process_input(raw_text, input_type):
    """
    Validate and process input data with type-specific error handling
    """
    if not raw_text:
        return None, f"No {input_type} list provided"

    items = [item.strip() for item in raw_text.split(",") if item.strip()]
    if not items:
        return None, f"Invalid or empty {input_type} list"

    return items, None

def run_endpoint_function(func, items, endpoint_name):
    """
    Safely execute endpoint functions with error handling
    """
    try:
        result = func(items)
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
        
        # Determine input type based on context or header if needed
        input_type = request.headers.get('X-Input-Type', 'drug')
        
        # Validate input
        items, error = safe_process_input(raw_text, input_type)
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
            # Submit all tasks to the thread pool
            futures = [
                executor.submit(run_endpoint_function, func, items, name)
                for func, items, name in endpoint_tasks
            ]
            
            # Wait for all futures to complete
            concurrent.futures.wait(futures)
            
            # Collect and aggregate results
            results = {}
            for future in futures:
                results.update(future.result())
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"aggregate_error": f"Internal Server Error: {str(e)}"}), 500

# Preserve all existing routes with parallel processing option
@app.route("/drug_drug_classify", methods=["POST"])
def classify_drugs():
    try:
        raw_text = request.data.decode("utf-8").strip()
        drugs, error = safe_process_input(raw_text, 'drug')
        if error:
            return jsonify({"error": error}), 400

        result = drug_classifier(drugs)
        return jsonify({"drug-drug classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_drug_describer", methods=["POST"])
def describe_drugs():
    try:
        raw_text = request.data.decode("utf-8").strip()
        drugs, error = safe_process_input(raw_text, 'drug')
        if error:
            return jsonify({"error": error}), 400

        result = drug_describer(drugs)
        return jsonify({"drug-drug describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_food_classify", methods=["POST"])
def classify_food():
    try:
        raw_text = request.data.decode("utf-8").strip()
        foods, error = safe_process_input(raw_text, 'food')
        if error:
            return jsonify({"error": error}), 400

        result = food_classifier(foods)
        return jsonify({"drug-food classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_food_describer", methods=["POST"])
def describe_food():
    try:
        raw_text = request.data.decode("utf-8").strip()
        foods, error = safe_process_input(raw_text, 'food')
        if error:
            return jsonify({"error": error}), 400

        result = food_describer(foods)
        return jsonify({"drug-food describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_duplication_classify", methods=["POST"])
def classify_duplication():
    try:
        raw_text = request.data.decode("utf-8").strip()
        drugs, error = safe_process_input(raw_text, 'drug')
        if error:
            return jsonify({"error": error}), 400

        result = duplication_classifier(drugs)
        return jsonify({"drug-duplication classification": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/drug_duplication_describer", methods=["POST"])
def describe_duplication():
    try:
        raw_text = request.data.decode("utf-8").strip()
        drugs, error = safe_process_input(raw_text, 'drug')
        if error:
            return jsonify({"error": error}), 400

        result = duplication_describer(drugs)
        return jsonify({"therapeutic-duplication describer": result})

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)