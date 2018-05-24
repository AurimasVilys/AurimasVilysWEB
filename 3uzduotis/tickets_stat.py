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
	{'id' : '1', 'Barcode' : '78355256', 'EID' : '3', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '2', 'Barcode' : '', 'EID' : '5', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '3', 'Barcode' : '', 'EID' : '1', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '4', 'Barcode' : '', 'EID' : '6', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '5', 'Barcode' : '', 'EID' : '3', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '6', 'Barcode' : '', 'EID' : '2', 'Current Zone' : '0', 'Rated': '0'},
	{'id' : '7', 'Barcode' : '', 'EID' : '2', 'Current Zone' : '0', 'Rated': '0'}
]

@app.route('/')
def hello():
	return 'Connected'

# 1ST TASK

# GET information about current Tickets in JSON format
@app.route('/tickets', methods=['GET'])
def getCurrentTickets():
	if(request.args.get('embedded', '') == "events"):
		try:
			copy_tickets = copy.deepcopy(ticketsDB)
			url = 'http://service:81/movies'
			movies = []
			for i in range(0, len(ticketsDB)):
				r = requests.get('{}/{}'.format(url, ticketsDB[i]['EID']))
				r = json.loads(r.text)
				movies.append(r)
				copy_tickets[i]['Event'] = []
				copy_tickets[i]['Event'].append(movies[i])
			return jsonify(copy_tickets)
		except requests.RequestException as e:
			copy_tickets = copy.deepcopy(ticketsDB)
			for i in range(0, len(ticketsDB)):
				copy_tickets[i]['Event'] = []
			return jsonify(copy_tickets)
	else:	
		return jsonify(ticketsDB)

# GET information about single Ticket in JSON format
@app.route('/tickets/<ticketID>', methods=['GET'])
def getSingleTicket(ticketID):
	if(request.args.get('embedded', '') == "events"):
		try:
			ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
			copy_tickets = copy.deepcopy(ticket)
			url = 'http://service:81/movies'
			movies = []
			for EID in copy_tickets[0]['EID']:
				r = requests.get('{}/{}'.format(url, EID))
				r = json.loads(r.text)
				movies.append(r)
			copy_tickets[0]['Event'] = []
			copy_tickets[0]['Event'].append(movies)
			return jsonify(copy_tickets)
		except requests.RequestException as e:
			copy_tickets = copy.deepcopy(ticketsDB)
			for i in range(0, len(ticketsDB)):
				copy_tickets[i]['Event'] = []
			return jsonify(copy_tickets)
	else:
		ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	return jsonify(ticket[0])

# GET information about current Event Tickets in JSON format
@app.route('/events/<eventID>/tickets', methods=['GET'])
def getCurrentTicketsByEvent(eventID):
	eventTickets = [ tic for tic in ticketsDB if (tic['EID'] == eventID)]
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
	ticket = [tic for tic in ticketsDB if (tic['EID'] == eventID)]
	for eventsTic in ticket:
		if(eventsTic['Barcode'] == ''):
			randomBarcode = random.randint(100000,1000000)
			eventsTic['Barcode']  = randomBarcode
	return jsonify(ticket)

#PUT update info (only EID)
@app.route('/tickets/<ticketID>', methods=['PUT'])
def changeEvent(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if (len(ticket) == 0):
		abort(404)
	if 'EID' in request.json:
		ticket[0]['EID'] = request.json['EID']
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
		'EID' :request.json['EID'],
		'Current Zone': '0',
		'Rated': '0'
	}
	ticketsDB.append(ticket)
	return jsonify(ticket), 201

# DELETE - Remove ticket from the list.
# Only when the barcode is not generated
@app.route('/tickets/<ticketID>', methods = ['DELETE'])
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
	try:
		r = requests.get('http://service:81/movies')
		return r.text
	except requests.RequestException as e:
		print(e)
		return str(e), 503
	return jsonify(404)

# POST - Add selected amount of tickets to the selected event. 
#Amount of tickets, event(film) id passed by JSON. String and int
@app.route('/events/tickets', methods = ['POST'])
def addTicketToEvent():
	try:
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
					'EID' : r['ID'],
					'Current Zone': '0',
					'Rated': '0'
				}
				ticketsDB.append(ticket)
			eventTickets = [ tic for tic in ticketsDB if (tic['EID'] == r['ID'])]
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
					'EID' : eventID[0]['ID'],
					'Current Zone': '0',
					'Rated': '0'
				}
				ticketsDB.append(ticket)
			eventTickets = [ tic for tic in ticketsDB if (tic['EID'] == str(eventID[0]['ID']))]
			return jsonify(eventTickets), 201
	except requests.RequestException as e:
		print(e)
		return str(e), 503
	return jsonify(404)

# PATCH. Rate film using TicketID. TicketID and Rating passed by json (both as strings)
@app.route('/events/rates', methods = ['PATCH'])
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
	r = requests.patch('{}/{}'.format(url, ticket[0]['EID']), json=data)
	if(r.status_code==200):
		ticket[0]['Rated'] = "1"
		return r.text, 200
	return r.text, 404


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
