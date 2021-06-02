from flask import Flask
from routes.route_manager import RouteManager
import logging

app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')
route_control = RouteManager()


# POST /clients => Creates a new client
@app.route("/clients", methods=["POST"])
def post_client():
    return route_control.post_client()


# GET /clients => gets all clients
@app.route("/clients", methods=["GET"])
def get_clients():
    return route_control.get_clients()


# GET /clients/10 => get client with id of 10
@app.route("/clients/<client_id>", methods=["GET"])
def get_client(client_id: str):
    return route_control.get_client(client_id)


# PUT /clients/12 => updates client with id of 12
@app.route("/clients/<client_id>", methods=["PUT"])
def update_client(client_id: str):
    return route_control.update_client(client_id)


# DELETE /clients/15 => deletes client with the id of 15
@app.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id: str):
    return route_control.remove_client(client_id)


# POST /clients/5/accounts =>creates a new account for client with the id of 5
@app.route("/clients/<client_id>/accounts", methods=["POST"])
def add_new_account_for(client_id: str):
    return route_control.post_new_account_for(client_id)


# GET /clients/7/accounts => get all accounts for client 7
# GET /clients/7/accounts?amountLessThan=2000&amountGreaterThan400
@app.route("/clients/<client_id>/accounts", methods=["GET"])
def get_all_accounts_for(client_id: str):
    return route_control.get_all_accounts_for(client_id)


# GET /clients/9/accounts/4 => get account 4 for client 9
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
def get_account_for(client_id: str, account_id: str):
    return route_control.get_account_for(client_id, account_id)


# PUT /clients/10/accounts/3 => update account  with the id 3 for client 10
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
def update_account_for(client_id: str, account_id: str):
    return route_control.update_account_for(client_id, account_id)


# DELETE /clients/15/accounts/6 => delete account 6 for client 15
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
def delete_account_for(client_id: str, account_id: str):
    return route_control.delete_account_for(client_id, account_id)


# PATCH /clients/17/accounts/12 => Withdraw/deposit given amount (Body: {"deposit":500} or {"withdraw":250}
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
def update_balance_for(client_id: str, account_id: str):
    return route_control.update_balance_for(client_id, account_id)


# PATCH /clients/12/accounts/7/transfer/8 => transfer funds from account 7 to account 8 (Body: {"amount":500})
@app.route("/clients/<client_id>/accounts/<account_from_id>/transfer/<account_to_id>", methods=["PATCH"])
def transfer_funds_to(client_id: str, account_from_id: str, account_to_id: str):
    return route_control.transfer_funds_to(client_id, account_from_id, account_to_id)


# Start web server
app.run(debug=True)
