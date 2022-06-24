from flask import Flask;
from flask import request,redirect;
import config.constants as const;
from flask_sqlalchemy import SQLAlchemy;
import pandas as pd 
import psycopg2




DATABASE_URL=const.DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_size": 20}

db = SQLAlchemy(app)


class UserAccountModal(db.Model):
    __tablename__ = 'user_account_modal'
    discordId = db.Column(db.String(50),primary_key=True)
    bank_balance = db.Column(db.Integer)
    wallet_balance = db.Column(db.Integer)

    def __init__(self,discordId,bank_balance,wallet_balance):
        self.discordId = discordId
        self.bank_balance=bank_balance
        self.wallet_balance=wallet_balance


# def post_db(id,bank,wallet):
#     data = UserAccountModal(id,bank,wallet)
#     db.session.add(data)
#     db.session.commit()
#     return "Success"


@app.route('/test',methods = ['GET'])
def test_function_one():
    if request.method=="GET":
        return "Success"


@app.route('/test_function',methods = ['GET'])
def test_function_two():
    if request.method=="GET":
        return test_function()


@app.route('/test_read',methods = ['GET'])
def test_function_three():
    if request.method=="GET":
        return test_read()

@app.route('/test_write',methods = ['POST'])
def test_function_four():
    if request.method=="POST":
        return test_write()

@app.route('/test_update',methods = ['PUT'])
def test_function_five():
    if request.method=="PUT":
        return test_update()


def test_read():
    try:

        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()

        query = f"""SELECT * 
                    FROM test_db"""        
        results = pd.read_sql(query, con).set_index('Name')
        print("typerOF",type(results))
        print(results)
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')
    
    return ("PASSED")





def test_write():
    try:

        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()

        query = """INSERT INTO test_db("Name","Age") VALUES('Ashish',20) """

        cur.execute(query)
        con.commit()

        
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')
    
    return ("INSERTED")




def test_update():
    try:

        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()

        query = """UPDATE test_db SET test_db.Age=111 Where test_db.Name=John"""

        cur.execute(query)
        con.commit()
        
        
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')
    
    return ("UPDATED")




def test_function():
    engine = db.create_engine(DATABASE_URL,{"pool_size": 20})
    data = {'Name': ['John'], 'Age': [20]}  
    df = pd.DataFrame(data).set_index('Name')
    print(df)
    df.to_sql('test_db', con = engine, if_exists='append')
    return "NOT FAIL"



if __name__ == "__main__":
    app.run(debug=True)