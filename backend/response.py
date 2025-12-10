from typing import Any, Optional
from dataclasses import dataclass
from flask import jsonify

@dataclass
class Result:
    code:int
    message:str
    data:Optional[Any] = None

    def to_dict(self) -> dict:
        return {
            "code":self.code,
            "data":self.data,
            "message":self.message
        }
    
    @classmethod
    def success(cls, data:Optional[Any] = None, message:str=None):
       return jsonify(cls(code=200,data=data,message=message).to_dict()) 
    
    @classmethod
    def error(cls, message:str=None):
        return jsonify(cls(code=500,message=message).to_dict())
    