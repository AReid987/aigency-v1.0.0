import pandas as pd
from io import StringIO
from typing import Dict, Any
import plotly.express as px
import plotly.io as pio

async def analyze_csv_data(file_content: str) -> Dict[str, Any]:
    """
    Analyzes CSV data and returns basic statistics.
    """
    try:
        df = pd.read_csv(StringIO(file_content))
        
        # For POC, return basic info
        analysis_results = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "head": df.head().to_dict(orient='records'),
            "description": df.describe().to_dict()
        }
        return analysis_results
    except Exception as e:
        return {"error": str(e)}

async def generate_bar_chart(file_content: str, x_column: str, y_column: str) -> Dict[str, Any]:
    """
    Generates a bar chart from CSV data using Plotly.
    """
    try:
        df = pd.read_csv(StringIO(file_content))
        if x_column not in df.columns or y_column not in df.columns:
            return {"error": "Specified columns not found in data."}

        fig = px.bar(df, x=x_column, y=y_column)
        chart_html = pio.to_html(fig, full_html=False)
        return {"chart_html": chart_html}
    except Exception as e:
        return {"error": str(e)}
