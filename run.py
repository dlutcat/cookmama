#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.escape import json_encode
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')
    #return json_encode({ 'code': 12 })

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
