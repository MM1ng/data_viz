"""
可视化模块
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

def line_chart(df, x_col, y_cols, title="", x_label="", y_label=""):
    """创建折线图"""
    fig = go.Figure()
    
    if isinstance(y_cols, str):
        y_cols = [y_cols]
    
    for col in y_cols:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[col],
                mode='lines+markers',
                name=col,
                hovertemplate=f'<b>{col}</b><br>{x_label}: %{{x}}<br>{y_label}: %{{y:.2f}}<extra></extra>'
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode='x unified',
        template='plotly_white',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def bar_chart(df, x_col, y_col, title="", x_label="", y_label=""):
    """创建柱状图"""
    fig = px.bar(
        df, x=x_col, y=y_col,
        title=title,
        labels={x_col: x_label, y_col: y_label},
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    return fig

def map_chart(df, lat_col, lon_col, color_col, title=""):
    """创建地图"""
    if lat_col not in df.columns or lon_col not in df.columns:
        return None
    
    df_map = df.dropna(subset=[lat_col, lon_col])
    if len(df_map) == 0:
        return None
    
    fig = px.scatter_mapbox(
        df_map,
        lat=lat_col,
        lon=lon_col,
        color=color_col if color_col in df_map.columns else None,
        zoom=3,
        height=500,
        title=title,
        mapbox_style="open-street-map"
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    return fig

def distribution_chart(df, col, title="", bins=30):
    """创建分布图"""
    fig = px.histogram(
        df, x=col, title=title, nbins=bins,
        color_discrete_sequence=[COLOR_PALETTE[0]]
    )
    fig.update_layout(
        template='plotly_white',
        height=400,
        showlegend=False
    )
    return fig

def box_plot(df, x_col, y_col, title=""):
    """创建箱线图"""
    fig = px.box(df, x=x_col, y=y_col, title=title, color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(template='plotly_white', height=400)
    return fig

def correlation_heatmap(df, title="相关性热力图"):
    """创建相关性热力图"""
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr_matrix = numeric_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>相关性: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(title=title, height=500, template='plotly_white')
    return fig
