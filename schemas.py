from pydantic import BaseModel


class HrefModel(BaseModel):
    link: str
    company_image: list[str]
    
class FoundersModel(BaseModel):
    founder_images: list[str]
    founder_names: list[list[str]]
    
class Founders_data(BaseModel):
    hrefs:HrefModel
    founders:FoundersModel
    jobs:list[list[str]]
    specifications:list[str]
    tech_stack:list[str]