
import pymysql
from pymysql import Connection


def connect_mysql()->Connection:

    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
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
        raise Exception

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
        raise Exception

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
        raise Exception('查询失败')

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
        raise Exception('查询出错')

    return count

def data_insert_mysql(sql:str,*args,**kwargs)->int:
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(sql % args)
    conn.commit()
    count = cursor.rowcount
    if count == 0:
        raise Exception('插入失败')
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
        raise Exception('更新失败')
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
        raise Exception('删除失败')
    cursor.close()

    return count

def main():
    pass
