from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse
from training_pipeline import TrainingPipeline
from prediction import Prediction
import utils as util
import os
import shutil
import uvicorn
import sqlite3

app = FastAPI()
origins = ["*"]
processed_path = 'Processed_Files/'
prediction_path = 'Prediction_Results/'
validation_path = 'Validation_Files/'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Datasets(BaseModel):
    file_name: str
    created_on: str
    last_modified: str
    file_name: str

class DownloadFile(BaseModel):
    file_name: str
    source: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_dataset_list")
async def get_dataset_list():
    result = []
    for file in os.listdir(processed_path):
        created_datetime, modified_datetime = util.get_created_datetime(processed_path + file)
        record = {
            'file_name': file, 
            'created_on': created_datetime,
            'last_modified':modified_datetime
        }
        result.append(record)
    return result

@app.post("/upload_data")
async def upload_data(data_file: UploadFile = File(...)):
    util.delete_file(validation_path + data_file.filename)
    with open(validation_path + data_file.filename, "wb+") as file_object:
        shutil.copyfileobj(data_file.file, file_object)
    predict_pipe = Prediction()
    predict_pipe.prediction(validation_path + data_file.filename)
    return {'status':'OK'}

@app.post("/update_default_dataset")
async def update_default_dataset(dataItem : Datasets):
    util.update_sql("UPDATE tbl_default_dataset set FileName = '" + dataItem.file_name + "' where ID = 1")
    return {'status':'OK'}

@app.get("/get_pipeline_status")
async def get_pipeline_status():
    cursor = util.execute_sql("SELECT COUNT(*) ActiveCount FROM tbl_train_pipeline WHERE IsRunning = 1;")
    return util.cursor_to_json(cursor)[0]

    
@app.get("/get_pipeline_details")
async def get_pipeline_details():
    cursor = util.execute_sql("SELECT * FROM tbl_train_pipeline;")
    return util.cursor_to_json(cursor)

@app.get("/get_default_dataset")
async def get_default_dataset():
    cursor = util.execute_sql("SELECT * FROM tbl_default_dataset;")
    return util.cursor_to_json(cursor)[0]


@app.get("/train_pipeline")
async def train_pipeline(background_tasks: BackgroundTasks):
    background_tasks.add_task(training)
    return {'status':'OK'}

def training():
    util.update_sql("UPDATE tbl_train_pipeline set IsRunning = 1 where ID = 1;")
    cursor = util.execute_sql("SELECT * FROM tbl_default_dataset;")
    import_datafile = util.cursor_to_json(cursor)[0]
    path = processed_path + import_datafile['FileName']
    util.clear_all_models()
    util.clear_logs_files()
    train_pipe = TrainingPipeline()
    train_pipe.train_model(path)
    util.update_sql("UPDATE tbl_train_pipeline set IsRunning = 0 where ID = 1;")

# @app.get("/train_pipeline")
# async def train_pipeline():
#     util.update_sql("UPDATE tbl_train_pipeline set IsRunning = 1 where ID = 1;")
#     cursor = util.execute_sql("SELECT * FROM tbl_default_dataset;")
#     import_datafile = util.cursor_to_json(cursor)[0]
#     path = processed_path + import_datafile['FileName']
#     util.clear_all_models()
#     util.clear_logs_files()
#     train_pipe = TrainingPipeline()
#     train_pipe.train_model(path)
#     util.update_sql("UPDATE tbl_train_pipeline set IsRunning = 0 where ID = 1;")

@app.get("/get_prediction_files_list")
async def get_prediction_files_list():
    result = []
    for file in os.listdir(prediction_path):
        created_datetime, modified_datetime = util.get_created_datetime(prediction_path + file)
        record = {
            'file_name': file, 
            'created_on': created_datetime
        }
        result.append(record)
    return result

@app.get("/get_preprocessing_logs")
async def get_preprocessing_logs():
    file = open("Log_Files/data_preprocessing.txt","r+")
    data = file.readlines()
    file.close()
    return data

@app.get("/get_prediction_logs")
async def get_prediction_logs():
    with open("Log_Files/prediction_validation.txt","r+") as file:
        return file.readlines()

@app.get("/get_training_logs")
async def get_training_logs():
    with open("Log_Files/training_pipeline.txt","r+") as file:
        return file.readlines()
    
@app.post("/download_file")
async def download_file(file_info : DownloadFile): 
    switcher = {
        0: './Prediction_Results/',
        1: './Processed_Files/',
    }
    file_path =switcher.get(int(file_info.source)) + file_info.file_name
    return FileResponse(file_path, media_type='application/octet-stream')
    # file_path = switcher.get(int(file_info.source)) + file_info.file_name
    # def iterfile():  
    #     with open(file_path, mode="rb") as file_like:  
    #         yield from file_like
    # return StreamingResponse(iterfile())
    # return FileResponse(path=switcher.get(int(file_info.source)) + file_info.file_name, media_type='application/text', filename=file_info.file_name)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)