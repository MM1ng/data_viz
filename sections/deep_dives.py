"""
深入分析页面
"""
import streamlit as st
import pandas as pd
import numpy as np
from utils.viz import distribution_chart, box_plot, correlation_heatmap

def render(df, tables, filters):
    st.header("深入分析")
    
    # 分布分析
    st.subheader("变量分布分析")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_var = st.selectbox("选择要分析的变量", numeric_cols, key="dist_var")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_dist = distribution_chart(df, selected_var, title=f"{selected_var} 分布直方图")
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            st.markdown("### 统计摘要")
            stats = df[selected_var].describe()
            st.metric("均值", f"{stats['mean']:.2f}")
            st.metric("中位数", f"{stats['50%']:.2f}")
            st.metric("标准差", f"{stats['std']:.2f}")
            st.metric("最小值", f"{stats['min']:.2f}")
            st.metric("最大值", f"{stats['max']:.2f}")
    
    # 天气类型分组比较
    if 'weather' in df.columns and numeric_cols:
        st.subheader("天气类型分组比较")
        
        col1, col2 = st.columns(2)
        with col1:
            value_var = st.selectbox("选择数值变量", numeric_cols, key="box_value")
        
        if value_var:
            # 限制天气类型数量
            weather_counts = df['weather'].value_counts()
            top_weathers = weather_counts.head(10).index
            df_filtered = df[df['weather'].isin(top_weathers)]
            
            fig_box = box_plot(
                df_filtered,
                'weather',
                value_var,
                title=f"{value_var} 按天气类型分组比较"
            )
            st.plotly_chart(fig_box, use_container_width=True)
    
    # 相关性分析
    if len(numeric_cols) > 1:
        st.subheader("变量相关性分析")
        
        selected_vars = st.multiselect(
            "选择要分析相关性的变量",
            numeric_cols,
            default=numeric_cols[:min(8, len(numeric_cols))],
            key="corr_vars"
        )
        
        if len(selected_vars) > 1:
            df_corr = df[selected_vars].dropna()
            
            if len(df_corr) > 0:
                fig_corr = correlation_heatmap(df_corr, title="变量相关性矩阵")
                st.plotly_chart(fig_corr, use_container_width=True)
                
                # 找出最强相关性
                corr_matrix = df_corr.corr()
                corr_matrix = corr_matrix.where(
                    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
                )
                
                max_corr = corr_matrix.max().max()
                min_corr = corr_matrix.min().min()
                
                if abs(max_corr) > abs(min_corr):
                    pair = corr_matrix.stack().idxmax()
                    st.success(f"**最强正相关**：{pair[0]} 和 {pair[1]} (r = {max_corr:.3f})")
                else:
                    pair = corr_matrix.stack().idxmin()
                    st.info(f"**最强负相关**：{pair[0]} 和 {pair[1]} (r = {min_corr:.3f})")
