import pandas as pd
from dataclasses import dataclass
from typing import Optional
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils
from datetime import datetime
import io

@dataclass
class SalesPeak:
    peak_date: str
    peak_sales: float
    total_sales: float
    avg_sales: float
    days: int

class SalesAnalyzer:
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.peak: Optional[SalesPeak] = None
    
    @property
    def is_valid(self) -> bool:
        return self.df is not None and len(self.df) >= 2
    
    def load_sales_excel(self, file_content: bytes, filename: str) -> bool:
        """Validate EXACTLY 2 columns: Date, Sales_USD"""
        try:
            df = pd.read_excel(io.BytesIO(file_content))
            
            # ✅ BUSINESS VALIDATION: Exactly 2 columns
            if df.shape[1] != 2:
                raise ValueError("Must have EXACTLY 2 columns: Date, Sales_USD")
            
            # Column validation
            df.columns = ['Date', 'Sales_USD']  # Standardize
            if not pd.api.types.is_datetime64_any_dtype(df['Date']):
                df['Date'] = pd.to_datetime(df['Date'])
            
            # Sales must be numeric
            df['Sales_USD'] = pd.to_numeric(df['Sales_USD'], errors='coerce')
            df = df.dropna()
            
            if len(df) < 2:
                raise ValueError("Need at least 2 data points for analysis")
            
            # If all validations pass, set self.df
            self.df = df
            
            # Calculate peak
            peak_idx = self.df['Sales_USD'].idxmax()
            self.peak = SalesPeak(
                peak_date=self.df.loc[peak_idx, 'Date'].strftime('%Y-%m-%d'),
                peak_sales=float(self.df.loc[peak_idx, 'Sales_USD']),
                total_sales=float(self.df['Sales_USD'].sum()),
                avg_sales=float(self.df['Sales_USD'].mean()),
                days=len(self.df)
            )
            
            return True
        except Exception as e:
            # Reset state on failure
            self.df = None
            self.peak = None
            return False
    
    def create_peak_sales_graph(self) -> str:
        """Graph with HIGHEST sales date MARKED RED"""
        fig = go.Figure()
        
        # Line + markers
        fig.add_trace(go.Scatter(
            x=self.df['Date'], y=self.df['Sales_USD'],
            mode='lines+markers',
            name='Daily Sales ($)',
            line=dict(color='blue')
        ))
        
        # ✅ HIGHEST POINT MARKED RED
        peak_x = [self.peak.peak_date]
        peak_y = [self.peak.peak_sales]
        fig.add_trace(go.Scatter(
            x=peak_x, y=peak_y,
            mode='markers+text',
            name=f'PEAK: ${self.peak.peak_sales}',
            marker=dict(color='red', size=15, symbol='star'),
            text=peak_x,
            textposition="top center",
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"Sales Trend - Peak: ${self.peak.peak_sales} on {self.peak.peak_date}",
            xaxis_title="Date",
            yaxis_title="Sales (USD)",
            height=500,
            template="plotly_white"
        )
        
        return plotly.utils.PlotlyJSONEncoder().encode(fig)
