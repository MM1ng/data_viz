"""
介绍页面
"""
import streamlit as st
from utils.io import get_dataset_info

def render(lang: str = 'zh'):
    if lang == 'en':
        st.header("Climate and Atmospheric Conditions - Story")
        st.markdown("""
        ### Why this matters

        Climate change is one of the most pressing global challenges of the 21st century. Understanding patterns in climate and atmospheric conditions helps to:

        - **Predict extreme weather events**: help communities prepare
        - **Support sustainable development**: inform policy decisions
        - **Optimize resource allocation**: guide agriculture, energy, and urban planning
        - **Advance scientific research**: improve understanding of the climate system
        """)

        st.markdown("""
        ### Study goals

        This analysis aims to answer the following key questions:

        1. **Time trends**: How have climate conditions changed over recent years?
        2. **Variable relationships**: How are temperature, humidity, pressure, wind speed, etc. related?
        3. **Weather patterns**: What are the distributions and characteristics of different weather types?
        4. **Anomaly detection**: Are there extreme events or anomalous patterns?
        """)

        st.markdown("### Dataset information")
        dataset_info = get_dataset_info()

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Dataset name**: {dataset_info['name']}")
        with col2:
            st.info(f"**Source**: [Kaggle dataset]({dataset_info['url']})")

        st.markdown("### Data notes")
        st.warning("""
        - **Time range**: The temporal coverage may be limited
        - **Geographic coverage**: Data may not cover all regions
        - **Data quality**: There may be missing values or measurement errors
        - **Sampling methods**: Collection methods may affect representativeness
        """)
    else:
        st.header("气候与大气条件数据故事")
        
        st.markdown("""
        ### 为什么这很重要？
        
        气候变化是21世纪最紧迫的全球挑战之一。理解气候和大气条件的变化模式对于：
        
        - **预测极端天气事件**：帮助社区做好防灾准备
        - **支持可持续发展**：为政策制定提供数据支持
        - **优化资源配置**：指导农业、能源和城市规划
        - **科学研究**：推进对气候系统的理解
        """)
        
        st.markdown("""
        ### 研究目标
        
        本分析旨在回答以下关键问题：
        
        1. **时间趋势**：气候条件在过去几年中如何变化？
        2. **变量关系**：温度、湿度、气压、风速等变量之间如何相互关联？
        3. **天气模式**：不同天气类型的分布和特征是什么？
        4. **异常检测**：是否存在极端天气事件或异常模式？
        """)
        
        st.markdown("### 数据集信息")
        dataset_info = get_dataset_info()
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**数据集名称**: {dataset_info['name']}")
        with col2:
            st.info(f"**数据来源**: [Kaggle数据集]({dataset_info['url']})")
        
        st.markdown("### 数据注意事项")
        st.warning("""
        - **时间范围**：数据的时间跨度可能有限
        - **地理覆盖**：数据可能不覆盖所有地区
        - **数据质量**：可能存在缺失值或测量误差
        - **采样方法**：数据收集方法可能影响结果的代表性
        """)
