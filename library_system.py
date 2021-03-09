# coding:utf-8
import pymysql
import os
import datetime


def create_books():
    os.system('cls')
    db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
    cursor = db.cursor()
    book_num = int(input('您要存入多少种书籍：'))
    a = 0
    while a < book_num:
        book_name1 = input('请输入书籍的名字:')
        book_press1 = input('请输入书籍的出版社:')
        book_writer1 = input('请输入书籍的作者:')
        book_date1 = input('请输入书籍的出版日期:')
        book_isbn1 = input('请输入书籍的ISBN号码:')
        book_shuliang1 = input('请输入存入该种书籍的数量:')
        sql = "insert into books(book_name,book_press,book_writer,book_date,book_isbn,book_shuliang)\
        values('%s','%s','%s','%s','%s','%s')" % (str(book_name1), str(book_press1), str(book_writer1), str(book_date1),\
                                                 str(book_isbn1), str(book_shuliang1))
        cursor.execute(sql)
        print('添加书籍成功！')
        a = a + 1
    db.commit()
    cursor.close()


def search_books():
    """查询书籍函数"""
    db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
    cursor = db.cursor()
    flag = 1
    while flag == 1:
        choose1 = int(input("请选择你要用什么方式查找书籍：\n1.ISBN序列号\n2.书名\n3.出版社\n4.作者\n5.出版日期\n6.类型\n"))
        if choose1 == 1:
            isbn = input("请输入该书籍的ISBN序列号：\n")
            res3 = cursor.execute("select book_name,book_shuliang from books where book_isbn = '%s'" % isbn)  # 返回值是0或1
            if res3:
                data = cursor.fetchone()
                print("书籍:'%s'" % str(data[0]))
                print("该书还剩余：%d 本" % int(data[1]))
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
            else:
                print("图书馆暂无此书籍！")
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
        elif choose1 == 2:
            name = str(input("请输入你要查询的书籍的名称："))
            res = cursor.execute("select book_isbn,book_shuliang from books where book_name = '%s'" % name)
            if res:
                data = cursor.fetchone()
                print("该书籍的ISBN编码：'%s' " % str(data[0]))
                print("该书还剩余：%d 本" % int(data[1]))
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
            else:
                print("图书馆暂无此书籍！")
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
        elif choose1 == 3:
            name_press = str(input("请输入出版社名称："))
            res = cursor.execute("select * from books where book_press = '%s'" % name_press)
            if res:
                data = cursor.fetchall()
                print(data, end='\n')
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
            else:
                print("图书馆暂无此出版社的书籍！")
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
        elif choose1 == 4:
            name_writer = str(input("请输入作者名字："))
            res3 = cursor.execute("select * from books where book_writer = '%s'" % name_writer)
            if res3:
                data = cursor.fetchall()
                print(data, end='\n')
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
            else:
                print("图书馆暂无此作者的书籍！")
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
        elif choose1 == 5:
            date = str(input("请输入出版日期："))
            res4 = cursor.execute("select * from books where book_date = '%s'" % date)
            if res4:
                data = cursor.fetchall()
                print(data, end='\n')
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))
            else:
                print("图书馆暂无此书籍！")
                flag = int(input("是否要继续查询？\n1.是\n2.否\n"))


def borrow_books(user_name, user_id):
    """借书函数"""
    db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
    cursor = db.cursor()
    if '校内人员' in user_id:  # 校内人员借阅
        cursor.execute("select user_res from user where user_name = '%s'" % user_name)
        data = cursor.fetchone()
        restrict = data[0]
        comp = int(restrict)
        print("您最多同时借阅4本书籍,当前已经借阅：'%s' 本" % restrict)
        if 0 <= comp < 4:
            isbn = str(input("请输入该书籍的ISBN序列号：\n"))
            cursor.execute("select book_name from books where book_isbn = '%s'" % str(isbn))
            book_name = cursor.fetchone()
            res3 = cursor.execute("select book_name,book_shuliang from books where book_isbn = '%s'" % str(isbn))  # 返回值是0或1
            if res3:
                cursor.execute("select book_shuliang from books where book_isbn = '%s'" % str(isbn))
                data = cursor.fetchone()
                print("您要借阅的书籍是：《%s》\n现在该书籍还剩余：%d 本\n" % (book_name[0], int(data[0])))
                choose2 = int(input("您一次只能借阅一本，是否继续？\n1.继续\n2.退出\n"))
                if choose2 == 1:
                    new_num = int(int(data[0]) - 1)
                    cursor.execute("update books set book_shuliang = %d where book_isbn = '%s'" % (new_num, str(isbn)))
                    db.commit()
                    cursor.execute("select user_book_name from user where user_name = '%s'" % user_name)
                    old_books = cursor.fetchone()
                    old_books_str = ''.join(old_books)
                    new_book_str = old_books_str + ' '+ book_name[0]
                    cursor.execute("update user set user_book_name = '%s' where user_name = '%s'" % \
                                       (new_book_str, user_name))
                    db.commit()
                    cursor.execute("update user set user_res = '%s' where user_name = '%s'" \
                                   % (str(comp + 1), user_name))
                    db.commit()
                    cursor.close()
                    print("借书成功，记得及时归还哦！")
                elif choose2 == 2:
                    return False
            else:
                print("请查正书籍的ISBN编号！")
        else:
            print("每个人最多同时持有4本书，请先归还图书！")
    else:  # 校外人员借阅
        cursor.execute("select user_res from user where user_name = '%s'" % user_name)
        data = cursor.fetchone()
        restrict = data[0]
        comp = int(restrict)
        print("您最多同时借阅2本书籍,当前已经借阅：'%s' 本" % restrict)
        if comp == 1:
            isbn = str(input("请输入该书籍的ISBN序列号：\n"))
            cursor.execute("select book_name from books where book_isbn = '%s'" % str(isbn))
            book_name = cursor.fetchone()
            res3 = cursor.execute(
                "select book_name,book_shuliang from books where book_isbn = '%s'" % str(isbn))  # 返回值是0或1
            if res3:
                cursor.execute("select book_shuliang from books where book_isbn = '%s'" % str(isbn))
                data = cursor.fetchone()
                print("您要借阅的书籍是：《%s》\n现在该书籍还剩余：%d 本\n" % (book_name[0], int(data[0])))
                choose2 = int(input("您一次只能借阅一本，是否继续？\n1.继续\n2.退出\n"))
                if choose2 == 1:
                    new_num = int(int(data[0]) - 1)
                    cursor.execute("update books set book_shuliang = %d where book_isbn = '%s'" % (new_num, str(isbn)))
                    db.commit()
                    cursor.execute("select user_book_name from user where user_name = '%s'" % user_name)
                    old_books = cursor.fetchone()
                    old_books_str = ''.join(old_books)
                    new_book_str = old_books_str + ' ' + book_name[0]
                    cursor.execute("update user set user_book_name = '%s' where user_name = '%s'" % \
                                   (new_book_str, user_name))
                    db.commit()
                    cursor.execute("update user set user_res = '%s' where user_name = '%s'" \
                                   % (str(comp + 1), user_name))
                    db.commit()
                    cursor.close()
                    print("借书成功，记得及时归还哦！")
                elif choose2 == 2:
                    return False
            else:
                print("请查正书籍的ISBN编号！")
        else:
            print("校外人员最多持有2本书，请先归还图书再借阅读！")


def back_books(user_name):  # user_name是字符串类型
    """还书函数"""
    db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
    cursor = db.cursor()
    book_name = input("请写出你要归还的书的名字:\n")
    cursor.execute("select user_book_name from user where user_name = '%s'" % user_name)
    data = cursor.fetchone()
    data_str = ''.join(data)
    result = book_name in data_str
    if result:
        new_str = data_str.replace('%s' % book_name, ' ')
        print("当前拥有的的书籍是：" + new_str)
        cursor.execute("update user set user_book_name = '%s' where user_name = '%s'" % \
                      (new_str, user_name))
        db.commit()
        cursor.execute("select book_shuliang from books where book_name = '%s'" % book_name)
        data2 = cursor.fetchone()
        now_num = int(data2[0])
        new_num = str(now_num + 1)
        print("当前用户：" + user_name)
        print(new_num)
        cursor.execute("update books set book_shuliang = '%s' where book_name = '%s'" % (new_num, book_name))
        db.commit()
        cursor.execute("select user_res from user where user_name = '%s'" % user_name)
        data = cursor.fetchone()
        new_res = str(int(''.join(data)) - 1)
        cursor.execute("update user set user_res = '%s' where user_name = '%s'" % (new_res, user_name))
        db.commit()
        print("还书成功！")
        cursor.close()
    else:
        print("您并未借阅此书籍！\n")


def login():
    """创建新的用户，把他们的数据写入user表中"""
    identity = int(input("请选择您的身份：\n1.在校人员或老师\n2.社会人员\n"))
    if identity == 1:  # 用户是在校人员或老师
        user_name1 = str(input("请输入新建用户的名称："))
        psw1 = str(input("请设置6位数纯数字密码："))
        id_card = " 校内人员"
        db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
        cursor = db.cursor()
        sql = "insert into user(user_name,user_psw,user_id)values('%s','%s','%s')" %\
              (str(user_name1), str(psw1), str(id_card))
        cursor.execute(sql)
        print('创建用户成功！')
        db.commit()
        cursor.close()
        return True
    elif identity == 2:  # 用户是社会人员
        user_name1 = str(input("请输入新建用户的名称："))
        psw1 = str(input("请设置6位数纯数字密码："))
        id_card = str(input("请输入您的身份证号："))
        db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
        cursor = db.cursor()
        sql = "insert into user(user_name,user_psw,user_id)values('%s','%s','%s')" % \
              (str(user_name1), str(psw1), str(id_card))
        cursor.execute(sql)
        print('创建社会用户成功！')
        db.commit()
        cursor.close()
        return True
    else:
        print("您输入的信息有误！")
        return False


def is_manager():
    user_name1 = input("请输入您的管理员用户名：")
    user_psw1 = input("请输入您的密码：")
    db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
    cursor = db.cursor()
    r = cursor.execute("select user_name from user where user_name = '%s'" % user_name1)
    if r == 1:
        cursor.execute("select user_name,user_psw,user_id from user where user_name = '%s'" % user_name1)
        res = cursor.fetchone()
        if str(res[1]) == str(user_psw1):
            print("登陆成功！\n欢迎您！")
            return True
        else:
            print("错误的密码！")
    else:
        print("错误的用户名！")
        return False
    pass


def signup():
    """已有用户登录，提供用户名和密码，可以展示当前正在借阅的书籍和欠款"""
    user_name1 = input("请输入您的用户名：")
    user_psw1 = input("请输入您的密码：")
    db = pymysql.connect("localhost", "root", "991015", "TESTDB", charset='utf8')
    cursor = db.cursor()
    r = cursor.execute("select user_name from user where user_name = '%s'" % user_name1)
    if r == 1:
        cursor.execute("select user_name,user_psw,user_id from user where user_name = '%s'" % user_name1)
        res_signup = cursor.fetchone()
        if str(res_signup[1]) == str(user_psw1):
            print("登陆成功！\n欢迎您！")
            cursor.execute("select user_id from user where user_name = '%s'" % user_name1)
            res2 = cursor.fetchone()
            user_id1 = res2[0]  # 字符串类型id
            print("您当前正在借阅的书籍有：")
            cursor.execute("select user_book_name from user where user_name = '%s'" % user_name1)
            user_books = cursor.fetchall()
            print(user_books)
            return True, str(user_name1), str(user_psw1), str(user_id1)
        else:
            print("错误的密码！")
    else:
        print("错误的用户名！")
        return False

#
# def find_debt():
#     pass


if __name__ == '__main__':
    print("\t\t\t\t\t您好！欢迎使用图书管理系统！\
    \n\t\t\t\t\t请选择您的功能：\n\t\t\t\t\t1.用户登录\n\t\t\t\t\t2.用户注册\n\t\t\t\t\t3.图书管理")
    choose = int(input())
    if choose == 1:
        res = signup()
        if res:
            flag = 1
            while flag == 1:
                user_choose = int(input("请选择您要进行的操作：\n1.借书\n2.还书\n3.查看欠款\n4.查询书籍\n"))
                if user_choose == 1:
                    borrow_books(res[1], res[3])
                    flag = int(input("请问您是否要继续操作？\n1.是\n2.否\n"))
                elif user_choose == 2:
                    back_books(res[1])
                    flag = int(input("请问您是否要继续操作？\n1.是\n2.否\n"))
                    pass
                elif user_choose == 3:
                    pass
                elif user_choose == 4:
                    search_books()
                    flag = int(input("请问您是否要继续操作？\n1.是\n2.否\n"))
        else:
            print("请重启管理系统并再次登陆！")
    elif choose == 2:
        login()
        choose = int(input("是否前往登陆？\n1.是\n2.否\n"))
        if choose == 1:
            res = signup()
            if res:
                flag = 1
                while flag == 1:
                    user_choose = int(input("请选择您要进行的操作：\n1.借书\n2.还书\n3.查看欠款\n4.查询书籍\n"))
                    if user_choose == 1:
                        borrow_books(res[1], res[3])
                        flag = int(input("请问您是否要继续操作？\n1.是\n2.否\n"))
                    elif user_choose == 2:
                        back_books(res[1])
                        flag = int(input("请问您是否要继续操作？\n1.是\n2.否\n"))
                        pass
                    elif user_choose == 3:
                        pass
                    elif user_choose == 4:
                        search_books()
                        flag = int(input("请问您是否要继续操作？\n1.是\n2.否\n"))
            else:
                print("请重启管理系统并再次登陆！")
    elif choose == 3:
        print("请再次以管理员身份(用户名为admin)登陆！")
        res1 = signup()
        if res1:
            manager_choose = int(input("管理员用户，请选择您的操作：\n1.存书\n2.查询书籍\n3.查看用户欠款\n"))
            if manager_choose == 1:
                create_books()
            elif manager_choose == 2:
                search_books()
            elif manager_choose == 3:
                print("暂无此功能，敬请期待！")
                pass
        print()

