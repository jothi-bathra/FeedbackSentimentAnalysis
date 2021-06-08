from flask import Flask, make_response, request,render_template
import io
import csv
import pandas as pd
from textblob import TextBlob
import nltk
import pygal

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('input.html')

@app.route('/input', methods=["POST"])
def input():
    msg=""
    c=0
    f = request.files['filename']
    name=f.filename
    if not f:
        return "No file"

    if name[-4:]=='.csv':

        stream = io.TextIOWrapper(f.stream._file, "UTF8", newline=None)
   
        csv_input = csv.reader(stream)
        data=pd.read_csv(stream)
        print(len(data))
    
    else:
        data = pd.read_excel(f)
        print(len(data))

    feedback=list(data[data.columns[1]])
    polarity=[]
    sentiment=[]
    p=0
    n=0
    neu=0
    for a in feedback:
        pol= TextBlob(a).polarity
        if pol>0:
            sentiment.append("POSITIVE")
            p=p+1
        elif pol<0:
            sentiment.append("NEGATIVE")
            n=n+1
        else:
            sentiment.append("NEUTRAL")
            neu=neu+1

        polarity.append(pol)
      
    
    data['sentiment']=sentiment
    print(data['sentiment'])
    print(polarity)

    data.to_csv('result.csv')

    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'FEEDBACK ANALYSIS'
    results=[(p,'Positive'),(n,'Negative'),(neu,'Neutral')]
    for r in results:
        pie_chart.add(r[1], r[0])
    pie_chart.value_formatter = lambda x: "%.15f" % x
    piech=pie_chart.render_data_uri()

    html= render_template('output.html', piech=piech)
    return html
    

if __name__ == "__main__":
    app.run(debug=True)
    
