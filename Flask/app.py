#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World!"

