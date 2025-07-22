from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form
from typing import Dict, Any

from .controllers import analyze_csv_data, generate_bar_chart
from apps.api.src.auth.controllers import get_current_user

data_analysis_router = APIRouter(
    prefix="/data-analysis",
    tags=["data-analysis"],
    dependencies=[Depends(get_current_user)],
)

@data_analysis_router.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analyzes an uploaded CSV file and returns basic statistics.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are allowed.")
    
    content = await file.read()
    analysis_results = await analyze_csv_data(content.decode('utf-8'))
    
    if "error" in analysis_results:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=analysis_results["error"])
        
    return analysis_results

@data_analysis_router.post("/generate-chart")
async def generate_chart(
    file: UploadFile = File(...),
    x_column: str = Form(...),
    y_column: str = Form(...)
) -> Dict[str, Any]:
    """
    Generates a bar chart from an uploaded CSV file.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are allowed.")
    
    content = await file.read()
    chart_results = await generate_bar_chart(content.decode('utf-8'), x_column, y_column)
    
    if "error" in chart_results:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=chart_results["error"])
        
    return chart_results
