import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
def movie_date_rate():
    '''
    绘制电影年份占比饼图与散点图
    :return:
    '''

    movie_date_rate = pd.read_csv('movie_date_rate.csv')
    # print(movie_date_rate.head())
    label = movie_date_rate.columns.tolist()
    data = movie_date_rate.values[0]
    # print(label)
    # print(data)
    fig, ax = plt.subplots(1,2,figsize=(10,6))
    ax[0].pie(data,
              labels=label,
              autopct='%1.1f%%',
              pctdistance=0.7,
              startangle=90,
              shadow=True,
              explode=[0.05 if i > 0.1 else 0 for i in data])
    ax[0].set_title('电影年份占比饼图',loc = 'center')
    ax[0].legend(loc='upper right',fancybox=True,shadow=True,fontsize='small')

    for date,rate in movie_date_rate.items():
        # print(date)
        # print(rate)
        ax[1].scatter(date,rate[0],
                      s=rate[0]*2000,
                      label=date,
                      )
        # 添加注释文本
        plt.text(date,rate[0] + 0.01,'{:.1%}'.format(rate[0]),ha='center',va='bottom')
    ax[1].set_title('电影年份占比散点图',loc = 'center')
    ax[1].set_xlabel('电影年份')
    ax[1].set_ylabel('占比率（%）')
    ax[1].legend(loc='upper left',
                 fancybox=True,
                 shadow=True,
                 fontsize='small',
                 bbox_to_anchor=(1,1))
    ax[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def movie_country_rate():
    '''
    绘制电影国家占比散点图与柱形图
    :return:
    '''

    movie_country_rate = pd.read_csv('movie_country_rate.csv')
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    label = movie_country_rate.columns.tolist()
    # 列索引和所有列值,iterrows行索引和所有行值
    for country,rows in movie_country_rate.items():
        ax.scatter(country,rows[0],
                   s=rows[0]*2000,
                   label=country)
        ax.text(country,rows[0] + 0.01,'{:.1%}'.format(rows[0]),ha='center',va='bottom')
    ax.set_title('豆瓣电影产地占比散点图',loc='center')
    ax.set_xlabel('电影产地')
    ax.set_xticks(np.array(range(len(label))))
    ax.set_xticklabels(label,rotation=60,)
    ax.set_ylabel('占比率（%）')
    ax.legend(bbox_to_anchor=(1.1, 1), loc='upper right',fancybox=True,shadow=True,)
    plt.tight_layout()
    plt.show()

def movie_type_rate():
    '''
    绘制电影类型占比散点图与柱形图
    :return:
    '''
    movie_type_rate = pd.read_csv('movie_type_rate.csv')
    label = movie_type_rate.columns.tolist()
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    for type,rate in movie_type_rate.items():#列索引和所有列值,iterrows行索引和所有行值
        ax.bar(type,rate[0],
               width= 0.8,
               label=type)
        ax.text(type,rate[0] + 0.001,'{:.1%}'.format(rate[0]),ha='center',va='bottom')
    ax.set_title('豆瓣电影类型柱形图',loc='center')
    ax.set_xlabel('电影类型')
    ax.set_ylabel('占比率（%）')
    ax.set_xticks(np.array(range(len(label))))
    ax.set_xticklabels(label,rotation=60,)
    plt.legend(loc='upper right',fancybox=True,shadow=True,bbox_to_anchor=(1.1,1))
    plt.tight_layout()
    plt.show()

def main():
    movie_date_rate()
    movie_country_rate()
    movie_type_rate()

if __name__ == '__main__':
    main()
    pass