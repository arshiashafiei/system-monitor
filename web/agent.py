from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psutil
import os
import uvicorn

app = FastAPI()

class SystemStatus(BaseModel):
    cpu: float
    memory: float
    processes: int

@app.get("/status", response_model=SystemStatus)
def get_system_status():
    try:
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        processes = len(psutil.pids())

        return SystemStatus(cpu=cpu, memory=memory.percent, processes=processes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving system status: {str(e)}")

@app.post("/restart")
def restart_system():
    try:
        # Command to restart the system (Linux-based systems)
        os.system("sudo reboot")
        return {"message": "System is restarting..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restarting system: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


