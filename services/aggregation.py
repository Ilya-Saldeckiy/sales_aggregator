import pandas as pd
from typing import Optional, List
from datetime import date

def calculate_metrics(df: pd.DataFrame, group_name: Optional[str] = None):
    delivered = df[df['status'] == 'delivered']
    returned_count = len(df[df['status'] == 'returned'])
    delivered_count = len(delivered)
    total_revenue = (delivered['price'] * delivered['quantity']).sum()
    total_cost = (delivered['cost_price'] * delivered['quantity']).sum()
    gross_profit = total_revenue - total_cost
    total_orders = delivered['order_id'].nunique()
    
    return {
        "group": str(group_name) if group_name else "total",
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "gross_profit": round(gross_profit, 2),
        "margin_percent": round((gross_profit / total_revenue * 100), 2) if total_revenue > 0 else 0,
        "total_orders": total_orders,
        "avg_order_value": round(total_revenue / total_orders, 2) if total_orders > 0 else 0,
        "return_rate": round(returned_count / (delivered_count + returned_count) * 100, 2) if (delivered_count + returned_count) > 0 else 0
    }

def get_summary(data: List, date_from: date, date_to: date, marketplace: str = None, group_by: str = None):
    if not data: return []
    df = pd.DataFrame([s.model_dump() for s in data])
    df['sold_at'] = pd.to_datetime(df['sold_at']).dt.date
    mask = (df['sold_at'] >= date_from) & (df['sold_at'] <= date_to)
    if marketplace:
        mask &= (df['marketplace'] == marketplace)
    df = df[mask]
    if df.empty: return []
    if group_by:
        groups = df.groupby(group_by)
        return [calculate_metrics(group, name) for name, group in groups]
    return [calculate_metrics(df)]