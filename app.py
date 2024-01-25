import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request

import matplotlib
matplotlib.use('Agg') # Use the Agg backend
import matplotlib.pyplot as plt
plt.style.use('dark_background') # For customizing theme

import io
import base64

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///datapoints.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Get points from html
        x = int(request.form.get("x"))
        y = int(request.form.get("y"))

        # Remember points in database
        db.execute("INSERT INTO points (x, y) VALUES (?, ?)", x, y)

        return redirect("/")

    else:

        # Get points from database
        points = db.execute("SELECT * FROM points")

        # Store x and y values as seperate lists
        x = []
        y = []
        if points:
            for dict in points:
                x.append(dict["x"])
                y.append(dict["y"])

        img = plot_points(x, y)

        return render_template("index.html", img=img, form_action=["/", "/dataset"])


@app.route("/dataset", methods=["POST"])
def dataset():

    # Clear database
    db.execute("DELETE FROM points")

    # Insert points into database
    db.execute("INSERT INTO points (x, y) VALUES (1,3), (2,12), (3,10), (4,10), (5,20), (4,20), (5,15), (10,20), (3,7), (2, 6), (8, 18), (7, 16)")

    return redirect("/")

@app.route("/plot", methods=["POST"])
def plot():

    # Get points from database
    points = db.execute("SELECT * FROM points")

    # Store x and y values as seperate lists
    if points:
        x = []
        y = []
        for dict in points:
            x.append(dict["x"])
            y.append(dict["y"])

    # Get list of plot images from function regression
    img = plot_regression(x, y)

    return render_template("index.html", img=img, form_action=["/", "/dataset"])


### POINTS
@app.route("/points", methods=["GET", "POST"])
def points():
    if request.method == "POST":

        # Get points from html
        x = int(request.form.get("x"))
        y = int(request.form.get("y"))

        # Remember points in database
        db.execute("INSERT INTO points (x, y) VALUES (?, ?)", x, y)

        return redirect("/points")

    else:
        points = db.execute("SELECT * FROM points")
        return render_template("points.html", points=points, form_action=["/points", "/dataset_points"])


### DATASET POINTS
@app.route("/dataset_points", methods=["POST"])
def dataset_points():

    # Clear database
    db.execute("DELETE FROM points")

    # Insert default dataset into database
    db.execute("INSERT INTO points (x, y) VALUES (1,3), (2,12), (3,10), (4,10), (5,20), (4,20), (5,15), (10,20), (3,7), (2, 6), (8, 18), (7, 16)")

    return redirect("/points")


# DELETE POINT FROM TABLE
@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM points WHERE id = ?", id)
    return redirect("/points")


## FUNCTIONS

# Linear regression function
def linear_function (X, M, B):
    Y=M*float(X)+B
    return Y

# Plot points and default linear regression
def plot_points(x, y):

    # Starting values:
    b = 1; m = 0

    # Clear plot
    plt.clf()

    # If input values are empty:
    if x == [] and y == []:
        x_default = [0.5, 9.5]
        y_default = [linear_function(i, m, b) for i in x_default]
        plt.xlim(0, 10)
        plt.ylim(0, 10)
    else:
        x_default = [min(x), max(x)]
        y_default = [linear_function(i, m, b) for i in x_default]

        # Axis scales
        plt.xlim(0, max(x)+0.5)
        plt.ylim(0, max(y)+0.5)

    # Plot data points
    plt.plot(x, y, 'o', label="Data-Points")

    # Plot default linear curve
    plt.plot(x_default, y_default, label="Regression Curve")

    # Plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.125),
          fancybox=True, shadow=True, ncol=5)

    # Save plot as png image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    # Add image to list
    images = []
    images.append(image_base64)

    # Returns a list of one plot image for each epoch
    return images

# Plot linear regression
def plot_regression(x, y):

    # Starting Values
    b = 1; m = 0

    # Hyperparameter
    Learning_rate = 0.01
    epochs = range(0,10)

    # Images list to store plots
    images = []

    # Optimize linear regression
    for k in epochs:

        # Starting Values
        dMSE_db = 0
        dMSE_dm = 0
        MSE = 0

        # For each data point
        for i in range(0,len(x)):

            # Calculate derivatives of MSE (Mean Squared Error)
            dMSE_db = dMSE_db - 2/len(x) * (y[i] - m*x[i] - b)
            dMSE_dm = dMSE_dm - 2*x[i]/len(x) * (y[i] - m*x[i] - b)

            # Calculate y
            ys = linear_function(x[i], m, b)

            # Calculate Mean Squared Error
            MSE=MSE + 1/len(x)*(ys-y[i])**2

        # Calculate b, m
        Stepsize_b = Learning_rate * dMSE_db
        b = b - Stepsize_b
        Stepsize_m = Learning_rate * dMSE_dm
        m = m - Stepsize_m

        # Clear plot
        plt.clf()

        # Axis scales
        plt.xlim(0, max(x)+0.5)
        plt.ylim(0, max(y)+0.5)

        # Plot data points
        plt.plot(x, y, 'o', label="Data-Points")

        # Plot linear regression
        y_values = [linear_function(i, m, b) for i in x]
        plt.plot(x, y_values, label="Regression Curve")

        # Plot legend
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.125),
          fancybox=True, shadow=True, ncol=5)

        # Save plot as png image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()

        # Add image to list
        images.append(image_base64)

    # Returns a list of one plot image for each epoch
    return images