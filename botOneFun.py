import psycopg2
import config.constants as const;


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

async def add_account(userID,walletBalance,bankBalance):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""INSERT INTO user_account("user_id","wallet_balance","bank_balance") VALUES('{userID}',{walletBalance},{bankBalance}) """
        cur.execute(query)
        con.commit()
    except:
        return "User alredy Exists"
    finally:
        if con is not None:
            con.close()
    return ("INSERTED")


async def read_balance(userID):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""SELECT "wallet_balance","bank_balance" FROM user_account Where ("user_id"='{userID}')"""        
        cur.execute(query)
        con.commit()
        record = cur.fetchone()
        print(record)
    finally:
        if con is not None:
            con.close()
    return "SUCCESS"

async def update_balance(userID,walletBalance,bankBalance):
    try:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor()
        query = f"""UPDATE user_account SET "wallet_balance"='{walletBalance}',"bank_balance"='{bankBalance}' Where ("user_id"='{userID}');"""
        cur.execute(query)
        con.commit()
    finally:
        if con is not None:
            con.close()
    return ("UPDATED")