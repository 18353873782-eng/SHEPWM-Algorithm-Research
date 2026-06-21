import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. 页面基本配置
st.set_page_config(page_title="SHEPWM算法研究成果展示", layout="wide")

st.title("🎓三电平变换器SHEPWM算法研究与仿真")
st.markdown("---")

# 2. 侧边栏：项目核心亮点
st.sidebar.header("📌 项目核心指标")
st.sidebar.success("✅ 目标谐波消除率：> 98%")
st.sidebar.success("✅ 算法收敛精度：10^-6 量级")
st.sidebar.success("✅ 交付成果：独立开发算法求解 GUI")
st.sidebar.markdown("---")
st.sidebar.write("**研究对象**：T型三电平逆变器")
st.sidebar.write("**核心算法**：多目标粒子群 (MOPSO)")

# --- 第一板块：理论建模 ---
st.header("1. 数学建模与问题定义 (Mathematical Modeling)")
col_math1, col_math2 = st.columns([1, 1])

with col_math1:
    st.write("针对三电平变换器，基于傅里叶级数分解建立非线性超越方程组。目标是在极低开关频率下，精准消除 5、7、11、13 次低次谐波。")
    st.latex(r'''
    \begin{cases}
    \frac{4}{\pi} \sum_{i=1}^{N} (-1)^{i+1} \cos(\alpha_i) = M \\
    \sum_{i=1}^{N} (-1)^{i+1} \cos(n\alpha_i) = 0, \quad n=5,7,11,13
    \end{cases}
    ''')

with col_math2:
    st.info("""
    **💡 算法挑战与对策**：
    - **挑战**：方程组具有高度非线性，对初值极其敏感。
    - **对策**：引入 **MOPSO** 算法，通过全局寻优获取最优解集。
    """)

st.markdown("---")

# --- 第二板块：核心算法实现 (新增：代码展示) ---
st.header("2. 核心算法实现 (Algorithm Snippets)")
st.write("以下展示了 MATLAB 中针对 SHEPWM 方程组构建的**适应度函数 (Fitness Function)** 核心逻辑，体现了多目标优化的思想：")

# 使用 st.code 展示代码，非常专业
code_snippet = """
function fitness = shepwm_obj(alpha, M, n_harmonics)
    % alpha: 开关角矢量, M: 调制度, n_harmonics: 待消除谐波次数
    
    % 1. 计算基波幅值偏差 (Fundamental Deviation)
    fundamental = (4/pi) * sum((-1).^(1:length(alpha)+1) .* cos(alpha));
    error_m = abs(fundamental - M);

    % 2. 计算各次谐波幅值总和 (Harmonic Residuals)
    error_h = 0;
    for i = 1:length(n_harmonics)
        h_val = (4/(n_harmonics(i)*pi)) * sum((-1).^(1:length(alpha)+1) .* cos(n_harmonics(i)*alpha));
        error_h = error_h + abs(h_val);
    end

    % 3. 综合目标函数 (加权优化)
    fitness = error_m * 100 + error_h; 
end
"""
st.code(code_snippet, language='matlab')

st.markdown("---")

# --- 第三板块：系统架构与工具开发 ---
st.header("3. 系统架构与工具开发 (System & Tools)")
col_img1, col_img2 = st.columns(2)

with col_img1:
    st.subheader("A. 仿真系统拓扑")
    if os.path.exists("topo.png"):
        st.image("topo.png", caption="基于 Simulink 搭建的 T 型三电平变换器主电路模型", use_container_width=True)
    else:
        st.warning("请上传 topo.png")

with col_img2:
    st.subheader("B. 自主开发求解工具 (GUI)")
    if os.path.exists("gui.png"):
        st.image("gui.png", caption="基于 MATLAB 开发的 SHEPWM 算法求解与可视化平台", use_container_width=True)
    else:
        st.warning("请上传 gui.png")

st.markdown("---")

# --- 第四板块：仿真验证与数据量化 ---
st.header("4. 仿真验证与数据量化 (Verification & Data)")

if os.path.exists("result.png"):
    st.image("result.png", caption="FFT 频谱分析：目标谐波被精准消除", use_container_width=True)

# 修复乱码：使用 $\alpha$ 代替直接输入字符
st.write(r"下表展示了通过 MOPSO 算法获取的部分最优开关角 $\alpha$ (单位: deg) 及消谐后性能指标：")

data = {
    "调制度 (M)": [0.2, 0.4, 0.6, 0.8, 0.9],
    "Alpha 1": [38.29, 31.55, 26.44, 24.12, 23.53],
    "Alpha 2": [41.59, 35.21, 31.08, 29.45, 28.58],
    "Alpha 3": [52.00, 46.88, 42.15, 40.02, 38.88],
    "THD (改善后)": ["42.77%", "41.25%", "38.56%", "40.12%", "44.44%"]
}
st.table(pd.DataFrame(data))

st.markdown("---")
st.caption("© 孙童舒|控制工程研究生作品集")
st.write("⚠️ **注**：受知识产权保护，完整源代码及仿真模型细节不在此公开展示。")
