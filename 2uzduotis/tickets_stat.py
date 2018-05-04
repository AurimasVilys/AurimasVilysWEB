from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import requests
import json
import os
import copy
import random

app = Flask(__name__)

ticketsDB = [
	{'id' : '1', 'Barcode' : '78355256', 'Event No' : '3', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '2', 'Barcode' : '', 'Event No' : '5', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '3', 'Barcode' : '', 'Event No' : '1', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '4', 'Barcode' : '', 'Event No' : '6', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '5', 'Barcode' : '', 'Event No' : '3', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '6', 'Barcode' : '', 'Event No' : '2', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '7', 'Barcode' : '', 'Event No' : '2', 'Current Zone' : '0', 'Rated': '0'}
]

@app.route('/')
def hello():
	return 'Connected'

# 1ST TASK

# GET information about current Tickets in JSON format
@app.route('/tickets', methods=['GET'])
def getCurrentTickets():
	return jsonify(ticketsDB)

# GET information about single Ticket in JSON format
@app.route('/tickets/<ticketID>', methods=['GET'])
def getSingleTicket(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	return jsonify(ticket[0])

# GET information about current Event Tickets in JSON format
@app.route('/events/<eventID>/tickets', methods=['GET'])
def getCurrentTicketsByEvent(eventID):
	eventTickets = [ tic for tic in ticketsDB if (tic['Event No'] == eventID)]
	return jsonify(eventTickets)


# PUT a barcode to the specific Ticket ID. Id provided by URL
@app.route('/tickets/<ticketID>', methods=['PATCH'])
def generateTicket(ticketID):
	randomBarcode = random.randint(10000000,100000000)
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if(ticket[0]['Barcode'] == ''):
		ticket[0]['Barcode']  = randomBarcode
		return jsonify(ticket[0])
	else:
		return 'Error. Ticket has a barcode generated', 405

# PUT a barcode to specific Event Tickets. Event Id provided by URL
@app.route('/events/<eventID>/tickets', methods=['PATCH'])
def generateEventTicket(eventID):
	ticket = [tic for tic in ticketsDB if (tic['Event No'] == eventID)]
	for eventsTic in ticket:
		if(eventsTic['Barcode'] == ''):
			randomBarcode = random.randint(100000,1000000)
			eventsTic['Barcode']  = randomBarcode
	return jsonify(ticket)

#PUT update info (only Event No)
@app.route('/tickets/<ticketID>', methods=['PUT'])
def changeEvent(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if (len(ticket) == 0):
		abort(404)
	if 'Event No' in request.json:
		ticket[0]['Event No'] = request.json['Event No']
	if 'Current Zone' in request.json:
		ticket[0]['Current Zone'] = request.json['Current Zone']
	if 'Barcode' in request.json:
		ticket[0]['Barcode'] = request.json['Barcode']
	return jsonify(ticket[0])

# POST - Add one Ticket to the Event. Event ID passed by JSON. Ticket ID is auto increasing.
@app.route('/tickets', methods = ['POST'])
def addTicket():
	lastId = int(ticketsDB[len(ticketsDB) - 1]['id']) + 1
	ticket = {
		'id': str(lastId),
		'Barcode': '',
		'Event No' :request.json['Event No'],
		'Current Zone': '0',
		'Rated': '0'
	}
	ticketsDB.append(ticket)
	return jsonify(ticket), 201

# DELETE - Remove ticket from the list.
# Only when the barcode is not generated
@app.route('/event/<ticketID>', methods = ['DELETE'])
def deleteTicket(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if (len(ticket) == 0):
		abort(404)
	if (ticket[0]['Barcode'] == ''):
		ticketsDB.remove(ticket[0])
		return jsonify(ticket[0]), 200
	else:
		return 'Error. Ticket has a barcode generated and cannot be deleted', 405

#2nd TASK

# GET info about all events(movies)
@app.route('/events', methods=['GET'])
def getEvents():
	r = requests.get('http://service:81/movies')
	return r.text

# POST - Add selected amount of tickets to the selected event. 
#Amount of tickets, event(film) id passed by JSON. String and int
@app.route('/events/tickets', methods = ['POST'])
def addTicketToEvent():
	if(request.args.get('embedded', '') == "movie"):
		movie = request.json['Movie']
		numberOfTickets = request.json['TicNumber']
		r = requests.post('http://service:81/movies', json = {"Title" : movie['Title'], "Release date" : movie['Release_date'], "Rating" : movie['Rating'], "Genre" : movie['Genre']})
		r = json.loads(r.text)
		for i in range(0,numberOfTickets):
			lastId = int(ticketsDB[len(ticketsDB) - 1]['id']) + 1
			ticket = {
				'id': str(lastId),
				'Barcode': '',
				'Event No' : r['ID'],
				'Current Zone': '0',
				'Rated': '0'
			}
			ticketsDB.append(ticket)
		eventTickets = [ tic for tic in ticketsDB if (tic['Event No'] == r['ID'])]
		return jsonify(eventTickets), 201
	else:
		filmTitle = request.json['Title']
		if(len(filmTitle) == 0):
			return 'Error. Title not provided or is invalid', 405
		numberOfTickets = request.json['TicNumber']
		if(numberOfTickets < 1):
			return 'Error. TicNumber not provided or is invalid', 405
		requestData = {'title' : filmTitle}
		r = requests.get('http://service:81/movies', params=requestData)
		eventID = r.json()
		for i in range(0,numberOfTickets):
			lastId = int(ticketsDB[len(ticketsDB) - 1]['id']) + 1
			ticket = {
				'id': str(lastId),
				'Barcode': '',
				'Event No' : eventID[0]['ID'],
				'Current Zone': '0',
				'Rated': '0'
			}
			ticketsDB.append(ticket)
		eventTickets = [ tic for tic in ticketsDB if (tic['Event No'] == str(eventID[0]['ID']))]
		return jsonify(eventTickets), 201

# PATCH. Rate film using TicketID. TicketID and Rating passed by json (both as strings)
@app.route('/events/rate', methods = ['PATCH'])
def addRatingToEvent():
	ticketID = request.json['Ticket ID']
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if(len(ticketID) == 0):
		return 'Error. TicketID not provided or is invalid', 405
	if(ticket[0]['Rated'] == "1"):
		return 'Error. Ticket already participated in rating', 405
	data = {
		"Rating": request.json['Rating']
	}
	url = 'http://service:81/movies'
	r = requests.patch('{}/{}'.format(url, ticket[0]['Event No']), json=data)
	if(r.status_code==200):
		ticket[0]['Rated'] = "1"
		return r.text, 200
	return r.text, 404


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
