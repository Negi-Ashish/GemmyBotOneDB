from flask import Flask;
from flask import request,redirect;
import config.constants as const;
from botOneFun import test_read,read_balance,add_account,create_table,update_balance,check_existance,account_earn,fortune_teller,fd_earn

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
        return create_table()



##########################################################################################################

@app.route('/check_account',methods = ['GET'])
async def checkExistance():
    try:
        if request.method=="GET":
            userID = request.args.get('userID')
            return await check_existance(userID)
    except:
        return "Wrong json format"







@app.route('/add_account',methods = ['POST'])
async def addAccount():
    try:
        if request.headers["GEMMY_ACCESS_TOKEN"]!=const.GEMMY_ACCESS_TOKEN:
            return "You are not Authorised by GemmyHead"        
        if request.method=="POST":
            data = request.json
            return await add_account(data['userId'],data['walletBalance'],data['bankBalance'])
    except:
        return "You are not Authorised by GemmyHead"        



@app.route('/read_balance',methods = ['GET'])
async def readBalances():
    try:
        if request.method=="GET":
            userID = request.args.get('userID')
            return await read_balance(userID)
    except:
        return "ERROR"

@app.route('/update_balances',methods = ['PUT'])
async def updateBalance():
    try:
        if request.headers["GEMMY_ACCESS_TOKEN"]!=const.GEMMY_ACCESS_TOKEN:
            return "You are not Authorised by GemmyHead"
        if request.method=="PUT":
            data = request.json
            return await update_balance(data['userId'],data['walletBalance'],data['bankBalance'])
    except:
        return "You are not Authorised by GemmyHead"


@app.route('/account_earn',methods = ['PUT'])
async def earnGem():
    try:
        if request.headers["GEMMY_ACCESS_TOKEN"]!=const.GEMMY_ACCESS_TOKEN:
            return "You are not Authorised by GemmyHead"
        if request.method=="PUT":
            userID = request.args.get('userID')
            return await account_earn(userID)
    except:
        return "You are not Authorised by GemmyHead"        


@app.route('/fortune',methods = ['GET'])
async def fortune():
    try:
        if request.method=="GET":
            return await fortune_teller()
    except:
        return "Fortune error"



@app.route('/fixed_deposit',methods = ['PUT'])
async def updateBalance():
    try:
        if request.headers["GEMMY_ACCESS_TOKEN"]!=const.GEMMY_ACCESS_TOKEN:
            return "You are not Authorised by GemmyHead"
        if request.method=="PUT":
            data = request.json
            return await fd_earn(data['userId'],data)
    except:
        return "You are not Authorised by GemmyHead"


if __name__ == "__main__":
    app.run(debug=True)