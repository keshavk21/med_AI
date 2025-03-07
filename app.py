from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import concurrent.futures
import json
import os
import uvicorn
from dotenv import load_dotenv
from menu.drug_interaction.drug_drug import stream_output as drug_drug_check
from menu.drug_interaction.drug_food import stream_output as drug_food_check
from menu.drug_interaction.therapeutic_duplication import stream_output as therapeutic_check
from menu.drug_details.drug_detail import stream_output as drug_detail_check

# Load environment variables
load_dotenv()

app = FastAPI()

# Define the input model
class InputData(BaseModel):
    selected_meds: str

@app.post("/aggregate_interactions")
async def aggregate_interactions(selected_meds: str = Form(...)):
    """Endpoint to aggregate drug interactions, food interactions, and therapeutic duplications."""
    user_prompt = selected_meds.strip()
    
    # Prepare tasks for concurrent execution
    tasks = [
        (drug_drug_check, user_prompt, "drug_drug_check"),
        (drug_food_check, user_prompt, "drug_food_check"),
        (therapeutic_check, user_prompt, "therapeutic_check"),
    ]
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(func, user_prompt): name
            for func, user_prompt, name in tasks
        }
        
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                results[name] = result
            except Exception as e:
                results[name] = {"error": f"Error: {str(e)}"}
    
    return JSONResponse(content=results)

@app.post("/drug_details")
async def drug_details(selected_meds: str = Form(...)):
    """Endpoint to get drug details."""
    user_prompt = selected_meds.strip()
    response = drug_detail_check(user_prompt)
    # Return the raw response string without attempting to parse it as JSON
    return JSONResponse(content={"drug_details": response})

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={"status": "API is running"})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", 8000)))
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", 8000)))