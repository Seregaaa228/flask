import json

from flask import Flask, render_template, request, jsonify
from pydantic import BaseModel

app = Flask(__name__)

from user import UserCRUD

user = UserCRUD("data.json")


class NewUserModel(BaseModel):
    login: str
    password: str


@app.route("/registration", methods=['POST'])
def reg_user():
    new_user = NewUserModel(**request.json)

    if user.get_item(new_user.login) is not None:
        return jsonify({"info": "User with such name already exists"}), 403

    user.set_item(new_user.login, {"password": new_user.password})
    user.write_to_file()

    return jsonify({"info": "Success"})


@app.route("/sign-in", methods=['POST'])
def sign_in():
    acc_signed = NewUserModel(**request.json)

    if user.get_item(acc_signed.login) is not None and user.get_item(acc_signed.login)['password'] == acc_signed.password:
        return render_template("account.html", acc=acc_signed.login)
    elif user.get_item(acc_signed.login) is not None and user.get_item(acc_signed.login)['password'] != acc_signed.password:
        return jsonify({"info": "Invalid password"}), 401
    elif user.get_item(acc_signed.login) is None:
        return jsonify({"info": "User with such name doesnt exists"}), 401

    else:
        return jsonify({"info": "Unknown error"}), 403


@app.route('/delete/<deleted_account>', methods=["GET", "DELETE"])
def delete_acc(deleted_account):
    user.delete_item(deleted_account)
    user.write_to_file()
    return jsonify({"info": "Success"})


@app.route('/reset/<changer_account>', methods=["PUT"])
def change_password(changer_account):
    new_password = request.json
    if user.get_item(changer_account) is not None and user.get_item(changer_account)['password'] != new_password:
        user.set_item(changer_account, {"password": new_password['password']})
        user.write_to_file()
        return jsonify({"info": "Success"})
    else:
        return jsonify({"info": "Unknown error"}), 403


@app.route("/<account_home>")
def account(account_home):
    return render_template("account.html", acc=account_home)


@app.route("/registration")
def regTemplate():
    return render_template("sign-up.html")


@app.route("/all_users")
def all_users():
    return str(user.get_all_users())


@app.route("/sign-in")
def sign_inTemplate():
    return render_template("sign-in.html")


@app.route('/reset/<changer_account>')
def change_template(changer_account):
    return render_template('password-change.html', acc=changer_account)


@app.route('/')
def index():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
