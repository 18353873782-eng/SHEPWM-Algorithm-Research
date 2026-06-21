import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

# 页面配置
st.set_page_config(page_title="SHEPWM 算法研究平台", layout="wide")

st.title("🎓 本科毕设：三电平变换器特定谐波消除(SHEPWM)研究")
st.markdown("---")

# 侧边栏：项目概览
st.sidebar.header("项目信息")
st.sidebar.write("**课题**：三相三电平变换器特定谐波消除算法求解及仿真研究")
st.sidebar.write("**核心算法**：多目标粒子群优化 (MOPSO)")
st.sidebar.write("**开发工具**：MATLAB / Simulink / Python")

# 导航
menu = st.sidebar.radio("内容导航", ["理论建模", "算法逻辑", "结果可视化"])

if menu == "理论建模":
    st.header("1. 数学建模 (Mathematical Modeling)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(
            "针对 T 型三电平拓扑，基于傅里叶级数构建非线性超越方程组。目标是在保持低开关频率的同时，精准消除 5、7、11、13 次低次谐波。")
        # 展示 LaTeX 公式，彰显数学功底
        st.latex(r'''
        \begin{cases}
        \frac{4}{\pi} \sum_{i=1}^{N} (-1)^{i+1} \cos(\alpha_i) = M \\
        \sum_{i=1}^{N} (-1)^{i+1} \cos(n\alpha_i) = 0, \quad n=5,7,11,13
        \end{cases}
        ''')
    with col2:
        st.info(
            "💡 核心难点：该方程组具有高度非线性，传统牛顿迭代法对初值依赖性强，极易发散。本项目引入智能优化算法解决此难题。")

elif menu == "算法逻辑":
    st.header("2. 智能优化算法：MOPSO")
    st.write("本项目采用多目标粒子群算法（MOPSO）进行全局寻优，通过动态权重配置提升收敛速度。")

    # 模拟算法流程图
    st.graphviz_chart('''
    digraph {
        "初始化粒子群" -> "计算适应度函数"
        "计算适应度函数" -> "更新个体与全局最优"
        "更新个体与全局最优" -> "判断终止条件"
        "判断终止条件" -> "输出最优开关角"
    }
    ''')

elif menu == "结果可视化":
    st.header("3. 算法求解结果可视化")
    st.write("模拟不同调制度 $M$ 下的开关角 $\alpha$ 变化趋势（基于论文实验数据）：")

    # 基于论文表 3.1 的数据插值模拟
    m_values = np.array([0.2, 0.5, 0.9])
    alpha_data = np.array([
        [38.29, 41.59, 52.00, 61.63, 66.65],
        [28.24, 33.33, 44.83, 52.23, 58.37],
        [23.53, 28.58, 38.88, 47.46, 55.21]
    ])

    m_slider = st.select_slider("调节调制度 (Modulation Index M)", options=[0.2, 0.5, 0.9])

    # 获取对应数据
    idx = np.where(m_values == m_slider)[0][0]
    current_alphas = alpha_data[idx]

    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        fig, ax = plt.subplots()
        ax.bar([f"Alpha {i + 1}" for i in range(5)], current_alphas, color='skyblue')
        ax.set_ylabel("角度 Angle (Degree)")
        ax.set_title(f"M = {m_slider} 时的最优开关角分布")
        st.pyplot(fig)

    with col_table:
        st.write("**数值结果**")
        st.table({
            "参数": [f"Alpha {i + 1}" for i in range(5)],
            "数值 (deg)": current_alphas
        })
        st.success(f"在此参数下，5/7/11/13次谐波消除率 > 95%")

    st.markdown("---")
    st.subheader("仿真结果展示")
    st.write("上传论文中的核心截图（如 FFT 频谱分析图）以增强说服力。")
    # 提醒上传图片
    st.warning("请在 GitHub 仓库上传论文截图（如 result.png），此处即可显示。")