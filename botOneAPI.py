from flask import Flask;
from flask import request,redirect;
import config.constants as const;
from botOneFun import test_read,read_balance,add_account,create_table,update_balance

DATABASE_URL=const.DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)




@app.route('/test',methods = ['GET'])
def test_function_one():
    if request.method=="GET":
        return "Success"


@app.route('/test_read',methods = ['GET'])
async def test_function_three():
    if request.method=="GET":
        return await test_read()



@app.route('/test_create',methods = ['POST'])
async def test_function_six():
    if request.method=="POST":
        return await create_table()



##########################################################################################################


@app.route('/add_account',methods = ['POST'])
async def addAccount():
    try:
        if request.method=="POST":
            data = request.json
            return await add_account(data['userId'],data['walletBalance'],data['bankBalance'])
    except:
        return "Wrong json format"



@app.route('/read_balance',methods = ['GET'])
async def read_balances():
    try:
        if request.method=="GET":
            userID = request.args.get('userID')
            return await read_balance(userID)
    except:
        return "ERROR"

@app.route('/update_balances',methods = ['PUT'])
async def update_balances():
    try:
        if request.method=="PUT":
            data = request.json
            return await update_balance(data['userId'],data['walletBalance'],data['bankBalance'])
    except:
        return "Wrong json format"

if __name__ == "__main__":
    app.run(debug=True)