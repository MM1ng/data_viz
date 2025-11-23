"""
结论页面
"""
import streamlit as st
import pandas as pd
from utils.prep import validate_data

def render(df, tables, filters, lang: str = 'zh'):
    if lang == 'en':
        st.header("Key insights & recommendations")
        st.subheader("Data quality report")
    else:
        st.header("关键洞察与启示")
        st.subheader("数据质量报告")

    quality_report = validate_data(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total rows" if lang == 'en' else "总记录数", f"{quality_report.get('total_rows', 0):,}")
        st.metric("Total columns" if lang == 'en' else "总列数", quality_report.get('total_columns', 0))
        st.metric("Duplicates" if lang == 'en' else "重复记录", f"{quality_report.get('duplicates', 0):,}")

    with col2:
        missing_stats = quality_report.get('missing_percentage', {})
        if missing_stats:
            max_missing_col = max(missing_stats.items(), key=lambda x: x[1])
            st.metric("Column with most missing" if lang == 'en' else "缺失值最多的列", f"{max_missing_col[0]}: {max_missing_col[1]:.2f}%")
        
        st.metric("Numeric columns" if lang == 'en' else "数值列数", len(quality_report.get('numeric_columns', [])))
        st.metric("Categorical columns" if lang == 'en' else "分类列数", len(quality_report.get('categorical_columns', [])))

    with col3:
        total_cells = quality_report.get('total_rows', 0) * quality_report.get('total_columns', 0)
        missing_cells = sum(quality_report.get('missing_values', {}).values())
        completeness = (1 - missing_cells / total_cells) * 100 if total_cells > 0 else 100
        st.metric("Data completeness" if lang == 'en' else "数据完整性", f"{completeness:.1f}%")

    with st.expander("Detailed missing values report" if lang == 'en' else "详细缺失值报告"):
        missing_df = pd.DataFrame({
            ('Column' if lang == 'en' else '列名'): list(quality_report.get('missing_values', {}).keys()),
            ("Missing count" if lang == 'en' else '缺失数量'): list(quality_report.get('missing_values', {}).values()),
            ("Missing percentage" if lang == 'en' else '缺失百分比'): list(quality_report.get('missing_percentage', {}).values())
        }).sort_values(("Missing percentage" if lang == 'en' else '缺失百分比'), ascending=False)
        
        if len(missing_df) > 0:
            st.dataframe(missing_df, use_container_width=True)

    if lang == 'en':
        st.subheader("Key insights summary")
        st.markdown("""
        ### 1. Time trend insights

        - **Long-term changes**: We observe seasonal patterns and long-term trends in climate variables
        - **Extreme events**: The data may contain records of extreme weather events
        - **Periodicity**: Some variables show annual or seasonal cycles

        ### 2. Variable relationship insights

        - **Correlation patterns**: Correlations reveal internal connections in the climate system
        - **Causal clues**: Correlation does not imply causation but can guide further research

        ### 3. Weather pattern insights

        - **Weather type distribution**: Different weather types show distinct frequencies and characteristics
        - **Climate conditions**: Different weather types correspond to distinct climate conditions (temperature, humidity, etc.)
        """)

        st.subheader("Practical recommendations")
        st.markdown("""
        ### Policy recommendations

        1. **Adaptation strategies**: Develop strategies to adapt to projected climate changes
        2. **Early warning systems**: Use pattern recognition to build extreme weather alerts

        ### Research recommendations

        1. **Model validation**: Use data to validate and improve climate models
        2. **Hypothesis testing**: Support or reject hypotheses about climate change
        """)

        st.subheader("Limitations & notes")
        st.warning("""
        **Data limitations**:

        - **Sample bias**: Data may not represent all regions or periods
        - **Measurement error**: Instrument precision and calibration may affect quality
        - **Time coverage**: The time span may be insufficient for long-term trends

        **Methodological limitations**:

        - **Correlation vs causation**: Correlation does not prove causation
        - **Prediction uncertainty**: Forecasts based on historical data carry uncertainty
        """)

        st.subheader("Next steps")
        st.markdown("""
        - **Expand data sources**: Integrate more datasets to improve completeness
        - **Machine learning**: Apply ML models for prediction and pattern recognition
        - **Interactivity**: Add more interactive features
        - **Mobile optimization**: Improve mobile experience
        """)
    else:
        st.subheader("关键洞察总结")
        
        st.markdown("""
        ### 1. 时间趋势洞察
        
        - **长期变化**：通过时间序列分析，我们观察到气候变量存在明显的季节性模式和长期趋势
        - **极端事件**：数据中可能包含极端天气事件的记录
        - **周期性**：某些变量显示出年度或季节性的周期性变化
        
        ### 2. 变量关系洞察
        
        - **相关性模式**：变量之间的相关性揭示了气候系统的内在联系
        - **因果关系线索**：虽然相关性不等于因果关系，但可以为深入研究提供方向
        
        ### 3. 天气模式洞察
        
        - **天气类型分布**：不同天气类型的出现频率和特征存在显著差异
        - **气候条件**：不同天气类型对应的气候条件（温度、湿度等）有明显区别
        """)
        
        st.subheader("实际应用启示")
        
        st.markdown("""
        ### 对政策制定的启示
        
        1. **气候适应策略**：基于历史趋势，制定适应未来气候变化的策略
        2. **预警系统**：利用模式识别，建立极端天气预警机制
        
        ### 对科学研究的启示
        
        1. **模型验证**：数据可用于验证和改进气候模型
        2. **假设检验**：支持或反驳关于气候变化的假设
        """)
        
        st.subheader("局限性与注意事项")
        
        st.warning("""
        **数据局限性**：
        
        - **样本偏差**：数据可能不代表所有地区或所有时期
        - **测量误差**：仪器精度和校准可能影响数据质量
        - **时间覆盖**：数据的时间跨度可能不足以捕捉长期趋势
        
        **分析方法局限性**：
        
        - **相关性 vs 因果关系**：相关性分析不能证明因果关系
        - **预测不确定性**：基于历史数据的预测存在不确定性
        """)
        
        st.subheader("下一步建议")
        
        st.markdown("""
        - **扩展数据源**：整合更多数据源，提高数据完整性
        - **机器学习**：应用ML模型进行预测和模式识别
        - **交互性**：增加更多交互式功能
        - **移动优化**：优化移动设备体验
        """)
