import json

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open("data.json") as file:
    data = json.load(file)


class CRUD:
    @staticmethod
    @app.route("/registration", methods=['POST'])
    def regUser():
        new_data = request.form

        if new_data["name"] not in [i["name"] for i in data]:
            data.append(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            return {"correct": "Account is created"}, 200
        return jsonify({"error": "Account with this name already exist"}, 400)

    @staticmethod
    @app.route("/sign-in", methods=['POST'])
    def sign_in():
        new_data = request.form
        for acc in data:
            if new_data["name"] == str(acc["name"]) and new_data["password"] == str(acc["password"]):
                return render_template("account.html", acc=acc)
            elif new_data["name"] == str(acc["name"]) and new_data["password"] != str(acc["password"]):
                return jsonify({"error": "Invalid password"}, 400)
            else:
                continue
        return jsonify({"error": "Something gone wrong"}, 403)

    @staticmethod
    @app.route('/<deleted_account>', methods=["GET"])
    def delete_acc(deleted_account):
        for acc in data:
            if acc['name'] == deleted_account:
                data.remove(data.index(acc))
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file)
                return jsonify({"correct": "Account is deleted"}, 200)

    @staticmethod
    @app.route('/reset/<changer_account>', methods=['PUT', "POST"])
    def change_password(changer_account):
        new_password = request.form.to_dict()
        for account in data:
            if account["name"] == changer_account:
                account['password'] = new_password['password']
                return jsonify({"correct": "Password changed"}, 200)
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)


@app.route("/registration")
def regTemplate():
    return render_template("sign-up.html")


@app.route("/all_users")
def all_users():
    return render_template("user-list.html", items=list([i["name"] for i in data]))


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
