import json

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

with open("data.json") as file:
    data = json.load(file)


@app.route("/registration", methods=['POST'])
def regUser():
    new_data = request.form

    if new_data["name"] not in [i["name"] for i in data]:
        data.append(new_data)
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
        return "Аккаунт создан"
    return "Аккаунт с таким именем уже есть"


@app.route("/registration")
def regTemplate():
    return render_template("sign-up.html")


@app.route("/all_users")
def all_users():
    return render_template("user-list.html", items=list([i["name"] for i in data]))


@app.route("/sign-in")
def sign_inTemplate():
    return render_template("sign-in.html")


@app.route("/sign-in", methods=['POST'])
def sign_in():
    new_data = request.form
    for acc in data:
        if new_data["name"] == str(acc["name"]) and new_data["password"] == str(acc["password"]):
            return render_template("account.html", acc=acc)
        elif new_data["name"] == str(acc["name"]) and new_data["password"] != str(acc["password"]):
            return "Пароль неправильный"
        else:
            continue
    return "Ошибка"


@app.route('/<deleted_account>')
def delete_acc(deleted_account):
    for acc in data:
        if acc['name'] == deleted_account:
            data.pop(data.index(acc))
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file)
            return all_users()


@app.route('/reset/<changer_account>')
def change_template(changer_account):
    return render_template('password-change.html', acc=changer_account )


@app.route('/reset/<changer_account>', methods=['POST'])
def change_password(changer_account):
    new_password = request.form.to_dict()
    for account in data:
        if account["name"] == changer_account:
            account['password'] = new_password['password']
            return "Пароль сменился"
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)



@app.route('/')
def index():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
