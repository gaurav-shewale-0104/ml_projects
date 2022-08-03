
from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import pickle
import numpy as np
from sklearn.utils import resample

app = Flask(__name__)

###### MYSQL Configuration 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'iris_db'

mysql = MySQL(app)

with open("linear_reg_model.pkl","rb") as model_file:
    model = pickle.load(model_file)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods = ["GET","POST"])
def predict():
    data = request.form
    print(data)

    
    
    sepalwidth_data = float(request.form["sepalwidth"])
    petallength_data= float(request.form["petallength"])
    petalwidth_data = float(request.form["petalwidth"])
    species_data = float(request.form["species"])
    
    array = [(sepalwidth_data,petallength_data,petalwidth_data,species_data)]
    SepalLengthCm = model.predict(array)
    print("SepalLengthCm == ",SepalLengthCm)


    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS iris_tb1(sepalwidth VARCHAR(10),petallength VARCHAR(10),petalwidth VARCHAR(10),species VARCHAR(10),sepallenghth VARCHAR(50))'
    cursor.execute(query)

    cursor.execute('INSERT INTO iris_tb1(sepalwidth,petallength,petalwidth,species,sepallenghth) VALUES(%s,%s,%s,%s,%s)',(sepalwidth_data,petallength_data,petalwidth_data,species_data,SepalLengthCm))

    mysql.connection.commit()
    cursor.close()


    return render_template("display.html",Sepal_Length=SepalLengthCm)


if __name__ == "__main__":
    app.run(host="127.0.0.1",port="5000",debug=True)