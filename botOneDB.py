from flask import Flask;
from flask import request,redirect;
import config.constants as const;
from flask_sqlalchemy import SQLAlchemy;

DATABASE_URL=const.DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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


def post_db(id,bank,wallet):
    data = UserAccountModal(id,bank,wallet)
    db.session.add(data)
    db.session.commit()
    return "Success"


# @app.route('/Discord-AssignRole',methods = ['GET'])
# def AssignRole_Discord():
#     if request.method=="GET":
#         access_token = request.headers["access_token"]
#         no_of_nft = request.headers["no_of_nft"]
#         return assign_owners_role(access_token,int(no_of_nft))


if __name__ == "__main__":
    app.run(debug=True)