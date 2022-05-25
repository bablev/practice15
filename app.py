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


@app.route('/runworkflow/<string:workflow>', methods=["POST", "GET"])
def runworkflow(workflow):
    if request.method == 'POST':
        data = request.form.to_dict()
        values = []
        for key, value in data.items():
            values.append(value)
        print(values)
        conn = get_db_connection()
        sql_scheme = 'INSERT INTO ' + workflow + '('
        counter = 0
        for key in data:
            counter += 1
            if counter == len(data):
                sql_scheme += key + ')'
            else:
                sql_scheme += key + ','
        sql_scheme += ' VALUES('
        for i in range(0, counter):
            if i == counter - 1:
                sql_scheme += '?)'
            else:
                sql_scheme += '?,'
        conn.execute(sql_scheme, values)
    conn = get_db_connection()
    variables = conn.execute('SELECT * FROM ' + workflow)
    return render_template('runworkflow.html', variables=variables, workflow=workflow)


@app.route('/<string:workflowName>', methods=["POST", "GET"])
def workflow(workflowName):
    print(workflowName)
    conn = get_db_connection()
    column_names = conn.execute('SELECT * FROM ' + workflowName)
    return render_template('workflow.html', workflowName=workflowName, columns=column_names)


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
