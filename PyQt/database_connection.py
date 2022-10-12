import datetime
import psycopg2
from persiantools.jdatetime import JalaliDate

jdate = JalaliDate.today().strftime("%Y/%m/%d")
# adds system gregorian time and date but with tehran timezone(sys default)!
u_datetime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
# connecting to postgres database
try:
    conn = psycopg2.connect(database="postgres", user="postgres", password="postgre", )
    curr = conn.cursor()

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into mobile table", error)


# noinspection SqlInjection
class Database(object):

    def __init__(self):

        # result type is None cause used none as argument in main.py
        self.result = None
        self.username = None
        self.id = []
        self.result_edit = None

    def check_connection(self, username, password):
        # wrong version :query=conn.execute("SELECT * FROM newtable WHERE USERNAME = ? AND PASSWORD = ?",(username,
        # password)) 

        curr.execute(f"select * from employee where username='{username}' and password='{password}' ")
        qresult = curr.fetchall()
        # print(result)
        if len(qresult) > 0:
            print("done")
            self.result = True
            self.username = username

        else:
            print("account not found")
            self.result = False

    def insert_data(self, pps1, pps2, pps3, pps4, title, combo, *args):
        # Use INSERT ... ON DUPLICATE KEY UPDATE
        # if the user clicked on save in insert mode use 'on conflict' function

        query = f"INSERT INTO proposal (username,pps1,pps2,pps3,pps4,title,date,status,version,u_datetime,organ) \
        VALUES ('{self.username}','{pps1}','{pps2}','{pps3}','{pps4}','{title}','{jdate}','1',1,'{u_datetime}','{combo}')"
        # ON CONFLICT (id) DO  update set id=EXCLUDED.id pps1='{pps1}',pps2='{pps2}',pps3='{pps3}',pps4='{pps4}',
        # version=proposal.version + 1 ;" 
        curr.execute(query)
        conn.commit()

        curr.execute(f"select id from proposal where title='{title}'")
        self.id_result = curr.fetchall()
        # self.id=[]
        for i in self.id_result:
            for j in i:
                self.id.append(j)
        # *self.id return id from current proposal but simple id is given by item list
        self.id = self.id[0]

    def update_data(self, pps1, pps2, pps3, pps4, title, id, combo):
        if id:
            query = f"update proposal set pps1='{pps1}',pps2='{pps2}',pps3='{pps3}',pps4='{pps4}',title='{title}',u_datetime='{u_datetime}',organ='{combo}',version=proposal.version + 1 where id={id}"
        elif self.id:
            query = f"update proposal set pps1='{pps1}',pps2='{pps2}',pps3='{pps3}',pps4='{pps4}',title='{title}',u_datetime='{u_datetime}',organ='{combo}',version=proposal.version + 1 where id={self.id}"
        curr.execute(query)
        conn.commit()

    def delete_data(self):
        query = f"update proposal set status='0' where id='{self.id}'"

        curr.execute(query)
        conn.commit()

    def edit_data(self, id):
        # *self.id return id from current proposal but simple id is given by item list
        query = f"SELECT id,username,pps1,pps2,pps3,pps4,title,date,organ FROM proposal WHERE id='{id}'"

        curr.execute(query)
        self.result_edit = curr.fetchall()

        # conn.commit()

    def show_user_data(self, username):
        query = f"select id,username,name,date,title from proposal where username='{username}' and status='1' order by id desc"
        curr.execute(query)
        self.result_show_user_data = curr.fetchall()

    def show_all_data(self):
        query = "select id,username,name,date,title from proposal where status='1' order by id desc"
        curr.execute(query)
        self.result_show_all_data = curr.fetchall()

        # cur.execute("SELECT age FROM newtable")  # for age in cur.fetchall() :  # print( age )

    def last_data(self):
        query = "SELECT id,username,pps1,pps2,pps3,pps4,title,date,organ FROM proposal where status='1' and id=(select max(id) from proposal where status='1')"
        curr.execute(query)
        self.result_edit = curr.fetchall()

    def first_data(self):
        query = "SELECT id,username,pps1,pps2,pps3,pps4,title,date,organ FROM proposal where status='1' and id=(select min(id) from proposal where status='1')"
        curr.execute(query)
        self.result_edit = curr.fetchall()

    def previous_data(self, current_id):
        query = f"SELECT id,username,pps1,pps2,pps3,pps4,title,date,organ FROM proposal where id={current_id}-1 and status='1' "
        curr.execute(query)
        self.result_edit = curr.fetchall()
        query2= f"select id from proposal where id=(select min(id-1) from proposal where status='1') and status='1'"
        curr.execute(query2)
        self.previous_result=curr.fetchall()

    def next_data(self, current_id):
        query = f"SELECT id,username,pps1,pps2,pps3,pps4,title,date,organ FROM proposal where id={current_id}+1 and status='1'"
        curr.execute(query)
        self.result_edit = curr.fetchall()
        query2 = f"select id from proposal where id=(select max(id+1) from proposal) and status='1'"
        curr.execute(query2)
        self.next_reslt = curr.fetchall()
