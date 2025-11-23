# 气候与大气条件数据故事仪表板

一个基于Streamlit的交互式数据可视化仪表板，用于分析和展示气候与大气条件数据。

## 项目概述

本项目是一个数据故事讲述应用，通过交互式可视化引导用户探索气候数据，揭示关键模式和趋势。项目遵循清晰的故事叙述结构：**问题 → 分析 → 洞察 → 启示**。

### 研究目标

- **时间趋势分析**：探索气候条件随时间的变化模式
- **空间分布可视化**：展示不同地区的气候差异
- **变量关系探索**：分析温度、湿度、气压、风速等变量之间的关联
- **异常检测**：识别极端天气事件和异常模式
- **预测性洞察**：从历史数据中提取有价值的见解

## 快速开始

### 环境要求

# Climate and Atmospheric Conditions - Story

This repository contains an interactive Streamlit dashboard for exploring and visualizing climate and atmospheric conditions data.

---

## Overview

The application is built with Streamlit and follows a narrative-driven data visualization approach: Introduction → Analysis → Insights → Recommendations.

Key objectives:

- Time-series analysis of climate variables
- Variable relationship exploration (temperature, humidity, pressure, wind speed, etc.)
- Weather-type comparisons and anomaly detection
- Summary KPIs and data quality reporting

---

## Quick Start

Prerequisites:

- Python 3.8 or newer
- pip

Steps:

1. Clone the repository and enter the project directory:

```bash
git clone git@github.com:MM1ng/data_viz.git
cd data_viz_project
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place your CSV dataset into the `data/` folder. The app will load the first CSV file it finds. The original dataset is available on Kaggle:

https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data

5. Run the app:

```bash
streamlit run app.py
```

Open the URL printed by Streamlit (typically `http://localhost:8501`).
2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place your CSV data into the `data/` directory (or use sample data provided).

5. Run the app:

```bash
streamlit run app.py
```

Open the app at `http://localhost:8501` (or the local URL printed by Streamlit).

---

## Project Structure

```
data_viz_project/
├── app.py                 # Streamlit app
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── sections/              # page modules
├── utils/                 # helpers (load, prep, viz)
├── data/                  # folder for CSV files
└── assets/                # resources (logos etc.)
```

---

## Features

- Time series analysis
- Distributions & box plots
- Weather-type comparisons
- Correlation heatmap
- KPI metrics

---

## Dataset

- Name: Climate and Atmospheric Conditions Data
- Source: Kaggle — https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data

Place your CSV in the `data/` folder; the app will automatically load the first CSV found.

---

## Development Notes

- Use `@st.cache_data` to cache data loading.
- Modular code: pages in `sections/`, helpers in `utils/`.

---

## Contact

- Jiaming Hu — jiaming.hu@efrei.net
- Mano Joseph Mathew — mano.mathew@efrei.fr

---

If you want a separate Chinese README file or other formatting (e.g., two-column web layout), tell me and I will add it as `README_zh.md`.

---

## 目录 / Contents

- 简介 / Introduction
- 快速开始 / Quick Start
- 项目结构 / Project Structure
- 功能与使用 / Features & Usage
- 数据集 / Dataset
- 开发与扩展 / Development & Extensibility
- 许可证与联系 / License & Contact

---

## 简介 / Introduction

该应用以“故事化数据可视化”为核心，通过交互式图表和过滤器，引导用户发现气候变量中的模式、趋势和异常。

This app focuses on data storytelling, guiding users to discover patterns, trends, and anomalies in climate variables using interactive charts and filters.

## 快速开始 / Quick Start

先确保已安装 Python 3.8+。

1. 克隆仓库并进入目录：

```bash
git clone git@github.com:MM1ng/data_viz.git
cd data_viz_project
```

2. 建议创建虚拟环境并激活：

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 将你的 CSV 数据放入 `data/` 目录（或者使用示例数据）：

Download the dataset from Kaggle and put the CSV in the `data/` folder, or use the sample data provided for demo purposes.

5. 运行应用：

```bash
streamlit run app.py
```

打开浏览器访问 `http://localhost:8501`（或 Streamlit 输出的本地 URL）。

Open the app in your browser at `http://localhost:8501` (or the local URL printed by Streamlit).

---

## 项目结构 / Project Structure

```
data_viz_project/
├── app.py                 # 主应用入口 / Streamlit app
├── requirements.txt       # 依赖 / Python dependencies
├── README.md              # 本文件 / This README
├── sections/              # 页面模块 / page modules
├── utils/                 # 工具模块（加载、预处理、可视化）
├── data/                  # 数据目录（放置 CSV）
└── assets/                # 资源（logo 等）
```

---

## 功能与使用 / Features & Usage

- 时间序列分析 / Time series analysis
- 变量分布与箱线图 / Distributions & box plots
- 天气类型比较 / Weather-type comparisons
- 相关性热力图 / Correlation heatmap
- KPI 面板 / KPI metrics
- 侧边栏过滤器（日期、变量、地区）/ Sidebar filters (date range, variables, regions)

交互说明：在侧边栏选择语言（中/英）、页面和过滤条件，图表会实时更新。

Interactions: use the sidebar to switch language (ZH/EN), pages and filters. Charts update interactively.

---

## 数据集 / Dataset

- 名称 / Name: Climate and Atmospheric Conditions Data
- 来源 / Source: Kaggle — https://www.kaggle.com/datasets/saadaliyaseen/climate-and-atmospheric-conditions-data/data

将 CSV 文件放入 `data/` 文件夹，应用将自动加载第一个 CSV 文件。

Place  CSV in the `data/` folder; the app will load the first CSV found automatically.

---

## 开发说明 / Development Notes

- 使用 `@st.cache_data` 优化数据加载。
- 模块化代码结构：`sections/` 存放页面，`utils/` 存放工具。
- 若要扩展：添加新的可视化函数到 `utils/viz.py`，并在相应页面中调用。

Use `@st.cache_data` to cache data loading. The code is modular: pages live in `sections/`, helpers in `utils/`. To extend, add visualization functions to `utils/viz.py` and call them from pages.

---

## 联系 / Contact

- 胡家铭 / Jiaming Hu — jiaming.hu@efrei.net




