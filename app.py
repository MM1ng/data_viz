"""
气候与大气条件数据故事仪表板
主应用文件
"""
import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from utils.io import load_data, get_dataset_info
from utils.prep import clean_data, make_tables
from sections import intro, overview, deep_dives, conclusions

# 页面配置
st.set_page_config(
    page_title="气候与大气条件数据故事",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'page' not in st.session_state:
    st.session_state.page = "介绍"

# 数据加载
@st.cache_data(show_spinner="正在加载和预处理数据...")
def get_processed_data():
    """加载和预处理数据"""
    df_raw = load_data()
    if df_raw is None:
        return None, None, {}
    
    df_clean = clean_data(df_raw)
    if df_clean is None:
        return None, None, {}
    
    tables = make_tables(df_clean)
    return df_raw, df_clean, tables

# 加载数据
df_raw, df_clean, tables = get_processed_data()

if df_clean is None:
    st.error("数据加载失败，请检查数据文件")
    st.stop()

# 标题
st.markdown('<div class="main-header">气候与大气条件数据故事仪表板</div>', unsafe_allow_html=True)

dataset_info = get_dataset_info()
st.caption(f"数据来源: {dataset_info['name']}")

# 侧边栏
with st.sidebar:
    st.header("控制面板")
    
    # 页面选择
    st.subheader("导航")
    page = st.radio(
        "选择页面",
        ["介绍", "概览", "深入分析", "结论"],
        index=0,
        key="page_selector",
        label_visibility="collapsed"
    )
    
    st.session_state.page = page
    st.markdown("---")
    
    # 数据信息
    st.subheader("数据信息")
    st.success("数据加载成功")
    
    with st.expander("数据详情"):
        st.write(f"**总记录数**: {len(df_clean):,}")
        st.write(f"**总列数**: {len(df_clean.columns)}")
        
        if 'date' in df_clean.columns:
            min_date = df_clean['date'].min()
            max_date = df_clean['date'].max()
            st.write(f"**日期范围**: {min_date.strftime('%Y-%m-%d')} 至 {max_date.strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    
    # 过滤器
    st.subheader("过滤器")
    filters = {}
    
    # 日期范围过滤器
    if 'date' in df_clean.columns:
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        df_dates = df_clean['date'].dropna()
        
        if len(df_dates) > 0:
            min_date = df_dates.min().date()
            max_date = df_dates.max().date()
            
            if min_date < max_date:
                date_range = st.date_input(
                    "日期范围",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="date_filter"
                )
                
                if isinstance(date_range, tuple) and len(date_range) == 2:
                    filters['date_range'] = date_range
                elif isinstance(date_range, date):
                    filters['date_range'] = (date_range, max_date)
    
    st.markdown("---")
    
    # 应用信息
    st.subheader("应用信息")
    st.caption("版本: 1.0.0")
    
    if st.button("重置过滤器"):
        st.rerun()

# 主内容区域
if page == "介绍":
    intro.render()
elif page == "概览":
    overview.render(df_clean, tables, filters)
elif page == "深入分析":
    deep_dives.render(df_clean, tables, filters)
elif page == "结论":
    conclusions.render(df_clean, tables, filters)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>气候与大气条件数据故事仪表板 | 数据可视化项目</p>
    <p>使用 Streamlit 构建 | 数据来源: <a href="https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data" target="_blank">Kaggle</a></p>
</div>
""", unsafe_allow_html=True)
