import psycopg2
import config.constants as const;
from datetime import datetime,timedelta
import random;
from config.fortune import fortune_dict

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
                    fixed_deposit INT DEFAULT 0,
                    earn_start TIMESTAMP,
                    fd_start TIMESTAMP
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
        dt = datetime.now()
        if record == None:
            query = f"""UPDATE user_account SET "earn_start"='{dt}' Where ("user_id"='{userID}') """
            cur.execute(query)
            con.commit()
            return {"message":"You have started earning gems come after 4 hours to claim."}
        else:
            date_time_delta = record+timedelta(hours = 4)
            if(date_time_delta>=datetime.now()):
                remaining_time = date_time_delta-datetime.now()
                return {"message":f"""You can claim your gems after {remaining_time.seconds//3600}hr and {(remaining_time.seconds//60)%60}min."""}
            else:
                random_amount = random.randrange(101)
                query = f"""UPDATE user_account SET "wallet_balance"=("wallet_balance"+'{random_amount}'),"earn_start"=NULL Where ("user_id"='{userID}') """
                cur.execute(query)
                con.commit()
                return {"message":f"""You have earned {random_amount} gems"""}
    except:
        return {"message":"You currently dont have a account. Type '!gemmy balance' to create a account","Error":"account_earn"}
    finally:
        if con is not None:
            con.close()


async def fortune_teller():
    random_number = random.randrange(150)
    return {"message":fortune_dict[random_number]}



async def fd_earn(userID,data):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query_read = f"""SELECT "fd_start","fixed_deposit","bank_balance" FROM user_account Where ("user_id"='{userID}')"""
        cur.execute(query_read)
        con.commit()
        record = cur.fetchone()[0]
        print(cur.fetchone())
        print(record)
        return 0
        dt = datetime.now()
        if record == None:
            query = f"""UPDATE user_account SET "bank_balance"=("bank_balance"-'{data['amount']}'),"fd_start"='{dt}',"fixed_deposit"='{data['amount']}' Where ("user_id"='{userID}') """
            cur.execute(query)
            con.commit()
            intrest_gems = round((data['amount']*7)/100)
            return {"message":f"You have made a fixed deposit of {data['amount']} gems come after 3 days to claim {data['amount']+intrest_gems} gems."}
        else:
            date_time_delta = record+timedelta(days = 3)
            if(date_time_delta>=datetime.now()):
                remaining_time = date_time_delta-datetime.now()
                return {"message":f"""You can claim your gems after {remaining_time.days}days , {remaining_time.seconds//3600}hr and {(remaining_time.seconds//60)%60}min."""}
            else:
                query_read = f"""SELECT "fixed_deposit" FROM user_account Where ("user_id"='{userID}')"""
                cur.execute(query_read)
                con.commit()
                amount = cur.fetchone()[0]
                intrest_gems = round((amount*7)/100)
                if intrest_gems>1500:
                    intrest_gems=1500
                query = f"""UPDATE user_account SET "bank_balance"=("bank_balance"+"fixed_deposit"+'{intrest_gems}'),"fd_start"=NULL,"fixed_deposit"='0'  Where ("user_id"='{userID}') """
                cur.execute(query)
                con.commit()
                return {"message":f"""You have claimied your FD interest please check your bank balance."""}
    except Exception as e:
        return {"message":"There was an issue with your FD(fd_earn) please contact a MOD","Error":f"{e}"}
    finally:
        if con is not None:
            con.close()
