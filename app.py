from flask import Flask, request, jsonify,  render_template
import mysql.connector
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def new_artist():
	return render_template('info.html')

@app.route('/artists', methods=['GET'])
def get_artists():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="arts",
    auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM artists')
    rows = mycursor.fetchall()
    artists = []
    for row in rows:
        artist = {}
        artist['id'] = row[0]
        artist['name'] = row[1]
        artist['description'] = row[2]
        artist['email'] = row[3]
        artists.append(artist)
    mydb.close()
    return jsonify(artists)

@app.route('/artists', methods=['POST'])
def create_artist():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="arts",
    auth_plugin='mysql_native_password'
    )
    id = str(uuid.uuid4())
    name = request.form['name']
    email = request.form['email']
    description = request.form['description']
    mycursor = mydb.cursor()
    mycursor.execute('INSERT INTO artists (id, name, description, email) VALUES (%s, %s, %s, %s)', (id, name,description,email))
    mydb.commit()
    mycursor.close()
    return jsonify({'message': 'Artist added successfully'})


if __name__ == '__main__':
    app.run(debug=True)
