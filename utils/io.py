"""
数据加载模块
"""
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path("data")
DATASET_URL = "https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data"
DATASET_NAME = "Climate and Atmospheric Conditions Data"

@st.cache_data(show_spinner="正在加载数据...")
def load_data():
    """加载气候数据"""
    csv_files = list(DATA_DIR.glob("*.csv"))
    
    if csv_files:
        df = pd.read_csv(csv_files[0])
        # 不再在全局显示加载成功的横幅；侧边栏会显示更友好的数据信息
        return df
    else:
        st.warning("未找到数据文件，请将CSV文件放在data/目录下")
        return None

def get_dataset_info():
    """返回数据集信息"""
    return {
        "name": DATASET_NAME,
        "url": DATASET_URL
    }
