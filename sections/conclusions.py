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

        - **Long-term changes**: Temperature and dew point show highly consistent trends, with clear seasonal fluctuations—higher in summer, lower in winter—reflecting typical seasonal patterns.
        - **Extreme events**: Humidity fluctuates greatly, with high values in summer and lower in winter. Some months (e.g., July, August) show humidity peaks, possibly related to rainfall or weather systems.
        - **Periodicity**: All three variables show annual cycles, and extreme values often appear during seasonal transitions, such as spring and autumn.
        - **Data distribution**: No obvious abnormal extreme events are found; overall data distribution is stable and suitable for further correlation and pattern analysis.

        ### 2. Variable relationship insights


        - **Correlation patterns**:
            - Temperature and dew point show a very strong positive correlation (r=0.933), indicating highly consistent trends.
            - Humidity and pressure have a moderate negative correlation (r≈-0.22~-0.24), meaning humidity tends to decrease as pressure rises.
            - Visibility and humidity show a strong negative correlation (r=-0.63), i.e., higher humidity leads to lower visibility, which matches meteorological phenomena.
            - Wind speed has weak correlations with other variables, indicating its changes are not strongly linked to temperature or humidity.
        - **Causal clues**: While correlation does not imply causation, strongly correlated variables can be prioritized for further modeling and mechanism analysis.

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

        - **长期变化**：温度和露点整体趋势一致，呈现明显季节性波动，夏季升高、冬季降低，反映出典型的季节变化特征。
        - **极端事件**：湿度波动较大，夏季高值明显，冬季略有下降，部分月份（如7月、8月）湿度峰值突出，可能与降水或天气系统有关。
        - **周期性**：三个变量在年内均有周期性变化，极端值多出现在季节交替时段，如春季和秋季。
        - **数据分布**：未发现明显异常极端事件，整体数据分布较为平稳，适合后续做相关性和模式分析。
        
        ### 2. 变量关系洞察

        - **相关性模式**：
            - 温度（temperature）与露点（dew_point）之间呈现极强正相关（r=0.933），说明两者变化趋势高度一致。
            - 湿度（humidity）与气压（pressure）之间存在中等负相关（r≈-0.22~-0.24），表明气压升高时湿度略有下降。
            - 能见度（visibility）与湿度呈现较强负相关（r=-0.63），即湿度高时能见度降低，符合实际气象现象。
            - 风速（wind_speed）与其他变量相关性较弱，说明风速变化与温度、湿度等关系不显著。
        - **因果关系线索**：虽然相关性不等于因果关系，但强相关变量可作为后续建模和机制分析的重点对象。
        
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
        - **机器学习**：应用ML模型进行预测和天气模式识别
        - **交互性**：增加更多交互式功能
        """)
