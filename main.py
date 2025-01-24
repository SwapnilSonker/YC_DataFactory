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
        data = Login(username, password, number)
        print("Login function executed")
        logging.info(f"Founders data processed for number {len(data)}")
        # Check for errors (if any)
        if not isinstance(data, list):
            raise HTTPException(status_code=500, detail="Invalid data received")

        # Return the extracted data as a list
        bands = [Founders_data(**res) for res in data]
        if not bands:
            return HTTPException(status_code=404, detail="Data not found")
        return [band.model_dump() for band in bands]

    except Exception as e:
        logging.error(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="localhost", log_level="info")