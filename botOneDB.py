from flask import Flask;
from flask import request,redirect;
import config.constants as const;
from flask_sqlalchemy import SQLAlchemy;
from botOneFun import test_read,read_balance,test_write,test_update,create_table

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
    try:
        if request.method=="POST":
            data = request.json
            return await test_write(data['userId'],data['walletBalance'],data['bankBalance'])
    except:
        return "Wrong json format"

@app.route('/test_update',methods = ['PUT'])
async def test_function_five():
    if request.method=="PUT":
        return await test_update()

@app.route('/test_create',methods = ['POST'])
async def test_function_six():
    if request.method=="POST":
        return await create_table()

@app.route('/read_balance',methods = ['GET'])
async def read_balances():
    try:
        if request.method=="GET":
            userID = request.args.get('userID')
            return await read_balance(userID)
    except:
        return "ERROR"



if __name__ == "__main__":
    app.run(debug=True)