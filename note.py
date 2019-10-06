import uuid
import time
import database

ENUMS = {
	"NOTE_DATABASE_FILE": "data/notes",
	"NOTE_TABLE_NAME": "notes"
}

notes = {}
database.createTable(ENUMS["NOTE_DATABASE_FILE"], ENUMS["NOTE_TABLE_NAME"], "uid TEXT NOT NULL PRIMARY KEY, content TEXT, timestamp sqlite3_uint64")

class Note:
	def __init__(self, content, timestamp=time.time(), uid=uuid.uuid4(), exists=False):
		self.uid = uid
		self.content = content
		self.timestamp = timestamp

		if not exists:
			database.setQuery(ENUMS["NOTE_DATABASE_FILE"], "INSERT INTO {0} VALUES ('{1}', '{2}', {3})".format(ENUMS["NOTE_TABLE_NAME"], self.getUID(), self.getContent(), self.getTimestamp()))

		notes[self.getUID()] = self

	def delete(self):
		uid = self.getUID()
		notes.pop(uid)
		database.setQuery(ENUMS["NOTE_DATABASE_FILE"], "DELETE FROM {0} WHERE uid = '{1}'".format(ENUMS["NOTE_TABLE_NAME"], uid))
		del self

	def getUID(self):
		return self.uid

	def getContent(self):
		return self.content

	def setContent(self, content):
		self.content = content
		database.setQuery(ENUMS["NOTE_DATABASE_FILE"], "UPDATE {0} SET content = '{1}' WHERE id = {2}".format(ENUMS["NOTE_TABLE_NAME"], self.getContent(), self.getUID()))

	def getTimestamp(self):
		return self.timestamp


def getAllNotes():
	return notes

def restoreNotes():
	db_notes = database.getQuery(ENUMS["NOTE_DATABASE_FILE"], "SELECT * FROM {0}".format(ENUMS["NOTE_TABLE_NAME"]))
	for note in db_notes:
		Note(content=note[1], timestamp=note[2], uid=note[0], exists=True)

restoreNotes()
