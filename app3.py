import os
import concurrent.futures
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, conlist
from typing import List, Dict, Union

# Import all existing Gemini functions
from menu.drug.classifier import message_gemini as drug_classifier
from menu.drug.describer import message_gemini as drug_describer
from menu.food.classifier import message_gemini as food_classifier
from menu.food.describer import message_gemini as food_describer
from menu.duplication.classifier import message_gemini as duplication_classifier
from menu.duplication.describer import message_gemini as duplication_describer

app = FastAPI(title="Parallel Processing API")

# Pydantic models for input validation
class InputList(BaseModel):
    items: conlist(str, min_items=1)  # Ensures at least one item in the list

def safe_process_input(items: List[str], input_type: str = 'drug'):
    """
    Validate input data with type-specific handling
    """
    cleaned_items = [item.strip() for item in items if item.strip()]
    if not cleaned_items:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid or empty {input_type} list"
        )
    return cleaned_items

def run_endpoint_function(func, items: List[str], endpoint_name: str):
    """
    Safely execute endpoint functions with error handling
    """
    try:
        result = func(items)
        return {endpoint_name: result}
    except Exception as e:
        return {f"{endpoint_name}_error": str(e)}

@app.post("/parallel_aggregate")
async def parallel_aggregate_endpoints(
    request: Request, 
    input_type: str = 'drug'
):
    """
    Parallel processing of all endpoint functions
    """
    try:
        # Get raw input data
        raw_text = await request.body()
        raw_text = raw_text.decode("utf-8").strip()
        
        # Split input into list
        items = [item.strip() for item in raw_text.split(",") if item.strip()]
        
        # Validate input
        cleaned_items = safe_process_input(items, input_type)

        # Define endpoint tasks with their corresponding functions and names
        endpoint_tasks = [
            (drug_classifier, cleaned_items, "drug-drug classification"),
            (drug_describer, cleaned_items, "drug-drug describer"),
            (food_classifier, cleaned_items, "drug-food classification"),
            (food_describer, cleaned_items, "drug-food describer"),
            (duplication_classifier, cleaned_items, "drug-duplication classification"),
            (duplication_describer, cleaned_items, "therapeutic-duplication describer")
        ]
        
        # Parallel processing using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit all tasks to the thread pool
            futures = [
                executor.submit(run_endpoint_function, func, cleaned_items, name)
                for func, cleaned_items, name in endpoint_tasks
            ]
            
            # Wait for all futures to complete
            concurrent.futures.wait(futures)
            
            # Collect and aggregate results
            results = {}
            for future in futures:
                results.update(future.result())
        
        return results
    
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Server Error: {str(e)}"
        )

# Individual endpoint routes
@app.post("/drug_drug_classify")
def classify_drugs(request: Request):
    try:
        # Get raw input data
        raw_text = request.body().decode("utf-8").strip()
        
        # Split and clean items
        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        
        # Validate input
        cleaned_drugs = safe_process_input(drugs, 'drug')

        # Process
        result = drug_classifier(cleaned_drugs)
        return {"drug-drug classification": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/drug_drug_describer")
def describe_drugs(request: Request):
    try:
        # Get raw input data
        raw_text = request.body().decode("utf-8").strip()
        
        # Split and clean items
        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        
        # Validate input
        cleaned_drugs = safe_process_input(drugs, 'drug')

        # Process
        result = drug_describer(cleaned_drugs)
        return {"drug-drug describer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/drug_food_classify")
def classify_food(request: Request):
    try:
        # Get raw input data
        raw_text = request.body().decode("utf-8").strip()
        
        # Split and clean items
        foods = [food.strip() for food in raw_text.split(",") if food.strip()]
        
        # Validate input
        cleaned_foods = safe_process_input(foods, 'food')

        # Process
        result = food_classifier(cleaned_foods)
        return {"drug-food classification": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/drug_food_describer")
def describe_food(request: Request):
    try:
        # Get raw input data
        raw_text = request.body().decode("utf-8").strip()
        
        # Split and clean items
        foods = [food.strip() for food in raw_text.split(",") if food.strip()]
        
        # Validate input
        cleaned_foods = safe_process_input(foods, 'food')

        # Process
        result = food_describer(cleaned_foods)
        return {"drug-food describer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/drug_duplication_classify")
def classify_duplication(request: Request):
    try:
        # Get raw input data
        raw_text = request.body().decode("utf-8").strip()
        
        # Split and clean items
        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        
        # Validate input
        cleaned_drugs = safe_process_input(drugs, 'drug')

        # Process
        result = duplication_classifier(cleaned_drugs)
        return {"drug-duplication classification": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/drug_duplication_describer")
def describe_duplication(request: Request):
    try:
        # Get raw input data
        raw_text = request.body().decode("utf-8").strip()
        
        # Split and clean items
        drugs = [drug.strip() for drug in raw_text.split(",") if drug.strip()]
        
        # Validate input
        cleaned_drugs = safe_process_input(drugs, 'drug')

        # Process
        result = duplication_describer(cleaned_drugs)
        return {"therapeutic-duplication describer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.get("/health")
def health_check():
    return {"status": "API is running"}

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)