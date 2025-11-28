import pandas as pd
import numpy as np

# --- 核心常数 ---
# 空子海相对流速 (v_rel)，来源于独立校准，非拟合参数。
V_REL = 49.6  # km/s

def calculate_v40_proxies(df):
    """
    根据 V4.0 理论公式，计算内部供给代理 (Theta_S) 和有效制动扭矩代理 (Theta_Braking)。
    
    参数:
    df (pd.DataFrame): 包含原始恒星观测数据的 DataFrame。
                       所需列: 'M_sun', 'R_sun', 'Teff_K', 'Age_Gyr', 'vsini_kms'
    
    返回:
    pd.DataFrame: 包含新增对数计算结果的 DataFrame。
    """
    # 将年龄从 Gyr 转换为 Yr 以保持单位一致性，但由于对数关系，
    # 保持 Gyr 单位计算 log10(Theta_S) 即可，常数项被纳入截距。
    
    # --- 1. 内部角动量供给代理 (Theta_S) ---
    # 公式 (2.1): Theta_S = M^(1.5) / (Teff^(2) * t_age)
    df['Theta_S'] = (df['M_sun'] ** 1.5) / (df['Teff_K'] ** 2 * df['Age_Gyr'])
    df['log10(Theta_S)'] = np.log10(df['Theta_S'])

    # --- 2. 有效制动扭矩代理 (Theta_Braking) ---
    # 公式 (2.2): Theta_Braking = R^(4) * (v_eq + v_rel)
    # v_eq 近似于 vsini_kms
    df['Theta_Braking'] = (df['R_sun'] ** 4) * (df['vsini_kms'] + V_REL)
    df['log10(Theta_Braking)'] = np.log10(df['Theta_Braking'])
    
    # 计算非线性耦合比 Beta (用于参考和分析)
    df['Beta_vsini/vrel'] = df['vsini_kms'] / V_REL
    
    return df

def main():
    """
    加载原始数据，执行 V4.0 计算，并保存结果到 Calculated_Results.csv。
    
    注意：在实际 GitHub 部署中，您需要将以下模拟数据替换为从 Raw_Data.csv 加载的代码。
    """
    
    # 模拟 Raw_Data.csv 的数据结构 (根据 V4.0-Stellar-Braking-Verification.md 报告中的表格)
    # 实际部署时应使用 pd.read_csv('Analysis_Data/Raw_Data.csv')
    data = {
        'Identifier': ['Sun', 'HD 26965', 'HD 114613', 'HD 160617', 'HD 134060', 'HD 34411', 'HD 117618', 'HD 10180', 'HD 154088', 'HD 117207', 'HD 168009', 'HD 210918', 'HD 45184', 'HD 192310', 'HD 204961', 'HD 176986', 'HD 215152', 'HD 51608'],
        'M_sun': [1.00, 0.78, 1.28, 1.09, 1.10, 1.07, 1.08, 1.06, 1.04, 1.04, 1.03, 1.03, 1.04, 0.78, 0.78, 0.84, 0.99, 0.85],
        'R_sun': [1.00, 0.74, 1.65, 1.43, 1.38, 1.53, 1.25, 1.34, 1.38, 1.38, 1.35, 1.31, 1.21, 0.81, 0.82, 0.87, 1.05, 0.94],
        'Teff_K': [5772, 5250, 6550, 6200, 6180, 6050, 6100, 5900, 6100, 6080, 5995, 6050, 6070, 5300, 5310, 5450, 5860, 5735],
        'Age_Gyr': [4.6, 10.0, 1.5, 2.5, 2.9, 4.0, 3.2, 4.3, 3.3, 3.0, 4.8, 3.8, 3.5, 9.5, 9.0, 8.8, 4.0, 5.9],
        'vsini_kms': [2.0, 1.3, 7.2, 5.5, 5.1, 5.0, 4.8, 4.5, 4.3, 4.2, 4.1, 4.0, 3.8, 1.4, 1.5, 1.7, 1.8, 1.9]
    }
    df = pd.DataFrame(data)
    
    print("--- 正在执行 V4.0 理论代理变量计算 ---")
    
    # 执行核心计算
    results_df = calculate_v40_proxies(df)
    
    # 提取用于线性回归的关键列
    final_output = results_df[[
        'Identifier', 
        'vsini_kms',
        'Beta_vsini/vrel',
        'log10(Theta_S)', 
        'log10(Theta_Braking)'
    ]]
    
    # 打印和保存结果
    print("\n[INFO] 计算完成。以下为用于线性回归的核心结果：")
    print(final_output)
    
    # 实际部署时应保存到 Analysis_Data/Calculated_Results.csv
    # final_output.to_csv('Analysis_Data/Calculated_Results.csv', index=False, float_format='%.3f')
    print("\n[INFO] 结果已成功计算并准备好保存到 Calculated_Results.csv。")

if __name__ == "__main__":
    main()
