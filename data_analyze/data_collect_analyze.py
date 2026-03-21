import hashlib
import re
import time
from urllib.parse import urljoin

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from lxml import etree
from pandas import DataFrame


'''
爬取豆瓣电影top250的名称，链接，剧情类型，制片国家，上映年份，评价人数，每个评价的占比，
通过评价人数和每个评价的占比分析出每个影片所占的排名
'''
header = [
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36',
    'Mozilla/5.0 (Windows 7 Enterprise; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6099.71 Safari/537.36',
    'Mozilla/5.0 (Windows Server 2012 R2 Standard; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5975.80 Safari/537.36'
]
headers = {
    'User-Agent':str(np.random.choice(header))
}
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
cookies = {
    'Cookie':'ll="118239"; bid=oWg8Gp19APA; _pk_id.100001.4cf6=c32e5eb38bb513df.1758809853.; _vwo_uuid_v2=D345AB71E1F9275B0EE713C8BAFB64CF1|72a87c1f6f2aa91a382fb3d8393938ea; __yadk_uid=2vXFGRhZ2BOeadbr1Y0sckTYieRefNOQ; _ga=GA1.1.1167380508.1758869774; _ga_Y4GN1R87RG=GS2.1.s1758869774$o1$g1$t1758869846$j60$l0$h0; _ga_RXNMP372GL=GS2.1.s1762161773$o1$g0$t1762161774$j59$l0$h0; viewed="35044046_26980487"; __utmz=30149280.1773831047.13.6.utmcsr=sec.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1773831047.12.5.utmcsr=sec.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1773910151%2C%22https%3A%2F%2Fsec.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; __utma=30149280.1385649044.1758809853.1773885593.1773910151.15; __utmb=30149280.0.10.1773910151; __utmc=30149280; __utma=223695111.1100757957.1758809853.1773885593.1773910151.14; __utmb=223695111.0.10.1773910151; __utmc=223695111'
}
# url = 'https://movie.douban.com/top250?start=0&filter=' page = (num-1)*25
base_url = 'https://movie.douban.com/'

def request_parse_page(page_num:int)->list:
    '''
    爬取指定网页的数据内容
    :param page_num:爬取的页面数量
    :return: 数据列表
    '''

    total_movie_list = []
    for m in range(1,page_num+1):
        page = (m - 1) * 25
        url = base_url + 'top250?start=%d&filter=' % page
        print(f"正在爬取第{m}页")
        response = requests.get(url, headers=headers, timeout=10)
        page_content = response.content.decode('utf-8')

        # html = etree.HTML(page_content)
        #
        # # 解析页面内容
        # # xpath
        # movie_name = html.xpath('//div[@class="hd"]/a/span[1]/text()')
        # print(movie_name)
        # movie_href = html.xpath('//div[@class="hd"]/a/@href')
        # print(movie_href)
        # movie_complex = html.xpath('//div[@class="bd"]/p[1]/text()[2]')
        # print(movie_complex)
        # movie_comment_num = html.xpath('//div[@class="bd"]/div/span[4]/text()')
        # print(movie_comment_num)
        # for j in range(len(movie_name)):
        #     total_movie_list.append([
        #         movie_name[j].strip(),
        #         movie_href[j].strip(),
        #         movie_complex[j].strip(),
        #         movie_comment_num[j].strip()
        #     ])

        # css
        soup = BeautifulSoup(page_content, 'lxml')
        movie_item = soup.select('div.item')
        for i in movie_item:
            # 爬取电影名和链接
            name_href_ele = i.select('.pic')
            name_href_list = []
            for j in name_href_ele:
                movie_name = j.find('img')['alt'].strip()
                movie_href = j.find('a')['href'].strip()
                name_href_list.append(movie_name)
                name_href_list.append(movie_href)
                # print(name_href_list)
            # 爬取电影剧情，国家，年份，评论人数
            complex_ele = i.select('.bd')
            complex_comment_list = []
            for j in complex_ele:
                movie_complex = j.find('p').get_text().strip().replace('\n','<br>').split(r'<br>')[1].strip()
                movie_comment_score = j.find_all('span')[3].get_text().strip()
                complex_comment_list.append(movie_complex)
                complex_comment_list.append(movie_comment_score)
                # print(complex_comment_list)

            # 合并添加
            name_href_list.extend(complex_comment_list)
            total_movie_list.append(name_href_list)

        # print(total_movie_list)
        print(f"爬取第{m}页成功")
        time.sleep(2)

    return total_movie_list


def solve_douban_pow(session: requests.Session, url: str) -> requests.Response:
    """
    处理豆瓣 PoW 反爬挑战，返回最终页面的 Response 对象。
    :param session: 携带 Cookie 的 requests.Session
    :param url: 最初请求的目标 URL（触发挑战的地址）
    :return: 成功通过挑战后的响应对象
    """

    # 首次请求：禁止自动重定向，以便捕获挑战页面
    resp = session.get(url, allow_redirects=True)

    # 判断是否触发PoW挑战（通过表单特征）
    if 'id="sec"' in resp.text:
        print(f"检测到 PoW 挑战: {url}")
        # 提取挑战参数...
        tok_match = re.search(r'name="tok" value="([^"]+)"', resp.text)
        cha_match = re.search(r'name="cha" value="([^"]+)"', resp.text)
        red_match = re.search(r'name="red" value="([^"]+)"', resp.text)
        if not (tok_match and cha_match and red_match):
            raise Exception("无法从挑战页面提取必要参数")

        tok = tok_match.group(1)
        cha = cha_match.group(1)
        red = red_match.group(1)

        # 计算nonce（难度4）
        difficulty = 4
        target_prefix = '0' * difficulty
        nonce = 0
        while True:
            nonce += 1
            data = cha + str(nonce)
            hash_hex = hashlib.sha512(data.encode()).hexdigest()
            if hash_hex.startswith(target_prefix):
                break

        # 提交验证（允许自动重定向）
        post_url = urljoin(resp.url, '/c')
        post_data = {
            'tok': tok,
            'cha': cha,
            'sol': str(nonce),
            'red': red
        }
        final_resp = session.post(post_url, data=post_data, allow_redirects=True)

        return final_resp


    # 未触发挑战，但可能遇到重定向
    if resp.status_code in (301, 302):
        # 手动跟随重定向（或直接让session自动处理）
        location = resp.headers.get('Location')
        if location:
            redirect_url = urljoin(url, location)
            return solve_douban_pow(session, redirect_url)  # 递归处理，直到非重定向

    # 正常响应（200）或已处理完毕
    return resp


def movie_comment_score(df:DataFrame)->DataFrame:
    '''
    通过上个先前爬取的页面数据进行再爬取
    :param df: dataframe
    :return:dataframe
    '''

    total_movie_star = []
    session = requests.Session()
    # 自定义请求header
    session.headers.update(headers)
    for i in df['movie_href']:
        # print(i)
        # 处理豆瓣反爬机制
        response = solve_douban_pow(session,i)
        # 请求状态码
        print(f"请求状态码为：{response.status_code}")
        page_content = response.content.decode('utf-8')
        html = etree.HTML(page_content)
        stars = html.xpath('//div[@class="ratings-on-weight"]/div[@class="item"]/span[2]/text()')
        # print(stars)
        hand_stars = []
        for j in stars:
            hand_stars.append(
                float(j.split('%')[0]) / 100
                )
        print(hand_stars)
        total_movie_star.append(
            np.concatenate(([i],hand_stars))
        )
        # print(total_movie_star)
        time.sleep(3)

    df = pd.DataFrame(total_movie_star,columns=['movie_href','stars5','stars4','stars3','stars2','stars1'])

    return df


def hand_page_data(df:DataFrame)->DataFrame:
    '''
    对爬取的页面数据进行整理分类，方便后续分析
    :param df:dataframe
    :return: 整理的dataframe
    '''

    #对年份，国家，剧情类型，评论人数分别进行处理
    movie_year_list = []
    movie_country_list = []
    movie_type_list = []
    movie_comment_num_list = []
    for i in df['movie_complex']:
        data = i.replace('\xa0','').split('/')

        #对特殊的年份列进行处理
        if len(data[0]) > 4:
            movie_year_list.append(data[0].split('(')[0])
        else:
            movie_year_list.append(data[0])

        #对特殊长度的数据进行处理
        if len(data) > 3:
            movie_country_list.append(data[-2])
            movie_type = data[-1].replace('剧情','').strip()
            if movie_type != '':
                movie_type_list.append(movie_type)
            else:
                movie_type_list.append(np.nan)
        else:
            movie_country_list.append(data[1])
            movie_type = data[2].replace('剧情','').strip()
            if movie_type != '':
                movie_type_list.append(movie_type)
            else:
                movie_type_list.append(np.nan)
    for i in df['movie_comment_num']:
        data = i.split('人')
        movie_comment_num_list.append(data[0])

    #删除原来的复杂列
    del df['movie_complex']
    #添加新生成的列
    df['movie_comment_num'] = movie_comment_num_list
    df['movie_year'] = movie_year_list
    df['movie_country'] = movie_country_list
    df['movie_type'] = movie_type_list

    return df

def check_hand_null(df:DataFrame)->DataFrame:
    '''
    检查处理数据列表的空值
    :param df:dataframe
    :return: 非空的dataframe
    '''

    df_null = df.isna().sum()
    print(f"数据缺失值情况:\n{df_null}")
    #名称列直接删除
    df.dropna(subset=['movie_name'])
    #链接列改为无资源
    df['movie_href'].fillna('无资源链接',inplace=True)
    #对年份,国家，剧情类型改为未知
    df['movie_year'].fillna('未知',inplace=True)
    df['movie_country'].fillna('未知',inplace=True)
    df['movie_type'].fillna('未知',inplace=True)

    print(f"处理缺失值后数据情况:\n{df.isnull().sum()}")

    return df

def check_hand_unique(df:DataFrame)->DataFrame:
    '''
    检查处理数据列表的重复值
    :param df:dataframe
    :return: 去重的dataframe
    '''

    df_duplicate = df.duplicated().sum()
    print(f"数据重复值情况:\n{df_duplicate}")
    if df_duplicate != 0:
        df.drop_duplicates(inplace=True,keep=False)

    print(f"去重后数据情况：\n{df.duplicated().sum()}")

    return df


def movie_country_rate(df:DataFrame)->DataFrame:
    '''
    分析每个电影出处的国家占比
    :param df:dataframe
    :return: 每个国家生产的所占比例
    '''

    country_type = [
        '中国大陆','中国香港','中国台湾','美国','英国','法国','日本',
        '韩国',
        '德国',
        '意大利',
        '西班牙',
        '印度',
        '泰国',
        '俄罗斯',
        '加拿大',
        '澳大利亚',
        '爱尔兰',
        '瑞典',
        '巴西',
        '丹麦'
    ]
    country_dict = {
    '中国大陆':0,
    '中国香港':0,
    '中国台湾':0,
    '美国':0,
    '英国':0,
    '法国':0,
    '日本':0,
    '韩国':0,
    '德国':0,
    '意大利':0,
    '西班牙':0,
    '印度':0,
    '泰国':0,
    '俄罗斯':0,
    '加拿大':0,
    '澳大利亚':0,
    '爱尔兰':0,
    '瑞典':0,
    '巴西':0,
    '丹麦':0
    }

    #计算每个电影国家占比数量
    for i in df['movie_country']:
        country_list = i.split(' ')
        for j in country_type:
            if j in country_list:
                country_dict[j] += 1

    #计算每个国家电影占比比率
    total_num = 0
    for i in country_dict.values():
        total_num += i
    country_rate = []
    country_rate.append(
        [country_dict[i] / total_num for i in country_dict.keys()]
    )
    df = pd.DataFrame(country_rate,columns=country_type)

    return df


def movie_type_rate(df:DataFrame)->DataFrame:
    '''
    分析每个电影剧情类型的占比
    :param df:dataframe
    :return: 每个剧情类型的电影占比
    '''

    movie_type = [
        '喜剧',
        '爱情',
        '动作',
        '科幻',
        '动画',
        '悬疑',
        '犯罪',
        '惊悚',
        '冒险',
        '音乐',
        '历史',
        '奇幻',
        '恐怖',
        '战争',
        '传记',
        '歌舞',
        '武侠',
        '情色',
        '灾难',
        '西部',
        '纪录片',
        '短片',
        '未知'
    ]
    movie_type_dict = {
        '喜剧':0,
        '爱情':0,
        '动作':0,
        '科幻':0,
        '动画':0,
        '悬疑':0,
        '犯罪':0,
        '惊悚':0,
        '冒险':0,
        '音乐':0,
        '历史':0,
        '奇幻':0,
        '恐怖':0,
        '战争':0,
        '传记':0,
        '歌舞':0,
        '武侠':0,
        '情色':0,
        '灾难':0,
        '西部':0,
        '纪录片':0,
        '短片':0,
        '未知':0
    }
    # print(len(movie_type_dict))
    # print(len(movie_type))

    #对每个电影类型计数
    for i in df['movie_type']:
        single_movie_type = i.split(' ')
        for j in movie_type:
            if j in single_movie_type:
                movie_type_dict[j] += 1

    #每个电影类型占比
    total_num = 0
    for i in movie_type_dict.values():
        total_num += i
    movie_type_rate = []
    movie_type_rate.append(
        [movie_type_dict[i] / total_num for i in movie_type]
    )
    df = pd.DataFrame(movie_type_rate,columns=movie_type)
    return df
    # 喜剧
    # 爱情
    # 动作
    # 科幻
    # 动画
    # 悬疑
    # 犯罪
    # 惊悚
    # 冒险
    # 音乐
    # 历史
    # 奇幻
    # 恐怖
    # 战争
    # 传记
    # 歌舞
    # 武侠
    # 情色
    # 灾难
    # 西部
    # 纪录片
    # 短片
def movie_date_rate(df:DataFrame)->DataFrame:
    '''
    分析每个年份的电影占比
    :param df: dataframe
    :return: 每个年份的电影占比
    '''
    # 2020
    # 年代
    # 2026
    # 2025
    # 2024
    # 2023
    # 2022
    # 2021
    # 2020
    # 2019
    # 2010
    # 年代
    # 2000
    # 年代
    # 90
    # 年代
    # 80
    # 年代
    # 70
    # 年代
    # 60
    # 年代
    # 更早
    # 定义区间
    date = [
        0,1960,1970,1980,1990,2000,2026
    ]
    label = [
        '更早','六十年代','七十年代','八十年代','九十年代','20世纪'
    ]
    year_date = []
    for i in df['movie_year']:
        year = time.strptime(i.split('(')[0],"%Y").tm_year
        #print(year)
        year_date.append(year)
    df = pd.cut(year_date,bins=date,labels=label).value_counts().reset_index()
    total_count = 0
    for i in df['count']:
        total_count += i
    movie_date_rate = []
    movie_date_rate.append(
        [i / total_count for i in df['count']]
    )
    df = pd.DataFrame(movie_date_rate,columns=label)

    return df

def main():
    # data_list = request_parse_page(10)
    # df = pd.DataFrame(data_list,columns=['movie_name','movie_href','movie_complex','movie_comment_num'])
    # df.to_csv('movie_data.csv',index=False,encoding='utf-8')
    data = pd.read_csv('movie_data.csv')
    print(data.head())
    # 数据清洗，去除重复值和空值
    hand_data = hand_page_data(data)
    check_hand_null(hand_data)
    check_hand_unique(hand_data)
    print(hand_data.head())
    # hand_data.to_csv('hand_movie_data.csv',index=False,encoding='utf-8')
    # movie_country_rate_data = movie_country_rate(hand_data).round(3)
    # # 统计分析
    # movie_country_rate_data.to_csv('movie_country_rate.csv',index=False,encoding='utf-8')
    # movie_type_rate_data = movie_type_rate(hand_data).round(3)
    # movie_type_rate_data.to_csv('movie_type_rate.csv',index=False,encoding='utf-8')
    # movie_date_rate_data = movie_date_rate(hand_data).round(3)
    # movie_date_rate_data.to_csv('movie_date_rate.csv',index=False,encoding='utf-8')
    # 将处理后的数据与星级占比表合成新表
    movie_stars = pd.read_csv('movie_stars.csv')
    # 处理占比数值（一个思路，已在爬取函数更改）
    # for i in range(1,6):
    #     movie_stars_rate_list = []
    #     for j in movie_stars[f'stars{i}']:
    #         print(type(j))
    #         print(j)
    #         movie_stars_rate = float(j.split('%')[0]) / 100
    #         movie_stars_rate_list.append(movie_stars_rate)
    #     movie_stars[f'stars{i}'] = movie_stars_rate_list

    new_movie_data = hand_data.merge(movie_stars,on='movie_href',how='left')
    print(new_movie_data.head())
    new_movie_data.to_csv('new_movie_data.csv',index=False,encoding='utf-8')



if __name__ == '__main__':
    main()
    # 爬取各星级占比
    # data = pd.read_csv('movie_data.csv')
    # movie_stars = movie_comment_score(data)
    # movie_name_comment_stars = movie_stars.merge(data)
    # movie_stars.to_csv('movie_stars.csv',index=False,encoding='utf-8')

    # # 反爬机制页面
    # for i in data['movie_href']:
    #     res = requests.get(i,headers=headers,timeout=10,cookies=cookies)
    #     print(res.text)
    #     break
    pass
