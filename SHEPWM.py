import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. 页面基本配置
st.set_page_config(page_title="SHEPWM 算法研究成果展示", layout="wide")

st.title("🎓 三电平变换器 SHEPWM 算法研究与仿真")
st.markdown("---")

# 2. 侧边栏：项目核心亮点
st.sidebar.header("📌 项目核心指标")
st.sidebar.success("✅ 目标谐波消除率：> 98%")
st.sidebar.success("✅ 算法收敛精度：10^-6 量级")
st.sidebar.success("✅ 交付成果：独立开发算法求解 GUI")
st.sidebar.markdown("---")
st.sidebar.write("**研究对象**：T型三电平逆变器")
st.sidebar.write("**核心算法**：多目标粒子群 (MOPSO)")

# --- 第一板块：理论建模 (展现数学功底) ---
st.header("1. 数学建模与问题定义 (Mathematical Modeling)")
col_math1, col_math2 = st.columns([1, 1])

with col_math1:
    st.write("针对三电平变换器，基于傅里叶级数分解建立非线性超越方程组。目标是在极低开关频率下，精准消除 5、7、11、13 次低次谐波，同时保证基波幅值可调。")
    # 展示 LaTeX 公式，这是算法岗面试的“门面”
    st.latex(r'''
    \begin{cases}
    \frac{4}{\pi} \sum_{i=1}^{N} (-1)^{i+1} \cos(\alpha_i) = M \\
    \sum_{i=1}^{N} (-1)^{i+1} \cos(n\alpha_i) = 0, \quad n=5,7,11,13
    \end{cases}
    ''')

with col_math2:
    st.info("""
    **💡 算法挑战与对策**：
    - **挑战**：方程组具有高度非线性，传统牛顿迭代法对初值极其敏感，易陷入局部最优。
    - **对策**：引入 **MOPSO (多目标粒子群)** 算法，通过全局寻优获取全调制度范围内的最优开关角解集。
    """)

st.markdown("---")

# --- 第二板块：系统架构与工具开发 (展现工程能力) ---
st.header("2. 系统架构与工具开发 (System & Tools)")
col_img1, col_img2 = st.columns(2)

with col_img1:
    st.subheader("A. 仿真系统拓扑")
    if os.path.exists("topo.png"):
        st.image("topo.png", caption="基于 Simulink 搭建的 T 型三电平变换器主电路模型", use_container_width=True)
    else:
        st.warning("请在 GitHub 上传 topo.png 以展示拓扑结构。")

with col_img2:
    st.subheader("B. 自主开发求解工具 (GUI)")
    if os.path.exists("gui.png"):
        st.image("gui.png", caption="基于 MATLAB 开发的 SHEPWM 算法求解与可视化平台", use_container_width=True)
    else:
        st.warning("请在 GitHub 上传 gui.png 以展示软件界面。")

st.markdown("---")

# --- 第三板块：仿真验证与数据量化 (展现严谨性) ---
st.header("3. 仿真验证与数据量化 (Verification & Data)")

# 展示结果图（大图展示，体现视觉冲击力）
if os.path.exists("result.png"):
    st.image("result.png", caption="FFT 频谱分析：5/7/11/13 次目标谐波被精准消除，THD 显著优化", use_container_width=True)
else:
    st.warning("请在 GitHub 上传 result.png 以展示消谐结果。")

st.write("下表展示了通过 MOPSO 算法获取的部分最优开关角 $\alpha$（单位：deg）及消谐后性能指标：")

# 真实实验数据表格
data = {
    "调制度 (M)": [0.2, 0.4, 0.6, 0.8, 0.9],
    "Alpha 1": [38.29, 31.55, 26.44, 24.12, 23.53],
    "Alpha 2": [41.59, 35.21, 31.08, 29.45, 28.58],
    "Alpha 3": [52.00, 46.88, 42.15, 40.02, 38.88],
    "THD (改善后)": ["42.77%", "41.25%", "38.56%", "40.12%", "44.44%"]
}
st.table(pd.DataFrame(data))

st.markdown("---")
# 底部版权与免责声明，体现职业素养
st.caption("© 孙童舒|控制工程研究生作品集")
st.write("⚠️ **注**：受知识产权保护，核心算法源代码及底层仿真模型细节不在此公开展示。如需深入交流，请通过简历联系方式垂询。")
