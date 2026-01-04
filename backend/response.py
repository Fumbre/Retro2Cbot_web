from typing import Any, Optional
from dataclasses import dataclass

@dataclass # this decoration can generate construct function automatically.
class Result:
    # properties
    code:int # response code
    message:str #response message
    data:Optional[Any] = None #response data.

    def to_dict(self) -> dict:
        """
        Result instance convert to dict.
        
        :param self: Result instance
        :return: Result dict
        :rtype: dict
        """
        return {
            "code":self.code,
            "data":self.data,
            "message":self.message
        }
    
    @classmethod # this decoration mentions this method is Result class method (ps: not instance).
                 # for example, if we want to use some functions in this class, we need to create the instance. (Result result(...))
                 # Afterthat, we can use this method (result.success(...)). But In this method, we don't need create instance by hands,
                 # it just use Classname.method() (Result.success(...)).
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