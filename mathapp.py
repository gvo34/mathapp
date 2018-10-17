# Application - 'math api'
# Implement a web service (preferably in Go, Python, Ruby or Java; extra effort to do that in 
# Go will be recognised; using a framework or not):
# /min - given list of numbers and a quantifier (how many) provides min number(s)
# /max - given list of numbers and a quantifier (how many) provides max number(s)
# /avg - given list of numbers calculates their average 
# /median - given list of numbers calculates their median
# /percentile - given list of numbers and quantifier 'q', compute the qth percentile of the list elements
# No need to be concerned with resources, we're assuming there's plenty enough of memory, etc.

import numpy as np
from flask import Flask, jsonify, render_template, request, json

errorMessages = [
    "<b>Error collecting input: format expected is <i>'Q:array'</i>, where <i>Q</i> is a quantifier interger value and <i>array</i> is a comma separated list of numbers</b>",
    "<b>Error collecting input: format expected is <i>'array'</i> as a comma separated list of numbers</b>"]


app = Flask(__name__)

def getMinOrMax(numbers, quantifier, isMin):
    '''
    getMinOrMax
    numbers: list of numbers
    count: determine how many borders to retrieve
    isMin: True if computing the min otherwise computes the max
    '''
    minormax = ""
    if quantifier >= len(numbers):
        return ''.join([str(x)+' ' for x in numbers])

    for i in range(quantifier):
        if isMin:
            value = min(numbers)
        else:
            value = max(numbers)     
        numbers.remove(value)   
        minormax = minormax + str(value) + " "
    return minormax

@app.route('/min',)
def getminentry():
    return errorMessages[0]


@app.route('/min/<values>')
def getmin(values):
    if hasattr(values, 'response'):
        # expected jsonify of dictionary of the form {'numbers': [1,2,3,4,5], 'quantifier': 2}
        r = json.loads(values.response[0])
        minimums = getMinOrMax(r['numbers'], r['quantifier'], True)
        return "The "+ str(r['quantifier']) + " Min value(s): " +  minimums 
    else:
        try:
            # expected string with format 1:1,2,3,4,5
            strings = values.split(":")
            quantifier = int(strings[0])
            array = list(map(int,strings[1].split(','))) 
            minimums = getMinOrMax(array, quantifier, True)
            return "The "+ str(quantifier) + " Min values(s): " +  minimums 
        except:
            return errorMessages[0]


@app.route('/max',)
def getmaxentry():
    return errorMessages[0]

    
@app.route('/max/<values>')
def getmax(values):
    if hasattr(values, 'response'):
        # expected jsonify of dictionary of the form {'numbers': [1,2,3,4,5], 'quantifier': 2}
        r = json.loads(values.response[0])
        maximums = getMinOrMax(r['numbers'], r['quantifier'], False)
        return "The "+ str(r['quantifier']) + " Max value(s): " +  maximums
    else:
        try:
            # expected string with format 1:1,2,3,4,5
            strings = values.split(":")
            quantifier = int(strings[0])
            array = list(map(int,strings[1].split(','))) 
            maximums = getMinOrMax(array, quantifier, False)
            return "The "+ str(quantifier) + " Max value(s): "+  maximums 
        except:
            return errorMessages[0]
    

@app.route('/avg',)
def getavgentry():
    return errorMessages[1]

@app.route('/avg/<values>')
def getavg(values):
    if hasattr(values, 'response'):
        # expected jsonify of dictionary of the form {'numbers': [1,2,3,4,5]}
        r = json.loads(values.response[0])
        average_value = np.average(r['numbers'])
        return "The Average: " +  str(average_value)
    else:
        try:
            # expected string with format 1:1,2,3,4,5
            array = list(map(int,values.split(','))) 
            average_value = np.average(array)
            return "The Average: " +  str(average_value)
        except:
            return errorMessages[1]


@app.route('/median',)
def getmedianentry():
    return errorMessages[1]

@app.route('/median/<values>')
def getmed(values):
    if hasattr(values, 'response'):
        # expected jsonify of dictionary of the form {'numbers': [1,2,3,4,5]}
        r = json.loads(values.response[0])
        median_value = np.median(r['numbers'])
        return "The Median: " +  str(median_value)
    else:
        try:
            # expected string with format 1:1,2,3,4,5
            array = list(map(int,values.split(','))) 
            median_value = np.median(array)
            return "The Median: " +  str(median_value)
        except:
            return errorMessages[1]



@app.route('/percentile',)
def getpercentileentry():
    return errorMessages[0]

@app.route('/percentile/<values>')
def getpercentile(values):
    if hasattr(values, 'response'):
        # expected jsonify of dictionary of the form {'numbers': [1,2,3,4,5], 'quantifier': 2}
        r = json.loads(values.response[0])
        percentile_value = np.percentile(r['numbers'],r['quantifier'])
        return "The "+ str(r['quantifier']) + " Percentile:  " +  str(percentile_value) 
    else:
        try:
            # expected string with format 1:1,2,3,4,5
            strings = values.split(":")
            quantifier = int(strings[0])
            array = list(map(int,strings[1].split(','))) 
            percentile_value = np.percentile(array, quantifier)
            return "The "+ str(quantifier) + " Percentile: " +  str(percentile_value) 
        except:
            return errorMessages[0]

     

@app.route('/', methods=['GET', 'POST'])
def index():    
    
    if request.method == 'POST':
        try:
            listnumber = request.form['arraynumber']
            numbers = list(map(int,listnumber.split(',')))
            quantifier = request.form['quantifier']
            howmany = int(quantifier)
            
            values = {'numbers':numbers, 'quantifier':howmany}
            
        except:
            return errorMessages[0]
        
        # selected service via user button submit
        if 'max_button' in request.form:
            return getmax(jsonify(values))
        elif 'min_button' in request.form:
            return getmin(jsonify(values))
        elif 'avg_button' in request.form:
            return getavg(jsonify(values))
        elif 'med_button' in request.form:
            return getmed(jsonify(values))
        elif 'per_button' in request.form:
            return getpercentile(jsonify(values))
        else:
            return "Error obtaining request form"
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    app.run() 

