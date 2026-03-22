import pandas as pd
import pymysql
from pymysql import Connection


def connect_mysql()->Connection:

    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1913',
        db='company',
        charset='utf8'
    )
    return conn

def create_table(sql):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql)
    count = cursor.rowcount
    if count == 0:
        print('创建表成功')
    else:
        raise Exception('表已存在或检查语法错误')

def desc_table(sql:str):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql)
    count = cursor.rowcount
    if count != 0:
        print(f"表的结构为：")
        for row in cursor.fetchall():
            print(row)
    else:
        raise Exception('表不存在')

def select_table(sql:str):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql)
    count = cursor.rowcount
    if count != 0:
        print(f"成功查询到{count}张数据表")
        for row in cursor.fetchall():
            print(row)
    else:
        raise Exception('不存在表或检查语法错误')

def data_select_mysql(sql:str,*args,**kwargs)->int:
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql % args)
    count = cursor.rowcount
    if count != 0:
        print(f"查询出{count}条数据")
        for row in cursor.fetchall():
            print(row)
    else:
        raise Exception('没有数据或检查语法错误')
    return count

def data_insert_mysql(sql:str,*args,**kwargs)->int:
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql % args)
    conn.commit()
    count = cursor.rowcount
    if count == 0:
        raise Exception('数据已存在或检查语法错误')
    else:
        print(f"成功插入{count}条数据")
        for i in cursor.fetchall():
            print(i)
    cursor.close()

    return count

def data_update_mysql(sql:str,*args,**kwargs)->int:
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql % args)
    conn.commit()
    count = cursor.rowcount
    if count != 0:
        print(f"成功更新{count}条数据")
        for i in cursor.fetchall():
            print(i)
    else:
        raise Exception('数据不存在或检查语法错误')
    cursor.close()

    return count

def data_delete_mysql(sql:str,*args,**kwargs)->int:
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql % args)
    conn.commit()
    count = cursor.rowcount
    if count != 0:
        print(f"成功删除{count}条数据")
        for i in cursor.fetchall():
            print(i)
    else:
        raise Exception('数据不存在或检查语法错误')
    cursor.close()

    return count

def alter_table(sql:str,*args,**kwargs)->int:
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql % args)
    count = cursor.rowcount
    # print(count)
    if count == 0:
        print('修改表结构成功')
    else:
        raise Exception('检查语法错误')

    return count

def main():
    select_table_sql = 'show tables'
    select_table(select_table_sql)

    create_table_sql = '''
    create table if not exists movie(
    movie_name varchar(20) primary key not null,
    movie_href varchar(50) unique not null,
    movie_comment_num int(9),
    movie_year year,
    movie_country varchar(20),
    movie_type varchar(20))'''
    create_table(create_table_sql)

    desc_table_sql = 'desc movie'
    desc_table(desc_table_sql)

    # alter_table_sql = "alter table movie modify movie_country varchar(30)"
    # alter_table(alter_table_sql)

    # delete_sql = 'delete from movie'
    # data_delete_mysql(delete_sql)

    df = pd.read_csv('hand_movie_data.csv')
    # print(data.head())
    for i in range(len(df)):
        movie_name_list = df['movie_name'].tolist()
        movie_href_list = df['movie_href'].tolist()
        movie_comment_num_list = df['movie_comment_num'].tolist()
        movie_year_list = df['movie_year'].tolist()
        movie_country_list = df['movie_country'].tolist()
        movie_type = df['movie_type'].tolist()
        insert_sql = '''
        insert into movie(
        movie_name,
        movie_href,
        movie_comment_num,
        movie_year,
        movie_country,
        movie_type) values ('%s','%s','%d','%s','%s','%s')'''

        data = (
            movie_name_list[i], movie_href_list[i],
            movie_comment_num_list[i], movie_year_list[i],
            movie_country_list[i],movie_type[i]
        )
        # data_insert_mysql(insert_sql, *data)

    select_table_sql = "select *from movie limit 25"
    data_select_mysql(select_table_sql)

    update_sql = "update movie set movie_country='%s',movie_type='%s' where movie_name='%s'"
    # data_update_mysql(update_sql,*('英国','科幻','2001太空漫游'))
    # select_update_sql = "select * from movie where movie_name='%s'"
    # data_select_mysql(select_update_sql,'2001太空漫游')

    # delete_sql = "delete from movie where movie_name='%s'"
    # data_delete_mysql(delete_sql,'2001太空漫游')

    delete_all_sql = 'delete from movie'
    data_delete_mysql(delete_all_sql)

    pass

if __name__ == '__main__':
    main()