# for hitting the api

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from yc import Login
from typing import List, Dict, Tuple

load_dotenv()

app = FastAPI()


class Founders_data(BaseModel):
    hrefs:Dict[str, List[str]]
    founders:Dict[str, List[Tuple[str,str]]]
    jobs:List[str]
    specifications:List[str]
    tech_stack:List[str]
    



@app.get("/founders_data", response_model=List[Founders_data])
def founders_data(number:int):
    username =  os.getenv("YC_Username")
    password = os.getenv("YC_password")
    
    try:
        results = Login(username, password, number)
        return results
    except Exception as e:
        return {"error":str(e)}    
    
        
