from flask import Flask, request, render_template, jsonify
import spacy
import wikipediaapi
import random
import matplotlib.pyplot as plt
import os


@app.route("/")
def home():
    return render_template("index.html")