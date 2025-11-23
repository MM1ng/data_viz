"""
数据预处理模块
"""
import pandas as pd
import numpy as np

def clean_data(df):
    """清洗数据"""
    if df is None:
        return None
    
    df = df.copy()
    
    # 处理日期列
    if 'Date/Time' in df.columns:
        df['date'] = pd.to_datetime(df['Date/Time'], errors='coerce')
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # 标准化列名
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('/', '_')
    
    # 重命名列以便使用（创建新列后删除原始列，避免重复）
    column_mapping = {
        'Temp_C': 'temperature',
        'Dew_Point_Temp_C': 'dew_point',
        'Rel_Hum_%': 'humidity',
        'Wind_Speed_km_h': 'wind_speed',
        'Visibility_km': 'visibility',
        'Press_kPa': 'pressure',
        'Weather': 'weather'
    }
    
    # 先创建新列
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]
    
    # 然后删除原始列（保留新列名如temperature）
    columns_to_drop = [old_col for old_col in column_mapping.keys() if old_col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop, errors='ignore')
    
    return df

def validate_data(df):
    """验证数据质量"""
    if df is None:
        return {}
    
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
        "duplicates": df.duplicated().sum(),
        "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
        "categorical_columns": list(df.select_dtypes(include=['object']).columns)
    }

def make_tables(df):
    """创建聚合表"""
    if df is None or 'date' not in df.columns:
        return {}
    
    tables = {}
    df_work = df.copy()
    
    # 确保date是datetime类型
    df_work['date'] = pd.to_datetime(df_work['date'], errors='coerce')
    df_work = df_work.dropna(subset=['date'])
    
    if len(df_work) == 0:
        return tables
    
    # 时间序列（按日期聚合）
    numeric_cols = df_work.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 0:
        df_work['date_only'] = df_work['date'].dt.date
        tables['timeseries'] = df_work.groupby('date_only')[numeric_cols].mean().reset_index()
        tables['timeseries']['date'] = pd.to_datetime(tables['timeseries']['date_only'])
    
    # 按月聚合
    df_monthly = df_work.copy()
    df_monthly['year_month'] = df_work['date'].dt.to_period('M')
    if len(numeric_cols) > 0:
        tables['monthly'] = df_monthly.groupby('year_month')[numeric_cols].mean().reset_index()
        tables['monthly']['year_month'] = tables['monthly']['year_month'].astype(str)
    
    # 按年聚合
    df_yearly = df_work.copy()
    df_yearly['year_value'] = df_work['date'].dt.year
    if len(numeric_cols) > 0:
        tables['yearly'] = df_yearly.groupby('year_value')[numeric_cols].mean().reset_index()
        tables['yearly'] = tables['yearly'].rename(columns={'year_value': 'year'})
    
    # 按天气类型聚合
    if 'weather' in df_work.columns:
        if len(numeric_cols) > 0:
            tables['by_weather'] = df_work.groupby('weather')[numeric_cols].mean().reset_index()
    
    return tables

def calculate_kpis(df, filters=None):
    """计算KPI"""
    if df is None:
        return {}
    
    df_filtered = df.copy()
    
    # 应用日期过滤器
    if filters and 'date_range' in filters and filters['date_range']:
        if 'date' in df_filtered.columns:
            start_date, end_date = filters['date_range']
            df_filtered = df_filtered[
                (df_filtered['date'] >= pd.to_datetime(start_date)) &
                (df_filtered['date'] <= pd.to_datetime(end_date))
            ]
    
    kpis = {}
    
    if 'temperature' in df_filtered.columns:
        kpis['avg_temperature'] = df_filtered['temperature'].mean()
        kpis['max_temperature'] = df_filtered['temperature'].max()
        kpis['min_temperature'] = df_filtered['temperature'].min()
    
    if 'humidity' in df_filtered.columns:
        kpis['avg_humidity'] = df_filtered['humidity'].mean()
    
    if 'pressure' in df_filtered.columns:
        kpis['avg_pressure'] = df_filtered['pressure'].mean()
    
    if 'wind_speed' in df_filtered.columns:
        kpis['avg_wind_speed'] = df_filtered['wind_speed'].mean()
        kpis['max_wind_speed'] = df_filtered['wind_speed'].max()
    
    kpis['total_records'] = len(df_filtered)
    
    return kpis
