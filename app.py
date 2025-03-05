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

def parse_response(response: str) -> dict:
    """Parse the string response into a JSON dictionary."""
    response = response.replace('‘', '"').replace('’', '"')
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"error": "Failed to parse response"}

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
                results[name] = parse_response(result)
            except Exception as e:
                results[name] = {"error": f"Error: {str(e)}"}
    
    return JSONResponse(content=results)

@app.post("/drug_details")
async def drug_details(selected_meds: str = Form(...)):
    try:
        # Validate and clean input
        user_prompt = selected_meds.strip()
        
        if not user_prompt:
            return JSONResponse(
                content={"error": "No medication specified"},
                status_code=400
            )
        
        # Get response from AI
        response = drug_detail_check(user_prompt)
        
        # If the AI returns "error"
        if response == "error":
            return JSONResponse(
                content={"error": "AI service encountered an error"},
                status_code=500
            )
        
        # Parse the response
        try:
            # Directly return the parsed response as a dictionary
            parsed_response = json.loads(response)
            return JSONResponse(content=parsed_response)
        
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "error": "Failed to parse AI response",
                    "raw_response": response
                },
                status_code=500
            )
    
    except Exception as e:
        return JSONResponse(
            content={
                "error": f"Unexpected error: {str(e)}"
            },
            status_code=500
        )
    
    except Exception as e:
        return JSONResponse(
            content={
                "drug_detail": {
                    "error": f"Unexpected error: {str(e)}"
                }
            },
            status_code=500
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={"status": "API is running"})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", 8000)))