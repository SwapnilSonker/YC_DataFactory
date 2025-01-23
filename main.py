# for hitting the api

import logging
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schemas import Founders_data
from yc import Login


load_dotenv()

app = FastAPI()

#see bug bytes , very academy lec on fastapi
@app.get("/founders_data/{number}")
def founders_data(number:int) -> list[Founders_data]:
    username =  os.getenv("YC_Username")
    password = os.getenv("YC_password")
    print("here")
    try:
        # Get the extracted data
        print("in try")
        Login(username, password, number)
        logging.info(f"Founders data processed for number {len(Login(username, password, number))}")
        # Check for errors (if any)
        if not isinstance(Login(username, password, number), list):
            raise HTTPException(status_code=500, detail="Invalid data received")

        # Return the extracted data as a list
        bands = [Founders_data(**res) for res in Login(username, password, number)]
        if bands is None:
            return HTTPException(status_code=404, detail="Data not found")
        return [band.model_dump() for band in bands]

    except Exception as e:
        return {"error": str(e)}    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="localhost", log_level="info")