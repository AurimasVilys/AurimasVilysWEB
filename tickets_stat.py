from flask import Flask
from flask import request
from flask import jsonify

import random

app = Flask(__name__)

ticketsDB = [
	{'id' : '1', 'Barcode' : '', 'Event No' : '21', 'Current Zone' : '0'},
	{'id' : '2', 'Barcode' : '', 'Event No' : '43', 'Current Zone' : '0'},
	{'id' : '3', 'Barcode' : '', 'Event No' : '23', 'Current Zone' : '0'},
	{'id' : '4', 'Barcode' : '', 'Event No' : '43', 'Current Zone' : '0'},
	{'id' : '5', 'Barcode' : '', 'Event No' : '44', 'Current Zone' : '0'},
	{'id' : '6', 'Barcode' : '', 'Event No' : '77', 'Current Zone' : '0'},
	{'id' : '7', 'Barcode' : '', 'Event No' : '21', 'Current Zone' : '0'}
]

@app.route('/')
def hello():
	return 'You have connected to Tickets Stats'



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
		return 'Error. Ticket has a barcode generated'

# PUT a barcode to specific Event Tickets. Event Id provided by URL
@app.route('/events/<eventID>/tickets', methods=['PATCH'])
def generateEventTicket(eventID):
	ticket = [tic for tic in ticketsDB if (tic['Event No'] == eventID)]
	for eventsTic in ticket:
		if(eventsTic['Barcode'] == ''):
			randomBarcode = random.randint(100000,1000000)
			eventsTic['Barcode']  = randomBarcode
	return jsonify(ticket)

#PATCH update info (only Event No)
@app.route('/tickets/<ticketID>', methods=['PUT'])
def changeEvent(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if 'Event No' in request.json:
		ticket[0]['Event No'] = request.json['Event No']
	if 'Current Zone' in request.json:
		ticket[0]['Current Zone'] = request.json['Current Zone']
	return jsonify(ticket[0])

# POST - Add ne Ticket to the Event. Event ID passed by JSON. Ticket ID is auto increasing.
@app.route('/tickets', methods = ['POST'])
def addTicket():
	lastId = int(ticketsDB[len(ticketsDB) - 1]['id']) + 1
	ticket = {
		'id': str(lastId),
		'Barcode': '',
		'Event No' :request.json['Event No'],
		'Current Zone': '0'
	}
	ticketsDB.append(ticket)
	return jsonify(ticket), 201

# DELETE - Remove ticket from the list.
# Only when the barcode is not generated
@app.route('/tickets/<ticketID>', methods = ['DELETE'])
def deleteTicket(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if (ticket[0]['Barcode'] == ''):
		ticketsDB.remove(ticket[0])
		return jsonify(ticket[0]), 200
	else:
		return 'Error. Ticket has a barcode generated and cannot be deleted'

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')

