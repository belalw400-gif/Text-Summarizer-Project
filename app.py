from  fastapi import FastAPI, Body
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from textSummarizer.pipeline.prediction import PredictionPipeline


text:str = "What is Text Summarization?"

app = FastAPI()


@app.get("/", tags=['authentication'])
async def index():
    return RedirectResponse(url="/docs")



@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response(content="Training completed successfully!", media_type="text/plain")
    except Exception as e:
        return Response(content=f"Error occurred during training: {str(e)}", media_type="text/plain")







@app.post("/predict")
async def predict_route(text: str = Body(...)):
    try:
        obj= PredictionPipeline()
        text= obj.predict(text)
        return {"summary": text}
    except Exception as e:
        return {"error": str(e)}
    



if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)