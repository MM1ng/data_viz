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
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

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

# 标题（将在侧边栏渲染后显示，确保语言选择生效）

# 侧边栏
with st.sidebar:
    # 显示 logo 图片
    st.image("assets/logo1.png", width=120)
    st.image("assets/logo2.png", width=120)

    # 语言选择（放在联系人之前，确保联系人会跟随语言即时更新）
    if 'lang' not in st.session_state:
        st.session_state.lang = 'en'

    lang_choice = st.radio(
        "语言 / Language",
        ("中文", "English"),
        index=0 if st.session_state.lang == 'zh' else 1,
        key="lang_selector",
        label_visibility="collapsed"
    )

    # 立即更新标准化的语言代码，供后续控件使用
    st.session_state.lang = 'zh' if lang_choice == '中文' else 'en'

    # 个人和教授信息（根据语言切换姓名显示）
    if st.session_state.lang == 'en':
        st.markdown("""
        <div class="contact-info">
            <p><strong>Jiaming Hu</strong><br>jiaming.hu@efrei.net</p>
            <p><strong>Mano Joseph Mathew</strong><br>mano.mathew@efrei.fr</p>
        </div>
        <hr style="margin: 10px 0;">
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="contact-info">
            <p><strong>胡家铭</strong><br>jiaming.hu@efrei.net</p>
            <p><strong>Mano Joseph Mathew</strong><br>mano.mathew@efrei.fr</p>
        </div>
        <hr style="margin: 10px 0;">
        """, unsafe_allow_html=True)

    st.header("控制面板" if st.session_state.lang == 'zh' else "Control Panel")

    # 页面选择（根据当前语言切换标签）
    st.subheader("导航" if st.session_state.lang == 'zh' else "Navigation")
    page_options = ["介绍", "概览", "深入分析", "结论"] if st.session_state.lang == 'zh' else ["Introduction", "Overview", "Deep Dives", "Conclusions"]
    page = st.radio(
        "选择页面" if st.session_state.lang == 'zh' else "Select page",
        page_options,
        index=0,
        key="page_selector",
        label_visibility="collapsed"
    )

    # normalize page back to Chinese keys for routing internal logic (use zh keys)
    if st.session_state.lang == 'en':
        mapping = {"Introduction": "介绍", "Overview": "概览", "Deep Dives": "深入分析", "Conclusions": "结论"}
        page = mapping.get(page, page)

    st.session_state.page = page
    st.markdown("---")
    
    # 数据信息 / Data info
    st.subheader("数据信息" if st.session_state.lang == 'zh' else "Data information")
    st.success("数据加载成功" if st.session_state.lang == 'zh' else "Data loaded successfully")
    
    with st.expander("数据详情" if st.session_state.lang == 'zh' else "Dataset details"):
        st.write(("**总记录数**" if st.session_state.lang == 'zh' else "**Total records**") + f": {len(df_clean):,}")
        st.write(("**总列数**" if st.session_state.lang == 'zh' else "**Total columns**") + f": {len(df_clean.columns)}")
        
        if 'date' in df_clean.columns:
            min_date = df_clean['date'].min()
            max_date = df_clean['date'].max()
            if st.session_state.lang == 'zh':
                st.write(f"**日期范围**: {min_date.strftime('%Y-%m-%d')} 至 {max_date.strftime('%Y-%m-%d')}")
            else:
                st.write(f"**Date range**: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    
    # 过滤器
    st.subheader("过滤器" if st.session_state.lang == 'zh' else "Filters")
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
                    ("日期范围" if st.session_state.lang == 'zh' else "Date range"),
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
    st.subheader("应用信息" if st.session_state.lang == 'zh' else "App information")
    st.caption(("版本" if st.session_state.lang == 'zh' else "Version") + ": 1.0.0")
    
    if st.button("重置过滤器" if st.session_state.lang == 'zh' else "Reset filters"):
        st.rerun()

# 在侧边栏渲染之后再显示标题和数据来源，确保语言选择先被处理
if st.session_state.lang == 'en':
    st.markdown('<div class="main-header">Climate and Atmospheric Conditions - Story</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-header">气候与大气条件数据故事仪表板</div>', unsafe_allow_html=True)

dataset_info = get_dataset_info()
st.caption(f"{'Data source' if st.session_state.lang == 'en' else '数据来源'}: {dataset_info['name']}")

# 主内容区域
if page == "介绍":
    intro.render(st.session_state.lang)
elif page == "概览":
    overview.render(df_clean, tables, filters, st.session_state.lang)
elif page == "深入分析":
    deep_dives.render(df_clean, tables, filters, st.session_state.lang)
elif page == "结论":
    conclusions.render(df_clean, tables, filters, st.session_state.lang)

# 页脚
st.markdown("---")
if st.session_state.lang == 'en':
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Climate & Atmospheric Conditions Story Dashboard | Data Visualization Project</p>
        <p>Built with Streamlit | Data source: <a href="https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data" target="_blank">Kaggle</a></p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>气候与大气条件数据故事仪表板 | 数据可视化项目</p>
        <p>使用 Streamlit 构建 | 数据来源: <a href="https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data" target="_blank">Kaggle</a></p>
    </div>
    """, unsafe_allow_html=True)
