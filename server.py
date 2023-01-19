from flask import *
import psycopg2

app = Flask("bank_web_app")

password = open("password.txt").read()
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="bank",
    user="postgres",
    password=password)


@app.route("/api/v1/customers/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    print(f"called/customers/customer_id/{customer_id}")
    with conn:
        with conn.cursor() as cur:
            sql = "select * from customers where db_id = %s"
            cur.execute(sql, (customer_id,))
            result = cur.fetchone()
            if result:
                ret_data = {'customer_id': result[0],
                            'state_id': result[1],
                            'name': result[2],
                            'address': result[3]}
                # response = app.response_class(
                #     response=json.dumps(ret_data),
                #     status=200,
                #     mimetype='application/json'
                # )
                # return response

                return jsonify(ret_data)
            else:
                return app.response_class(status=404)



@app.route("/customers/<int:customer_id>", methods=['PUT'])
def update_customer(customer_id):
    new_data = request.form
    updates_str_list = []
    for field in new_data:
        updates_str_list.append(f"{field}=%s")
    sql = f"UPDATE customers SET {','.join(updates_str_list)} WHERE id=%s"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(new_data.keys()) + tuple([customer_id]))
            if cur.rowcount == 1:
                # update succeeded
                return app.response_class(status=200)
    return app.response_class(status=500)


# print(update_customer(1))

if __name__ == '__main__':
    app.run(debug=True)
