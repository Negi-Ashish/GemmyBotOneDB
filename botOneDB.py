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
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


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




def test_function():
    engine = db.create_engine(DATABASE_URL)
    data = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}  
    df = pd.DataFrame(data)  
    df.to_sql('test_db', con = engine, if_exists='append')
    return "NOT FAIL"



if __name__ == "__main__":
    app.run(debug=True)