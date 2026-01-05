from fastapi import APIRouter,Request
from service import insertRobots,selectRobots
from database import SessionLocal
from service import selectCurrentGripper,selectNeopixelList,selectPulsesList,selectReflectSensorList,selectSonarList

router = APIRouter()

@router.post("/robots")
async def insertRobot(request:Request):
    """
   insert robot information into database
    
    :param request: http request
    :type request: Request
    """
    params = await request.json() if hasattr(request, "json") else {}
    return insertRobots(request=request,robotName=params.get("robotName"),robotCode=params.get("robotCode"))


@router.get("/robots")
def robotList(request:Request):
    """
    get robots inforamtion
    
    :param request: http request
    :type request: Request
    """
    return selectRobots(request=request)

@router.get("/robots/{robotCode}/{event}")
def selectDataList(robotCode:str,event:str):
    db = SessionLocal()
    if event == "rs": # reflective sensor
        result = selectReflectSensorList(db=db, robotCode=robotCode)
        myResult = {
            **result,
            "event": event
            }
    elif event == "sonar": # sonar
        result = selectSonarList(db=db, robotCode=robotCode)
        myResult = {
         **result,
                "event": event
            }
    elif event == "pulses": # pulses
        result = selectPulsesList(db=db, robotCode=robotCode)
        myResult = {
            **result,
            "event": event
            }
    elif event == "neopixels": # leds
        result = selectNeopixelList(db=db, robotCode=robotCode)
        myResult = {
            **result,
            "event": event
            }
    elif event == "gripper": # gripper
        result = selectCurrentGripper(db=db, robotCode=robotCode)
        myResult = {
            **result,
             "event": event
            }
    return myResult;    