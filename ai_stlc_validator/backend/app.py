from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from validator import validate_documents

app = FastAPI(title="AI STLC Validator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/validate")
async def validate(mapping_file: UploadFile, testcase_file: UploadFile):
    mapping_df = pd.read_excel(io.BytesIO(await mapping_file.read()))
    testcase_df = pd.read_excel(io.BytesIO(await testcase_file.read()))
    
    report_path = validate_documents(mapping_df, testcase_df)
    
    return {"message": "Validation complete", "report_path": report_path}
