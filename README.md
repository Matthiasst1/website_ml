# Final Project: How Machines Learn
#### Video Demo:  https://youtu.be/7NOPMAHTB94
#### Welcome to the documentation of my final project: How Machines Learn! My name is Matthias Stollenwerk. I am from Cologne, Germany and I am happy to be your guide.

## Motivation

The fact that my parents keep asking me whether artificial intelligences will soon take over the world motivates me to decrease the fear towards AI by creating an understanding of how it actually works. My project "How Machines Learn" is a web-based application that uses JavaScript, Python and SQL and explains the mathematical basics of machine learning using a regression line. The regression line is a statistical tool that allows data points to be best represented when they have the smallest overall distance to the line. So, in the same way that AI robots today mimic human behaviour, the regression line mimics the data points as closely as possible.
The idea behind this project is to allow the user to interactively play with the data and ultimately gain a better understanding of AI.

## The Website

The website consists of two pages, *Plot* and *Data*. The user can access both pages via the menu below the headline. Each page contains an input form where the user can decide whether to add data points or simply use a preloaded data set. The main page *Plot* shows a graph in which an animation of the regression line approximating the data points is displayed after clicking the button **Start Machine Learning**. The second page *Points* shows all data points in a table where the user can additionally delete points to adjust the dataset.

## Under The Hood

Let's take a closer look at how the website is implemented. My project contains the html files "layout.html", "index.html" and "points.html" in the templates folder. Where "index.html" is the main page *Plot* and "points.html" is the second page *Points*. Furthermore there is a stylesheet "styles.css" in the static folder to make the web page look good, a database "datapoints.db" to store all of the data points and an "app.py" file. The "app.py" file contains six routes and three functions linear_function(), plot_points() and plot_regression(). The precise implementation of these functions will be discussed at the end of this Readme. In the following I will take a closer look at the html files Layout, Index and Points and how they are accessed via the routes in the app.py file.

### Layout

The layout contains the header with a heading and the menu that displays the two pages *Plot* and *Data*. Moreover it contains an input form where the user can add a data point or use the preloaded dataset. If the user is on the main page *Plot*, the data point will be visibly added to the graph. If the user is on the page *Data*, the data point is added visibly to the table. As these are two different actions on the same form, depending on which page the user is interacting with, a design choice is worth mentioning. In the Layout file, the form attribute action is set to a variable of either "/" or "/points“. So depending on which page the user submits the data, the layout will send it to the appropriate route in the app.py file. Finally, there's a footer on each page showing the editor's name and the CS50 course.

### Index

The Index html file contains a Button *Start Machine Learning*, an Image Container to display the graph and a Script that manages displaying the graphs.

If the user simply opens the main page or selects *Plot* from the menu, **route /** will be submitted via GET. In "app.py" **route /** retrieves the data points from datapoints.db using sql commands and passes them to the plot_points() function. It displays a graph on the web page with all available data points and a regression curve in the default position.

When a data point is added via the input form, it is submitted to **route /** via POST. In "app.py" **route /** retrieves the submitted x and y values and stores them in the database. It then redirects to **route /** and immediately adds the new datapoint to the graph. Alternatively, clicking on *Dataset* **route /dataset** is passed via POST. In app.py the existing datapoints are deleted and the pre-installed dataset is set using sql commands and stored in datapoints.db. The user is redirected to **route /** and the dataset is displayed on the graph.

When the user clicks the *Start Machine Learning* button, **route /plot** is passed via POST. In "app.py" **/plot** gets the data points from datapoints.db using sql commands and passes them to the plot_regression() function. The return value of the function is a list of plot images showing the approximation of the regression line to the data points, image by image. The list of plots is assigned to an img variable and passed to the Index file. Index.html handles the presentation of the plot images by a script. It basically defines a function display_image() that loops through the list of plot images and displays one plot after another with a delay of 1000 milliseconds. This creates an animation of the approaching regression line on the web page.

### Points

The Points html file contains a table that displays each point of the dataset.

When the user accesses *Data* via the menu, **route /points** is passed via GET. In "app.py" **route /points** retrieves the datapoints from datapoints.db via sql commands and passes them to the html file with the points variable. For each point in points, plus an additional *Delete* button, a table row is generated by a Jinja loop. Removing a data point by clicking *Delete*, **route /delete** is passed via POST. In "app.py" the data point is deleted from datapoints.db via sql commands. The user will be redirected to the page *Data*.

When a data point is added via the input form, it is submitted to **route /points** via POST. In "app.py" **route /points** retrieves the submitted x and y values and stores them in the database. It then redirects to **route /points** and immediately adds the new datapoint to the table. Alternatively, clicking on *Dataset* **route /points_dataset** is passed via POST. In app.py the existing datapoints are deleted and the pre-installed dataset is set using sql commands and stored in datapoints.db. The user is redirected to **route /points** and the dataset is displayed in the table.

### Functions

In the following, I will explain the functions I implemented to visualise the process of machine learning on the website.

#### Linear_function

The linear_function function calculates the linear function Y = M * float(X) + B and returns the value of Y.

#### Plot_points

The plot_points function takes two lists of x and y values as an input and returns a list of one single image. The image displays a graph with all the existing data points and a regression curve in default position. The function makes use of the Matplotlib package that contains a library to visualize graphs in python. Moreover the io and base64 package are used to save the graph as an image and return it.

#### Plot_regression

The plot_regression function is the main function in my project and responsible for machine learning (ML). It takes two lists of x and y values as an input and defines the linear regression in default position. The machine itself will learn to reduce the distance of the regression line to the data points.

The algorithm is described as follows: The averaged distance between the data points and the line is described by the Mean Squared Error (MSE). Accordingly, it is desired to find the minimum of the function of the MSE. The MSE is commonly referred to as the loss function. The position of the regression line is changed step by step to approach the minimum of the loss function. It is moved in small steps in the direction of the data points. This optimisation of the line position is also called optimizer gradient descent. At each iteration step, the updated position of the linear regression is plotted on the graph and then saved as an image. Finally, the function returns a list of images of the iteration steps. The images are displayed on the web page one at a time, showing the approximation of the regression line.
