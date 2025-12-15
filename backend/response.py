from typing import Any, Optional
from dataclasses import dataclass

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
       return cls(code=200,data=data,message=message).to_dict()
    
    @classmethod
    def error(cls, message:str=None):
        return cls(code=500,message=message).to_dict()
    
    @classmethod
    def success_ws(cls, data:Optional[Any] = None, message:str=None):
        return cls(code=200,data=data,message=message).to_dict()
    
    @classmethod
    def error_ws(cls, data:Optional[Any] = None, message:str=None):
        return cls(code=500,data=data,message=message).to_dict()