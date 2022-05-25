import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return render_template('index.html', tables=tables)


@app.route('/<string:workflowName>')
def workflow(workflowName):
    conn = get_db_connection()
    column_names = conn.execute('SELECT * FROM ' + workflowName)
    return render_template('workflow.html', workflowName = workflowName, columns=column_names)


@app.route('/createTemplate', methods=["POST", "GET"])
def createTemplate():
    if request.method == 'POST':
        variables = request.form.getlist('skill[]')
        print(variables)
        conn = get_db_connection()
        sql_scheme = 'CREATE TABLE ' + variables[0] + '(\n'
        for i in range(1, len(variables)):
            if (i == len(variables) - 1):
                sql_scheme = sql_scheme + variables[i].replace(" ", "") + ' VARCHAR(255) NOT NULL\n'
            else:
                sql_scheme = sql_scheme + variables[i].replace(" ", "") + ' VARCHAR(255) NOT NULL,\n'
        sql_scheme = sql_scheme + ');'
        print(sql_scheme)
        conn.execute(sql_scheme)
        conn.close()

    return render_template('createWorkFlow.html')


if __name__ == '__main__':
    app.run()
