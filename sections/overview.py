"""
概览页面
"""
import streamlit as st
import pandas as pd
from utils.viz import line_chart, bar_chart
from utils.prep import calculate_kpis

def render(df, tables, filters, lang: str = 'zh'):
    if lang == 'en':
        st.header("Data Overview")
    else:
        st.header("数据概览")
    
    kpis = calculate_kpis(df, filters)
    
    if lang == 'en':
        st.subheader("Key metrics")
    else:
        st.subheader("关键指标")

    col1, col2, c3, c4 = st.columns(4)
    
    with col1:
        if 'avg_temperature' in kpis:
            st.metric("Average temperature" if lang == 'en' else "平均温度", f"{kpis['avg_temperature']:.1f}°C")
    
    with col2:
        if 'avg_humidity' in kpis:
            st.metric("Average humidity" if lang == 'en' else "平均湿度", f"{kpis['avg_humidity']:.1f}%")
    
    with c3:
        if 'avg_pressure' in kpis:
            st.metric("Average pressure" if lang == 'en' else "平均气压", f"{kpis['avg_pressure']:.2f} kPa")
    
    with c4:
        st.metric("Total records" if lang == 'en' else "总记录数", f"{kpis.get('total_records', 0):,}")
    
    # 时间趋势
    if 'timeseries' in tables and len(tables['timeseries']) > 0:
        st.subheader("Time series analysis" if lang == 'en' else "时间趋势分析")
        

        if lang == 'zh':
            st.markdown("""
    **具体分析结论：**
    - 温度和露点整体趋势一致，呈现明显季节性波动，夏季升高、冬季降低。
    - 湿度波动较大，夏季高值明显，冬季略有下降，部分月份峰值突出。
    - 三个变量均有周期性变化，极端值多出现在季节交替时段。
    - 未发现明显异常极端事件，数据分布较平稳。
    """)
        elif lang == 'en':
            st.markdown("""
    **Detailed analysis:**
    - Temperature and dew point show highly consistent trends, with clear seasonal fluctuations—higher in summer, lower in winter.
    - Humidity fluctuates greatly, with high values in summer and lower in winter. Some months (e.g., July, August) show humidity peaks, possibly related to rainfall or weather systems.
    - All three variables show annual cycles, and extreme values often appear during seasonal transitions, such as spring and autumn.
    - No obvious abnormal extreme events are found; overall data distribution is stable and suitable for further correlation and pattern analysis.
    """)
        numeric_cols = [col for col in tables['timeseries'].columns 
                   if col not in ['date', 'date_only'] and pd.api.types.is_numeric_dtype(tables['timeseries'][col])]
        
        if numeric_cols:
            selected_vars = st.multiselect(
                "Select variables to display" if lang == 'en' else "选择要显示的变量",
                numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))],
                key="timeseries_vars"
            )
            
            if selected_vars:
                fig = line_chart(
                    tables['timeseries'],
                    'date',
                    selected_vars,
                    title=("Climate variables over time" if lang == 'en' else "气候变量随时间变化趋势"),
                    x_label=("Date" if lang == 'en' else "日期"),
                    y_label=("Value" if lang == 'en' else "数值")
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # 天气类型比较
    if 'by_weather' in tables and len(tables['by_weather']) > 0:
        st.subheader("Weather type analysis" if lang == 'en' else "天气类型分析")
        
        numeric_cols = [col for col in tables['by_weather'].columns 
                       if col != 'weather' and pd.api.types.is_numeric_dtype(tables['by_weather'][col])]
        
        if numeric_cols:
            selected_metric = st.selectbox(
                "Select metric to compare" if lang == 'en' else "选择比较指标",
                numeric_cols,
                key="weather_metric"
            )
            
            df_sorted = tables['by_weather'].sort_values(selected_metric, ascending=False)
            fig = bar_chart(
                df_sorted,
                'weather',
                selected_metric,
                title=(f"Comparison of {selected_metric} across weather types" if lang == 'en' else f"不同天气类型的 {selected_metric} 比较"),
                x_label=("Weather type" if lang == 'en' else "天气类型"),
                y_label=selected_metric
            )
            st.plotly_chart(fig, use_container_width=True)
