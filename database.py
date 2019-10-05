import sqlite3

def createConnection(db_file):
	connection = None
	try:
		connection = sqlite3.connect(db_file)
	except Exception as error:
		print(error)

	return connection

def createTable(db_file, name, structure):
	db = createConnection(db_file)
	cursor = db.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS {0} ({1})".format(name, structure))
	db.commit()
	db.close()

def getQuery(db_file, query):
	db = createConnection(db_file)
	cursor = db.cursor()
	cursor.execute(query)
	content = cursor.fetchall()
	db.close()
	return content

def setQuery(db_file, query):
	db = createConnection(db_file)
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	db.close()