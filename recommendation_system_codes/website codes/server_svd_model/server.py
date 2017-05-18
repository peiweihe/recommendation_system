from flask import Flask, render_template, request
import pandas as pd
import os
app = Flask(__name__)
'''
data = [("chocolate bars",123),
        ("chocolate bars2",123),
        ("chocolate bars3",123),
        ("chocolate bars4",123),
        ("chocolate bars5",123),
        ("chocolate muffins",456),
        ("chocolate muffins1",456),
        ("tomato puree",456)]
'''
#@app.route('')\
#C:\\Users\\yijuzhang5\\Desktop\\2017-5-9 codes\\server_svd_model\\
data = list(pd.read_pickle('C:\\x.pickle'))
@app.route('/')
def index():
    # Template should be in templates/index.html
    return render_template('index2.html')

@app.route('/options')
def options():
    data = list(pd.read_pickle('C:\\x.pickle'))
    query = request.args.get('query', '')
    # todo: compute some actual recommendations!
    options = [(name,id) for (name,id) in data if id == int(query)]#if query in int(query)]
    return render_template('options.html', query=query, options=options)

@app.route('/recommend')
def recommend():
    item  = request.args.get('item', '')
    recommendations = ["Something based on {item}".format(**locals())]
    return render_template('recommend2.html', recommendations=recommendations)

if __name__ == "__main__":
    # This is only called if the script is run directly
    # This is the 'normal' way to control execution in python
    app.run(debug=True)


