from flask import Flask,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Corrected sales_data model
class SalesData(db.Model):
    ORDERNUMBER = db.Column(db.Integer, primary_key=True)
    QUANTITYORDERED = db.Column(db.Integer)
    PRICEEACH = db.Column(db.Float)
    ORDERLINENUMBER = db.Column(db.Integer)
    SALES = db.Column(db.Float)
    ORDERDATE = db.Column(db.String(50))
    STATUS = db.Column(db.String(50))
    QTR_ID = db.Column(db.Integer)
    MONTH_ID = db.Column(db.Integer)
    YEAR_ID = db.Column(db.Integer)
    PRODUCTLINE = db.Column(db.String(100))
    MSRP = db.Column(db.Integer)
    PRODUCTCODE = db.Column(db.String(50))
    CUSTOMERNAME = db.Column(db.String(255))
    PHONE = db.Column(db.String(50))
    ADDRESSLINE1 = db.Column(db.String(255))
    ADDRESSLINE2 = db.Column(db.String(255), nullable=True)
    CITY = db.Column(db.String(100))
    STATE = db.Column(db.String(50), nullable=True)
    POSTALCODE = db.Column(db.String(50), nullable=True)
    COUNTRY = db.Column(db.String(100))
    TERRITORY = db.Column(db.String(50), nullable=True)
    CONTACTLASTNAME = db.Column(db.String(100))
    CONTACTFIRSTNAME = db.Column(db.String(100))
    DEALSIZE = db.Column(db.String(50))
# Load CSV data
df = pd.read_csv("sales_data_sample.csv", encoding="ISO-8859-1")

# Insert data into SQLite
with app.app_context():
    df.to_sql("sales_data", con=db.engine, if_exists="append", index=False)

print("Data uploaded successfully!")


@app.route("/pie_chart")
def pie_chart():
    # Fetch sales data by product line
    sales = db.session.query(SalesData.PRODUCTLINE, db.func.sum(SalesData.SALES)).group_by(SalesData.PRODUCTLINE).all()
    
    if not sales:
        return jsonify({"error": "No data available"}), 404
    
    # Extract labels and values
    labels = [row[0] for row in sales]
    values = [row[1] for row in sales]

    # Generate Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['blue', 'red', 'green', 'orange', 'purple'])
    plt.title("Sales by Product Line")

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')


@app.route("/line_chart")
def line_chart():
    # Fetch sales data by product line
    sales = db.session.query(SalesData.PRODUCTLINE, db.func.sum(SalesData.SALES)).group_by(SalesData.PRODUCTLINE).all()
    
    if not sales:
        return jsonify({"error": "No data available"}), 404
    
    # Extract labels and values
    labels = [row[0] for row in sales]  # Product lines
    values = [row[1] for row in sales]  # Sales amounts

    # Generate Line Chart
    plt.figure(figsize=(8, 5))
    plt.plot(labels, values, marker='o', linestyle='-', color='blue', linewidth=2)
    plt.xlabel("Product Line")
    plt.ylabel("Total Sales")
    plt.title("Sales by Product Line (Line Chart)")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.grid(True)

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    return send_file(img, mimetype='image/png')

@app.route("/bar_chart")
def bar_chart():
    # Fetch sales data by product line
    sales = db.session.query(SalesData.PRODUCTLINE, db.func.sum(SalesData.SALES)).group_by(SalesData.PRODUCTLINE).all()
    
    if not sales:
        return jsonify({"error": "No data available"}), 404

    # Extract labels and values
    labels = [row[0] for row in sales]
    values = [row[1] for row in sales]

    # Generate Bar Chart
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=['blue', 'red', 'green', 'orange', 'purple'])
    plt.xlabel("Product Line")
    plt.ylabel("Total Sales")
    plt.title("Sales by Product Line")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
