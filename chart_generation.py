import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any

def create_revenue_chart(historical_revenue: List[Dict[str, Any]]):
    """Create a bar chart for historical revenue trends."""
    years = [data["year"] for data in historical_revenue]
    revenues = [data["revenue"] for data in historical_revenue]
    
    fig = go.Figure(data=[
        go.Bar(x=years, y=revenues, text=revenues, textposition='auto')
    ])
    fig.update_layout(
        title="Historical Revenue Trends",
        xaxis_title="Year",
        yaxis_title="Revenue (USD)",
        yaxis_tickformat=',.0f'
    )
    return fig

def create_asset_composition_chart(asset_composition: Dict[str, float]):
    """Create a donut chart for asset composition."""
    labels = list(asset_composition.keys())
    values = list(asset_composition.values())
    
    fig = px.pie(
        names=labels,
        values=values,
        title="Asset Composition",
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig
