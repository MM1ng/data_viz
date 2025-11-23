"""
概览页面
"""
import streamlit as st
import pandas as pd
from utils.viz import line_chart, bar_chart
from utils.prep import calculate_kpis

def render(df, tables, filters):
    st.header("数据概览")
    
    kpis = calculate_kpis(df, filters)
    
    st.subheader("关键指标")
    col1, col2, c3, c4 = st.columns(4)
    
    with col1:
        if 'avg_temperature' in kpis:
            st.metric("平均温度", f"{kpis['avg_temperature']:.1f}°C")
    
    with col2:
        if 'avg_humidity' in kpis:
            st.metric("平均湿度", f"{kpis['avg_humidity']:.1f}%")
    
    with c3:
        if 'avg_pressure' in kpis:
            st.metric("平均气压", f"{kpis['avg_pressure']:.2f} kPa")
    
    with c4:
        st.metric("总记录数", f"{kpis.get('total_records', 0):,}")
    
    # 时间趋势
    if 'timeseries' in tables and len(tables['timeseries']) > 0:
        st.subheader("时间趋势分析")
        
        numeric_cols = [col for col in tables['timeseries'].columns 
                       if col not in ['date', 'date_only'] and pd.api.types.is_numeric_dtype(tables['timeseries'][col])]
        
        if numeric_cols:
            selected_vars = st.multiselect(
                "选择要显示的变量",
                numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))],
                key="timeseries_vars"
            )
            
            if selected_vars:
                fig = line_chart(
                    tables['timeseries'],
                    'date',
                    selected_vars,
                    title="气候变量随时间变化趋势",
                    x_label="日期",
                    y_label="数值"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # 天气类型比较
    if 'by_weather' in tables and len(tables['by_weather']) > 0:
        st.subheader("天气类型分析")
        
        numeric_cols = [col for col in tables['by_weather'].columns 
                       if col != 'weather' and pd.api.types.is_numeric_dtype(tables['by_weather'][col])]
        
        if numeric_cols:
            selected_metric = st.selectbox(
                "选择比较指标",
                numeric_cols,
                key="weather_metric"
            )
            
            df_sorted = tables['by_weather'].sort_values(selected_metric, ascending=False)
            fig = bar_chart(
                df_sorted,
                'weather',
                selected_metric,
                title=f"不同天气类型的 {selected_metric} 比较",
                x_label="天气类型",
                y_label=selected_metric
            )
            st.plotly_chart(fig, use_container_width=True)
