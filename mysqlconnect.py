from flask import Flask, redirect, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    database="forest",
    user="root",
    password=""
)

# Define the route for the home page 
# Also display existing data from database
@app.route('/')
def index():
    cursor = conn.cursor()

    # Fetch data from tree_data table
    data = 'SELECT * FROM tree_data ORDER BY update_at DESC LIMIT 10'
    cursor.execute(data)
    keepData = cursor.fetchall() #nanti keepData tukar kpd tree_data

    # Fetch data from stand_table table
    stand_query = 'SELECT * FROM stand_table'
    cursor.execute(stand_query)
    stand_data = cursor.fetchall()
    
    return render_template('form.html', data = keepData, stand_data=stand_data)




# A. INSERT NEW DATA TO DATABASE 
# Define the route for form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get form data from the request
        block_x = request.form['block_x']
        block_y = request.form['block_y']
        coordinate_x = request.form['coordinate_x']
        coordinate_y = request.form['coordinate_y']
        tree_number = request.form['tree_number']
        specode = request.form['specode']
        species_group = request.form['species_group']
        diameter_cm = request.form['diameter_cm']
        diameter_class = request.form['diameter_class']
        height_m = request.form['height_m']
        volume_m3 = request.form['volume_m3']
        status = request.form['status']
        

        # Insert form data into the database
        cursor = conn.cursor()
        insert_query = "INSERT INTO tree_data (Block_X, Block_Y, Coordinate_X, Coordinate_Y, Tree_Number, SPECODE, SPECIES_GROUP, Diameter_cm, Diameter_Class, Height_m, Volume_m3, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (block_x, block_y, coordinate_x, coordinate_y, tree_number, specode, species_group, diameter_cm, diameter_class, height_m, volume_m3, status))
        conn.commit()
        cursor.close()

        # Return success message  
        # return 'Data inserted successfully!'  # direct URL
    
        # success submitted, redirect / go to other default page
        return redirect ('/')  # redirect 

    # If the request method is not POST, return method not allowed
    return 'Method Not Allowed'

if __name__ == '__main__':
    # Run the Flask application using Gunicorn
    app.run(host='127.0.0.1', port=5500)  # set Gunicorn server/WSGI server port same with Live Server Port at 5500 -> To get runnning in backend and bootstrap running displaying




    
