
import pandas as pd
import numpy as np


data = pd.read_csv('new_movie_data.csv')
df = pd.DataFrame(data)
print(df.head())

# 将占比转换为计数
for star in range(1, 6):
    df[f'star{star}_cnt'] = (df[f'stars{star}'] * df['movie_comment_num']).round().astype(int)

print("原始数据（含计数）：")
print(df[['movie_name', 'movie_comment_num'] + [f'stars{i}' for i in range(1, 6)]])

# ---------- 2. 计算全局先验（狄利克雷分布参数alpha） ----------
# 将所有电影的各星级计数累加，得到先验分布
global_counts = df[[f'star{i}_cnt' for i in range(1, 6)]].sum().values
# print(f"各星级计数累加{global_counts}")
# 狄利克雷先验参数通常取平滑值，这里用全局计数作为先验强度
alpha_prior = global_counts * 0.8


# ---------- 3. 定义贝叶斯平滑得分函数 ----------
def bayesian_smoothing_score(row, alpha_prior, star_weights=None):
    """
    计算单部电影的贝叶斯平滑后验期望得分。
    row: 包含各星级计数的行（Series）
    alpha_prior: 各星级的全局先验参数（长度为5的数组）
    star_weights: 各星级对应的权重，默认为 [1,2,3,4,5]
    """
    if star_weights is None:
        star_weights = np.array([1, 2, 3, 4, 5])  # 也可自定义，如[0,0,0,1,2]突出高分

    # 各星级计数
    counts = np.array([row[f'star{i}_cnt'] for i in range(1, 6)])
    N = counts.sum()
    # print(f"各星级计数{counts}")
    # for i in counts:
    #     print(i)

    # 后验狄利克雷参数 = 计数 + 先验参数
    posterior_alpha = counts + alpha_prior
    # print(f"后验参数{posterior_alpha}")
    # 后验期望概率 = posterior_alpha / sum(posterior_alpha)
    posterior_probs = posterior_alpha / posterior_alpha.sum()
    # print(f"后验概率{posterior_probs}")
    # 期望得分 = 权重向量点乘概率
    expected_score = np.dot(star_weights, posterior_probs)
    return expected_score


# 计算每部电影的平滑得分
df['smooth_score'] = df.apply(bayesian_smoothing_score, axis=1, alpha_prior=alpha_prior)

# 对比原始平均分（未平滑）
df['raw_avg'] = df.apply(
    lambda row: np.dot([1, 2, 3, 4, 5], [row[f'stars{i}'] for i in range(1, 6)]), axis=1
)

print("\n排序结果（按平滑得分降序）：")
print(df[['movie_name', 'movie_comment_num', 'raw_avg', 'smooth_score']].sort_values('smooth_score', ascending=False))
df = df.sort_values('smooth_score', ascending=False)
df.to_csv('machine_learn_rank.csv',index=False,encoding='utf-8')

# ---------- 4. 解释与可视化 ----------
# 观察评论人数很少但平均分很高的电影D（评论人数10，平均分4.1）平滑后得分下降，
# 而评论人数多的电影C（500人，4.43分）平滑后得分保持高位，体现了贝叶斯平滑的收缩效果。