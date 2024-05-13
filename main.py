import os

import psycopg2 as psycopg2
from fastapi import FastAPI, Depends
from fastapi_pagination import Page, Params, paginate
import hashlib

app = FastAPI()
conn = psycopg2.connect(dbname="Cup_Store", user="root", password="NasSidAdmin789", host="109.238.83.39",
                        port="5665")


## ------cheques------

@app.post("/add_cheque/{order_id}/{cheque_text}/{pay_type_id}")
async def add_new_cheque(order_id: int, cheque_text: str, pay_type_id: int):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO cheques (order_id, cheque, pay_type) VALUES (\'{order_id}\', \'{cheque_text}\', \'{pay_type_id}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM cheques WHERE order_id = \'{order_id}\' ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/cheque/{order_id}")
async def get_cheque_for_order(order_id: int):
    cheque = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM cheques where order_id = \'{order_id}\'")
    for i in cursor.fetchall():
        cheque["id"] = i[0]
        cheque["order_id"] = i[1]
        cheque["cheque"] = i[2]
        cheque["pay_type"] = i[3]
    return cheque


@app.get("/cheques")
async def get_all_cheques():
    cheques = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cheques")
    for i in cursor.fetchall():
        cheques.append({
            "id": i[0],
            "order": i[1],
            "cheque": i[2],
            "pay_type": i[3]
        })
    return cheques


@app.put("/update_cheque/{cheque_id}/{order_id}/{cheque_text}/{pay_type_id}")
async def update_cheque(cheque_id: int, order_id: int, cheque_text: str, pay_type_id: int):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE cheques SET order_id = \'{order_id}\', cheque = \'{cheque_text}\',"
                   f" pay_type = \'{pay_type_id}\' where id = \'{cheque_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_cheque/{cheque_id}")
async def delete_cheque(cheque_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM cheques where id = \'{cheque_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##--------cups---------

@app.post("/add_cup/{name}/{cost}/{description}")
async def add_new_cup(name: str, cost: int, description: str):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO cups (name, cost, description) VALUES (\'{name}\', \'{cost}\', \'{description}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM cups ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/cup/{cup_name}")
async def get_cup_by_name(cup_name: str):
    cup = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM cups where name = \'{cup_name}\'")
    for i in cursor.fetchall():
        cup["id"] = i[0]
        cup["name"] = i[1]
        cup["cost"] = i[2]
        cup["description"] = i[3]
    return cup


@app.get("/cups")
async def get_all_cups(
        params: Params = Depends()
):

    cups = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cups")
    for i in cursor.fetchall():
        cups.append({
            "id": i[0],
            "name": i[1],
            "cost": i[2],
            "description": i[3]
        })
    pages = []
    for i in range(0, len(cups), params.size):
        pages.append(cups[i:i + params.size])
    return pages[params.page - 1]


@app.put("/update_cup/{cup_id}/{name}/{cost}/{description}")
async def update_cup(cup_id: int, name: str, cost: int, description: str):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE cups SET name = \'{name}\', cost = \'{cost}\',"
                   f" description = \'{description}\' where id = \'{cup_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_cup/{cup_id}")
async def delete_cup(cup_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM cups where id = \'{cup_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##------discounts-------

@app.post("/add_discount/{discount_name}")
async def add_new_discount(discount_name: int):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO discounts (discount) VALUES (\'{discount_name}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM discounts ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/discount/{discount_name}")
async def get_discount_by_name(discount_name: int):
    discount = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM discounts where discount = \'{discount_name}\'")
    for i in cursor.fetchall():
        discount["id"] = i[0]
        discount["discount"] = i[1]
    return discount


@app.get("/discounts")
async def get_all_discounts():
    discounts = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM discounts")
    for i in cursor.fetchall():
        discounts.append({
            "id": i[0],
            "discount": i[1],
        })
    return discounts


@app.put("/update_discount/{discount_id}/{discount_name}")
async def update_discount(discount_id: int, discount_name: int):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE discounts SET discount = \'{discount_name}\' where id = \'{discount_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_discount/{discount_id}")
async def delete_discount(discount_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM discounts where id = \'{discount_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##---------orders------------

@app.post("/add_order/{user_id}/{staff_id}/{cost}/{status_id}/{purchased_cups_text}")
async def add_new_order(user_id: int, staff_id: int, cost: int, status_id: int, purchased_cups_text: str):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO orders (user_id, staff, cost, status, purchased_cups) VALUES (\'{user_id}\', \'{staff_id}\', \'{cost}\', \'{status_id}\', \'{purchased_cups_text}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM orders ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/users_orders/{user_id}")
async def get_orders_by_user(user_id: int):
    orders = []
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM orders where user_id = \'{user_id}\'")
    for i in cursor.fetchall():
        orders.append({
            "id": i[0],
            "user": i[1],
            "staff": i[2],
            "cost": i[3],
            "status": i[4],
            "purchased_cups": i[5]
        })
    return orders


@app.get("/orders")
async def get_all_orders():
    orders = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    for i in cursor.fetchall():
        orders.append({
            "id": i[0],
            "user": i[1],
            "staff": i[2],
            "cost": i[3],
            "status": i[4],
            "purchased_cups": i[5]
        })
    return orders


@app.put("/update_order/{order_id}/{user_id}/{staff_id}/{cost}/{status_id}/{purchased_text}")
async def update_order(order_id: int, user_id: int, staff_id: int, cost: int, status_id: int, purchased_text: str):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE orders SET user_id = \'{user_id}\', staff = \'{staff_id}\', cost = \'{cost}\', status = \'{status_id}\', purchased_cups = \'{purchased_text}\'  where id = \'{order_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_order/{order_id}")
async def delete_order(order_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM orders where id = \'{order_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##-------pay_types--------

@app.post("/add_pay_type/{name}")
async def add_new_pay_type(name: str):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO pay_types (name) VALUES (\'{name}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM pay_types ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/pay_type/{pay_id}")
async def get_pay_types_by_id(pay_id: int):
    pay_type = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM pay_types where id = \'{pay_id}\'")
    for i in cursor.fetchall():
        pay_type["id"] = i[0]
        pay_type["name"] = i[1]
    return pay_type


@app.get("/pay_types")
async def get_all_pay_types():
    pay_types = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pay_types")
    for i in cursor.fetchall():
        pay_types.append({
            "id": i[0],
            "name": i[1],
        })
    return pay_types


@app.put("/update_pay_type/{pay_id}/{name}")
async def update_pay_type(pay_id: int, name: str):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE pay_types SET name = \'{name}\' where id = \'{pay_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_pay_type/{pay_id}")
async def delete_pay_type(pay_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM pay_types where id = \'{pay_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##----------positions-----------

@app.post("/add_position/{name}")
async def add_new_position(name: str):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO positions (name) VALUES (\'{name}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM positions ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/position/{pos_id}")
async def get_position_by_id(pos_id: int):
    position = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM positions where id = \'{pos_id}\'")
    for i in cursor.fetchall():
        position["id"] = i[0]
        position["name"] = i[1]
    return position


@app.get("/positions")
async def get_all_positions():
    positions = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM positions")
    for i in cursor.fetchall():
        positions.append({
            "id": i[0],
            "name": i[1],
        })
    return positions


@app.put("/update_position/{pos_id}/{name}")
async def update_position(pos_id: int, name: str):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE positions SET name = \'{name}\' where id = \'{pos_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_position/{pos_id}")
async def delete_position(pos_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM positions where id = \'{pos_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##------------statuses-----------

@app.post("/add_status/{name}")
async def add_new_status(name: str):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO statuses (name) VALUES (\'{name}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM statuses ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/status/{status_id}")
async def get_status_by_id(status_id: int):
    status = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM statuses where id = \'{status_id}\'")
    for i in cursor.fetchall():
        status["id"] = i[0]
        status["name"] = i[1]
    return status


@app.get("/statuses")
async def get_all_statuses():
    statuses = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM statuses")
    for i in cursor.fetchall():
        statuses.append({
            "id": i[0],
            "name": i[1],
        })
    return statuses


@app.put("/update_status/{st_id}/{name}")
async def update_status(st_id: int, name: str):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE statuses SET name = \'{name}\' where id = \'{st_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_status/{st_id}")
async def delete_status(st_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM statuses where id = \'{st_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


##-------staff---------

@app.post("/register_staff/{name}/{pos_id}/{login}/{password}")
async def add_new_staff(name: str, pos_id: int, login: str, password: str):
    salt = os.urandom(16).hex()
    str(salt)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO staff (name, position, login, password, salt) VALUES (\'{name}\', \'{pos_id}\', \'{login}\', \'{password}\', \'{salt}\')")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM staff ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/authorize_staff/{login}/{password}")
async def authorize_staff(login: str, password: str):
    user = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM staff where login = \'{login}\'")
    fetchall = cursor.fetchall()
    if len(fetchall) == 0:
        return {"Message": "Not found"}
    for i in fetchall:
        if (hashlib.sha256(i[5].encode() + i[4].encode()).hexdigest() ==
                hashlib.sha256(i[5].encode() + password.encode()).hexdigest()):
            user["id"] = i[0]
            user["name"] = i[1]
            user["position"] = i[2]
            user["login"] = i[3]
            user["password"] = i[4]
            user["salt"] = i[5]
            return user
    return {"Message": "incorrect password"}


@app.get("/staff/{staff_id}")
async def get_staff_by_id(staff_id: int):
    staff = []
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM staff where id = \'{staff_id}\'")
    for i in cursor.fetchall():
        staff.append({
            "id": i[0],
            "name": i[1],
            "position": i[2],
            "login": i[3],
            "password": i[4],
            "salt": i[5]
        })
    return staff


@app.get("/staff")
async def get_all_staff():
    staff = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff")
    for i in cursor.fetchall():
        staff.append({
            "id": i[0],
            "name": i[1],
            "position": i[2],
            "login": i[3],
            "password": i[4],
            "salt": i[5]
        })
    return staff


@app.put("/update_staff/{staff_id}/{name}/{position}/{login}/{password}")
async def update_staff(staff_id: int, name: str, position: int, login: str, password: str):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE staff SET name = \'{name}\', position = \'{position}\', login = \'{login}\', password = \'{password}\' where id = \'{staff_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_staff/{staff_id}")
async def delete_staff(staff_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM staff where id = \'{staff_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}

##-----------users---------------

@app.post("/register_user/{login}/{password}/{name}")
async def add_new_user(login: str, password: str, name: str):
    salt = os.urandom(16).hex()
    str(salt)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO users (login, password, salt, name, all_purchase_sum, discount) VALUES (\'{login}\', \'{password}\', \'{salt}\', \'{name}\', 0, 4)")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM users ORDER BY id")
    return {"New id": cursor.fetchall()[-1]}


@app.get("/authorize_user/{login}/{password}")
async def authorize_user(login: str, password: str):
    user = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users where login = \'{login}\'")
    fetchall = cursor.fetchall()
    if len(fetchall) == 0:
        return {"Message": "Not found"}
    for i in fetchall:
        if (hashlib.sha256(i[3].encode() + i[2].encode()).hexdigest() ==
                hashlib.sha256(i[3].encode() + password.encode()).hexdigest()):
            user["id"] = i[0]
            user["login"] = i[1]
            user["password"] = i[2]
            user["salt"] = i[3]
            user["name"] = i[4]
            user["all_purchase_sum"] = i[5]
            user["discount"] = i[6]
            return user
    return {"Message": "incorrect password"}


@app.get("/user/{user_id}")
async def get_user_by_id(user_id: int):
    user = {}
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users where id = \'{user_id}\'")
    for i in cursor.fetchall():
        user["id"] = i[0]
        user["login"] = i[1]
        user["password"] = i[2]
        user["salt"] = i[3]
        user["name"] = i[4]
        user["all_purchase_sum"] = i[5]
        user["discount"] = i[6]
    return user


@app.get("/users")
async def get_all_users():
    users = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    for i in cursor.fetchall():
        users.append({
            "id": i[0],
            "login": i[1],
            "password": i[2],
            "salt": i[3],
            "name": i[4],
            "all_purchase_goods": i[5],
            "discount": i[6]
        })
    return users


@app.put("/update_user/{user_id}/{login}/{password}/{name}/{all_purchase_sum}")
async def update_user(user_id: int, login: str, password: str, name: str, all_purchase_sum: int):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET name = \'{name}\', all_purchase_sum = \'{all_purchase_sum}\', login = \'{login}\', password = \'{password}\' where id = \'{user_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users where id = \'{user_id}\'")
    conn.commit()
    cursor.close()
    return {"status": "OK"}


