import psycopg2
import config.constants as const;
from datetime import datetime,timedelta

DATABASE_URL=const.DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


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



def create_table():
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

##################################################################################################

async def check_existance(userID):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""SELECT COUNT("user_id") FROM user_account Where ("user_id"='{userID}')"""        
        cur.execute(query)
        con.commit()
        record = cur.fetchone()[0]
        if record == 0:
            return {"existance":False}
    except:
        return {"existance":False,"Error":"User alredy exists"}
    finally:
        if con is not None:
            con.close()
    return {"existance":True}


async def add_account(userID,walletBalance,bankBalance):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""INSERT INTO user_account("user_id","wallet_balance","bank_balance") VALUES('{userID}',{walletBalance},{bankBalance}) """
        cur.execute(query)
        con.commit()
    except:
        return {"inserted":False,"Error":"User alredy exists"}
    finally:
        if con is not None:
            con.close()
    return {"inserted":True}


async def read_balance(userID):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""SELECT "wallet_balance","bank_balance" FROM user_account Where ("user_id"='{userID}')"""        
        cur.execute(query)
        con.commit()
        record = cur.fetchone()
        print(record)
        return {"wallet_balance":record[0],"bank_balance":record[1]}
    except:
        return {"wallet_balance":"FAILURE","bank_balance":"FAILURE","error":"No such Id exists"}
    finally:
        if con is not None:
            con.close()


async def update_balance(userID,walletBalance,bankBalance):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""UPDATE user_account SET "wallet_balance"='{walletBalance}',"bank_balance"='{bankBalance}' Where ("user_id"='{userID}');"""
        cur.execute(query)
        con.commit()
        return {"updated":True}
    except:
        return {"updated":False,"Error":"update_balance error"}
    finally:
        if con is not None:
            con.close()



async def account_earn(userID):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query_read = f"""SELECT "earn_start" FROM user_account Where ("user_id"='{userID}')"""
        cur.execute(query_read)
        con.commit()
        record = cur.fetchone()[0]

        print("Old Time Stamp",record)
        print(type(record))

        if record == None:
            dt = datetime.now()
            query = f"""UPDATE user_account SET "earn_start"='{dt}' Where ("user_id"='{userID}') """
            cur.execute(query)
            con.commit()
            return {"message":"You have started earning come after 5 hours to claim."}
        else:
            date_time_delta = record+timedelta(hours = 4)
            if(date_time_delta>=datetime.now()):
                remaining_time = date_time_delta-datetime.now()
                return {"message":f"""You can claim reward after {remaining_time.seconds//3600}hr and {(remaining_time.seconds//60)%60}min."""}

    except:
        return {"update":False,"Error":"User alredy exists"}
    finally:
        if con is not None:
            con.close()
