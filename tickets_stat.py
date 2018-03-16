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
	return jsonify({'Current Tickets: ':ticketsDB})

# GET information about current Event Tickets in JSON format
@app.route('/event/<eventID>/tickets', methods=['GET'])
def getCurrentTicketsByEvent(eventID):
	eventTickets = [ tic for tic in ticketsDB if (tic['Event No'] == eventID)]
	return eventTickets


# PUT a barcode to the specific Ticket ID. Id provided by URL
@app.route('/tickets/<ticketID>/barcode', methods=['PUT'])
def generateTicket(ticketID):
	randomBarcode = random.randint(10000000,100000000)
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if(ticket[0]['Barcode'] == ''):
		ticket[0]['Barcode']  = randomBarcode
		return ticket[0]
	else:
		return jsonify({'Response': 'Ticket has a barcode'})

# PUT a barcode to specific Event Tickets. Event Id provided by URL
@app.route('/events/<EventID>/tickets/barcode', methods=['PUT'])
def generateEventTicket(EventID):
	ticket = [tic for tic in ticketsDB if (tic['Event No'] == EventID)]
	for eventsTic in ticket:
		if(eventsTic['Barcode'] == ''):
			randomBarcode = random.randint(100000,1000000)
			eventsTic['Barcode']  = randomBarcode
	return ticket

#Scan ticket IN, parameters passed by JSON - ticket id - string, barcode - int
@app.route('/tickets/in', methods=['PUT'])
def scanIN():
	ticket = [tic for tic in ticketsDB if (tic['Barcode'] == request.json['Barcode'] and
										   tic['id'] == request.json['id'])]
	if(ticket[0]['Current Zone'] == '0'):
		ticket[0]['Current Zone'] = '1'
		return ticket[0]
	else:
		return jsonify({'Response': 'Ticket can not be scanned'})

#Scan ticket OUT, parameters passed by JSON - ticket id - string, barcode - int
@app.route('/tickets/out', methods=['PUT'])
def scanOUT():
	ticket = [tic for tic in ticketsDB if (tic['Barcode'] == request.json['Barcode'] and
										   tic['id'] == request.json['id'])]
	if(ticket[0]['Current Zone'] == '1'):
		ticket[0]['Current Zone'] = '0'
		return ticket[0]
	else:
		return jsonify({'Response': 'Ticket can not be scanned'})


# POST - Add ne Ticket to the Event. Event ID passed by JSON. Ticket ID is auto increasing.
@app.route('/tickets/new', methods = ['POST'])
def addTicket():
	lastId = int(ticketsDB[len(ticketsDB)-1]['id']) + 1
	ticket = {
		'id': lastId,
		'Barcode': '',
		'Event No' :request.json['Event No'],
		'Current Zone': '0'
	}
	ticketsDB.append(ticket)
	return ticket

# DELETE - Remove ticket from the list.
# Only when the barcode is not generated
@app.route('/tickets/remove/<ticketID>', methods = ['DELETE'])
def deleteTicket(ticketID):
	ticket = [tic for tic in ticketsDB if (tic['id'] == ticketID)]
	if (ticket[0]['Barcode'] == ''):
		ticketsDB.remove(ticket[0])
		return ticket[0]
	else:
		return jsonify(
			{'Response': 'Ticket is generated and can not be deleted'})

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')

