# coding=utf-8
__author__ = 'litao'

import sys
import os
import time
import markdown2
from webserver import app

from flask import render_template, request, redirect, url_for, json, send_file
from flask import render_template_string

from boolean import BooleanRetrieval
model = BooleanRetrieval.get_instance()

import os
cwd = os.getcwd()
print('view cwd:', cwd)
url_temp = 'http://www.jianshu.com/p/{}'
page_dir = os.path.join(cwd, 'page')

@app.route('/', methods=['GET','POST'])
def resonse_user():
    try:
        if request.method == 'GET':
            return render_template('template.html', result_list=[])
        elif request.method == 'POST':
            # print(request.form)
            value = request.form.get("input")
            data_list = model.search(value)
            # data_list = ['d633a115e363.md', '7dea5e957101.md']
            result_list = [(v, url_temp.format(v.split('.')[0])) for v in data_list]
            return render_template('template.html', result_list=result_list)
    except Exception as e:
        print(e)
        return render_template("template.html")

@app.route('/md/<id>', methods=['GET'])
def render_md(id):
    md_path = os.path.join(page_dir, id)
    html = markdown2.markdown_path(md_path)
    return render_template_string(html)
