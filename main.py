from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from utils import process_lab_report
import uvicorn

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = process_lab_report(contents)
        return JSONResponse(content={"is_success": True, "data": result})
    except Exception as e:
        return JSONResponse(content={"is_success": False, "error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
