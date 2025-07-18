from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import pandas as pd

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='college_bus_management'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admins', methods=['GET', 'POST'])
def admins():
    conn = get_db_connection()
    query = "SELECT * FROM admin_data"
    df = pd.read_sql(query, conn)
    conn.close()
    
    search_value = ""
    if request.method == 'POST':
        search_value = request.form['search']
        if search_value:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)
            df = df[mask]

    # Convert dataframe to HTML table string (not a list!)
    table_html = df.to_html(classes='table table-striped table-bordered', index=False)
    
    return render_template('admins.html', tables=table_html, search_value=search_value)


@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_data (admin_name, admin_password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('admins'))
    return render_template('add_admin.html')

@app.route('/edit_admin/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin_data WHERE id = %s", (admin_id,))
    admin = cursor.fetchone()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("UPDATE admin_data SET username=%s, password=%s WHERE id=%s", (username, password, admin_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admins'))
    conn.close()
    return render_template('edit_admin.html', admin=admin)

@app.route('/delete_admin/<int:admin_id>')
def delete_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin_data WHERE id = %s", (admin_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admins'))

if __name__ == '__main__':
    app.run(debug=True)