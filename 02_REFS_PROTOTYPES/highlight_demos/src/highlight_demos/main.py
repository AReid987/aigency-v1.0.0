from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import asyncio
import pandas as pd

app = FastAPI()

# In-memory store for agent metrics
agent_metrics = []
performance_cache = {}

class AgentMetric(BaseModel):
    agent_id: str
    timestamp: datetime
    response_time_ms: float
    tokens_input: int
    tokens_output: int
    success_rate: float
    user_rating: float = None

class AgentPerformance(BaseModel):
    agent_id: str
    avg_response_time: float
    avg_tokens_per_query: float
    success_rate: float
    user_satisfaction: float
    query_count: int
    performance_trend: list[float]

@app.post("/metrics/")
async def record_metric(metric: AgentMetric):
    agent_metrics.append(metric)
    return {"message": "Metric recorded successfully"}

@app.get("/performance/{agent_id}", response_model=AgentPerformance)
async def get_agent_performance(agent_id: str):
    if agent_id in performance_cache:
        return performance_cache[agent_id]
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

@app.get("/leaderboard/")
async def get_leaderboard():
    leaderboard = sorted(performance_cache.values(), key=lambda x: x.success_rate, reverse=True)
    return leaderboard

async def process_metrics():
    while True:
        if agent_metrics:
            # Group by agent_id
            df = pd.DataFrame([m.dict() for m in agent_metrics])
            agent_groups = df.groupby('agent_id')
            
            # Calculate performance metrics
            for agent_id, group in agent_groups:
                recent_data = group[group['timestamp'] > datetime.now() - timedelta(hours=24)]
                
                if not recent_data.empty:
                    # Calculate metrics using vectorized operations
                    avg_response_time = recent_data['response_time_ms'].mean()
                    avg_tokens = (recent_data['tokens_input'] + recent_data['tokens_output']).mean()
                    success_rate = recent_data['success_rate'].mean() * 100
                    
                    # Calculate user satisfaction (if ratings exist)
                    ratings = recent_data['user_rating'].dropna()
                    user_satisfaction = ratings.mean() if not ratings.empty else 0
                    
                    # Calculate performance trend (last 6 hours in hourly intervals)
                    trend = []
                    for i in range(6):
                        start_time = datetime.now() - timedelta(hours=i+1)
                        end_time = datetime.now() - timedelta(hours=i)
                        period_data = recent_data[(recent_data['timestamp'] > start_time) & 
                                                 (recent_data['timestamp'] <= end_time)]
                        trend.append(period_data['success_rate'].mean() * 100 if not period_data.empty else 0)
                    
                    # Store in cache
                    performance_cache[agent_id] = AgentPerformance(
                        agent_id=agent_id,
                        avg_response_time=avg_response_time,
                        avg_tokens_per_query=avg_tokens,
                        success_rate=success_rate,
                        user_satisfaction=user_satisfaction,
                        query_count=len(recent_data),
                        performance_trend=list(reversed(trend))
                    )
        
        # Process every 30 seconds
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_metrics())
