from flask import Flask;
from flask import request,redirect;
import config.constants as const;
from flask_sqlalchemy import SQLAlchemy;
import psycopg2
import asyncio

DATABASE_URL=const.DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_size": 20}

db = SQLAlchemy(app)


@app.route('/test',methods = ['GET'])
def test_function_one():
    if request.method=="GET":
        return "Success"


@app.route('/test_read',methods = ['GET'])
async def test_function_three():
    if request.method=="GET":
        return await test_read()

@app.route('/test_write',methods = ['POST'])
async def test_function_four():
    if request.method=="POST":
        data = request.json
        print(data)
        print(type(data))
        return await test_write()

@app.route('/test_update',methods = ['PUT'])
async def test_function_five():
    if request.method=="PUT":
        return await test_update()

@app.route('/test_create',methods = ['POST'])
async def test_function_six():
    if request.method=="POST":
        return await create_table()


async def test_read():
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""SELECT * FROM user_account """        
        cur.execute(query)
        con.commit()
        record = cur.fetchall()
        print(record)
    finally:
        if con is not None:
            con.close()
    return "SUCCESS"



async def test_write():
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = """INSERT INTO user_account("user_id","wallet_balance","bank_balance") VALUES('Anjali',20,100) """
        cur.execute(query)
        con.commit()
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
    return ("INSERTED")


async def test_update():
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = """UPDATE user_account SET "wallet_balance"='200' Where ("user_id"='Ashish');"""
        cur.execute(query)
        con.commit()
    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
    return ("UPDATED")



async def create_table():
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()

        query = """CREATE TABLE user_account(
                    user_id VARCHAR (20) PRIMARY KEY,
                    wallet_balance INT NOT NULL,
                    bank_balance INT NOT NULL,
                    earn_start TIMESTAMP
                    );"""
        cur.execute(query)
        con.commit()
    finally:
        if con is not None:
            con.close()
    return ("Created")




if __name__ == "__main__":
    app.run(debug=True)