# import re
# import hashlib
# import requests
# from urllib.parse import urljoin
#
#
# def solve_douban_pow(session: requests.Session, url: str) -> requests.Response:
#     # 首次请求：禁止自动重定向，以便捕获挑战页面
#     resp = session.get(url, allow_redirects=False)
#
#     # 判断是否触发PoW挑战（通过表单特征）
#     if 'id="sec"' in resp.text:
#         print(f"检测到 PoW 挑战: {url}")
#         # 提取挑战参数...
#         tok_match = re.search(r'name="tok" value="([^"]+)"', resp.text)
#         cha_match = re.search(r'name="cha" value="([^"]+)"', resp.text)
#         red_match = re.search(r'name="red" value="([^"]+)"', resp.text)
#         if not (tok_match and cha_match and red_match):
#             raise Exception("无法从挑战页面提取必要参数")
#
#         tok = tok_match.group(1)
#         cha = cha_match.group(1)
#         red = red_match.group(1)
#
#         # 计算nonce（难度4）
#         difficulty = 4
#         target_prefix = '0' * difficulty
#         nonce = 0
#         while True:
#             nonce += 1
#             data = cha + str(nonce)
#             hash_hex = hashlib.sha512(data.encode()).hexdigest()
#             if hash_hex.startswith(target_prefix):
#                 break
#
#         # 提交验证（允许自动重定向）
#         post_url = urljoin(resp.url, '/c')
#         post_data = {
#             'tok': tok,
#             'cha': cha,
#             'sol': str(nonce),
#             'red': red
#         }
#         final_resp = session.post(post_url, data=post_data, allow_redirects=True)
#         return final_resp
#
#     # 未触发挑战，但可能遇到重定向
#     if resp.status_code in (301, 302, 303, 307, 308):
#         # 手动跟随重定向（或直接让session自动处理）
#         location = resp.headers.get('Location')
#         if location:
#             redirect_url = urljoin(url, location)
#             return solve_douban_pow(session, redirect_url)  # 递归处理，直到非重定向
#
#     # 正常响应（200）或已处理完毕
#     return resp
#
#
# # 使用示例
# if __name__ == "__main__":
#     s = requests.Session()
#     s.headers.update({
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#     })
#
#     urls = [
#         "https://movie.douban.com/subject/1292052/",
#         "https://movie.douban.com/subject/1291546/",
#         "https://movie.douban.com/subject/1292722/",
#         "https://movie.douban.com/subject/1292720/"
#     ]
#
#     for url in urls:
#         response = solve_douban_pow(s, url)
#         print(f"{url} -> 状态码: {response.status_code}")
#         # 后续可进行数据解析，此处仅演示
#         print(response.text[:300])
from random import random

# import numpy as np
# header = [
#     'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36',
#     'Mozilla/5.0 (Windows 7 Enterprise; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6099.71 Safari/537.36',
#     'Mozilla/5.0 (Windows Server 2012 R2 Standard; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5975.80 Safari/537.36'
# ]
# headers = {
#     'User-Agent':str(np.random.choice(header))
# }
# # print(headers)

# import numpy as np
# import pandas as pd
#
# # ---------- 1. 构造示例数据集 ----------
# # 假设有5部电影，每部包含评论人数和1~5星的占比（或计数）
# data = {
#     'movie_id': ['A', 'B', 'C', 'D', 'E'],
#     'total_votes': [200, 50, 10, 500, 5],
#     'star1_ratio': [0.05, 0.10, 0.00, 0.02, 0.20],
#     'star2_ratio': [0.10, 0.20, 0.10, 0.03, 0.20],
#     'star3_ratio': [0.20, 0.30, 0.20, 0.10, 0.30],
#     'star4_ratio': [0.30, 0.25, 0.30, 0.35, 0.20],
#     'star5_ratio': [0.35, 0.15, 0.40, 0.50, 0.10]
# }
# df = pd.DataFrame(data)
# # print(df.head())
#
# # 将占比转换为计数（实际数据通常直接提供计数）
# for star in range(1, 6):
#     df[f'star{star}_cnt'] = (df[f'star{star}_ratio'] * df['total_votes']).round().astype(int)
#
# print("原始数据（含计数）：")
# print(df[['movie_id', 'total_votes'] + [f'star{i}_cnt' for i in range(1, 6)]])
#
# # ---------- 2. 计算全局先验（狄利克雷分布参数alpha） ----------
# # 将所有电影的各星级计数累加，得到先验分布
# global_counts = df[[f'star{i}_cnt' for i in range(1, 6)]].sum().values
# print(f"各星级计数累加{global_counts}")
# # 狄利克雷先验参数通常取平滑值，这里用全局计数作为先验强度
# alpha_prior = global_counts  # 也可乘以一个强度系数，此处直接使用
#
#
# # ---------- 3. 定义贝叶斯平滑得分函数 ----------
# def bayesian_smoothing_score(row, alpha_prior, star_weights=None):
#     """
#     计算单部电影的贝叶斯平滑后验期望得分。
#     row: 包含各星级计数的行（Series）
#     alpha_prior: 各星级的全局先验参数（长度为5的数组）
#     star_weights: 各星级对应的权重，默认为 [1,2,3,4,5]
#     """
#     if star_weights is None:
#         star_weights = np.array([1, 2, 3, 4, 5])  # 也可自定义，如[0,0,0,1,2]突出高分
#
#     # 各星级计数
#     counts = np.array([row[f'star{i}_cnt'] for i in range(1, 6)])
#     N = counts.sum()
#     print(f"各星级计数{counts}")
#     # for i in counts:
#     #     print(i)
#
#     # 后验狄利克雷参数 = 计数 + 先验参数
#     posterior_alpha = counts + alpha_prior
#     print(f"后验参数{posterior_alpha}")
#     # 后验期望概率 = posterior_alpha / sum(posterior_alpha)
#     posterior_probs = posterior_alpha / posterior_alpha.sum()
#     print(f"后验概率{posterior_probs}")
#     # 期望得分 = 权重向量点乘概率
#     expected_score = np.dot(star_weights, posterior_probs)
#     return expected_score
#
#
# # 计算每部电影的平滑得分
# df['smooth_score'] = df.apply(bayesian_smoothing_score, axis=1, alpha_prior=alpha_prior)
#
# # 对比原始平均分（未平滑）
# df['raw_avg'] = df.apply(
#     lambda row: np.dot([1, 2, 3, 4, 5], [row[f'star{i}_ratio'] for i in range(1, 6)]), axis=1
# )
#
# print("\n排序结果（按平滑得分降序）：")
# print(df[['movie_id', 'total_votes', 'raw_avg', 'smooth_score']].sort_values('smooth_score', ascending=False))
#
# # ---------- 4. 解释与可视化 ----------
# # 观察评论人数很少但平均分很高的电影D（评论人数10，平均分4.1）平滑后得分下降，
# # 而评论人数多的电影C（500人，4.43分）平滑后得分保持高位，体现了贝叶斯平滑的收缩效果。
