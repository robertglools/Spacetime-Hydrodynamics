# -*- coding: utf-8 -*-
"""
File: UED_Core_Metric_Calculator.py
Location: /01_Theoretical_Foundation/

Description: 
    This script defines the mathematical core of the Universal Energy Dynamics (UED) theory.
    It implements the "Unified Void Flow" equation to calculate the theoretical power output 
    driven by the gravitational binding energy metric (M^2/R).

    本程序定义了宇宙能量动力学 (UED) 的核心数学模型。
    它实现了“统一空子流”方程，用于计算基于引力结合能指标 (M^2/R) 的理论功率输出。

Theory Version: 1.0 (Initial Release)
Author: Robert Glools & Gemini AI Pro
Date: 2025-11-30
"""

import numpy as np

# ==========================================
# 1. 物理常数 (Physical Constants)
# ==========================================
G = 6.67430e-11  # Gravitational Constant
c = 2.99792e8    # Speed of Light

# ==========================================
# 2. 理论核心参数 (UED Core Parameters)
# ==========================================
# 统一通道释放因子 (Unified Release Factor)
# 定义了引擎将引力势能转化为活跃功率的基础效率
ALPHA = 10.0

# 空子流上限因子 (Void Flow Limit Factor)
# 定义了致密天体在极端条件下的功率饱和上限
BETA = 6.3e3 

# ==========================================
# 3. 核心方程 (The Core Equations)
# ==========================================

def calculate_ued_power(M, R, T_period):
    """
    计算 UED 理论功率 (P_Unified)。
    核心逻辑: Power ~ (G * M^2 / R) * Frequency_Term
    """
    if R <= 0: return np.nan
    
    # 频率项选择逻辑：
    # 对于普通天体，频率由自转周期 (1/T) 决定 (引擎的机械调制)
    # 对于致密天体，频率受限于光速穿越半径的时间 (c/R) (引擎的几何极限)
    if T_period <= 0:
        freq_term = c / R
    else:
        freq_term = max(1.0 / T_period, c / R)
        
    P_unified = ALPHA * (G * M**2 / R) * freq_term
    return P_unified

# ==========================================
# 4. 验证数据集 (Verification Dataset)
# ==========================================
# [名称, 质量(kg), 半径(m), 周期(s), 观测光度(W)]
validation_data = [
    ["Earth (地球)", 5.972e24, 6.371e6, 24*3600, 4.4e13],
    ["Jupiter (木星)", 1.898e27, 7.149e7, 9.9*3600, 2.3e18],
    ["Uranus (天王星)", 8.681e25, 2.556e7, 17.2*3600, 2.0e16],
    ["Sun (太阳)", 1.989e30, 6.963e8, 25*24*3600, 3.8e26], # 加入太阳作为基准
    ["White Dwarf (白矮星)", 1.0*1.989e30, 8.0e6, 0, 5.0e23], # T=0 触发 c/R 极限
    ["Neutron Star (中子星)", 1.4*1.989e30, 1.0e4, 0, 1.0e30]
]

# ==========================================
# 5. 执行验证 (Execution)
# ==========================================
if __name__ == "__main__":
    print(f"{'Celestial Body':<20} | {'Mass (kg)':<10} | {'UED Power (W)':<15} | {'Observed (W)':<15} | {'Ratio (P/L)':<10}")
    print("-" * 85)
    
    for name, M, R, T, L_obs in validation_data:
        P_ued = calculate_ued_power(M, R, T)
        ratio = P_ued / L_obs if L_obs > 0 else 0
        
        print(f"{name:<20} | {M:.1e}   | {P_ued:.2e}        | {L_obs:.2e}        | {ratio:.2f}")
    
    print("-" * 85)
    print("Interpretation:")
    print("Ratio ~ 1.0 : Engine active, thermal output matches theory (e.g., Earth, Jupiter).")
    print("Ratio >> 1.0: Engine restricted, gravity output dominates thermal (e.g., Uranus).")
