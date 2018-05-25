from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable, Array, ComplexModel
from spyne.model.fault import Fault

import requests
import json
import os
import copy
import random

app = Flask(__name__)
spyne = Spyne(app)

ticketsDB = [
	{'ID' : '1', 'Barcode' : '78355256', 'EID' : '3', 'Current_Zone' : '0', 'Rated': '0'},
	{'ID' : '2', 'Barcode' : '', 'EID' : '5', 'Current_Zone' : '0', 'Rated': '0'},
	{'ID' : '3', 'Barcode' : '', 'EID' : '1', 'Current_Zone' : '0', 'Rated': '0'},
	{'ID' : '4', 'Barcode' : '', 'EID' : '6', 'Current_Zone' : '0', 'Rated': '0'},
	{'ID' : '5', 'Barcode' : '', 'EID' : '3', 'Current_Zone' : '0', 'Rated': '0'},
	{'ID' : '6', 'Barcode' : '', 'EID' : '2', 'Current_Zone' : '0', 'Rated': '0'},
	{'ID' : '7', 'Barcode' : '', 'EID' : '2', 'Current_Zone' : '0', 'Rated': '0'}
]


class DefaultMessage(ComplexModel):
	Message = Unicode

class Movie(ComplexModel):
	ID = Unicode
	Title = Unicode
	Release_date = Unicode
	Rating = Unicode
	Genre = Unicode

class Ticket(ComplexModel):
	ID = Unicode
	Barcode = Unicode
	EID = Unicode
	Event = Movie
	Current_Zone = Unicode
	Rated = Unicode

class Tickets(ComplexModel):
	tickets = Array(Ticket)

class TicketsService(spyne.Service):
	__soap_target_namespace__ = 'MyNS'
	__soap_server_address__ = '/soap/tickets'
	__service_url_path__ = '/soap/tickets'
	__in_protocol__ = Soap11(validator='lxml')
	__out_protocol__ = Soap11()

	@spyne.srpc(Unicode(default='Welcome'),_returns=DefaultMessage)
	def ConnectedString(str):
		if(len(str) == 0):
			return DefaultMessage(Message='Connected')
		else:
			return DefaultMessage(Message=str)

	@spyne.srpc(_returns=Array(Ticket))
	def getTickets():
		m = []
		try:
			copy_tickets = copy.deepcopy(ticketsDB)
			url = 'http://service:81/movies'
			for i in range(0, len(ticketsDB)):
				r = requests.get('{}/{}'.format(url, ticketsDB[i]['EID']))
				Event = json.loads(r.text)
				m.append(Ticket(ID=ticketsDB[i]["ID"], Barcode=ticketsDB[i]["Barcode"], EID=ticketsDB[i]["EID"], 
					Current_Zone=ticketsDB[i]["Current_Zone"], Rated=ticketsDB[i]["Rated"], 
					Event=(Movie(ID=Event[0]['ID'], Title=Event[0]['Title'], Release_date=Event[0]['Release date'], Rating=str(Event[0]['Rating']), Genre=Event[0]['Genre']))))
			return m
		except requests.RequestException as e:
			copy_tickets = copy.deepcopy(ticketsDB)
			for i in range(0, len(ticketsDB)):
				m.append(Ticket(ID=ticketsDB[i]["0"], Barcode=ticketsDB[i]["Barcode"], EID=ticketsDB[i]["EID"], 
					Current_Zone=ticketsDB[i]["Current_Zone"], Rated=ticketsDB[i]["Rated"], 
					Event=[]))
			return m


	@spyne.srpc(Unicode,_returns=Ticket)
	def getTicket(TicketID):
		try:
			ticket = [tic for tic in ticketsDB if (tic['ID'] == TicketID)]
			copy_tickets = copy.deepcopy(ticket)
			url = 'http://service:81/movies'
			movies = []
			r = requests.get('{}/{}'.format(url, copy_tickets[0]['EID']))
			Event = json.loads(r.text);
			return Ticket(ID=copy_tickets[0]["ID"], Barcode=copy_tickets[0]["Barcode"], EID=copy_tickets[0]["EID"], 
					Current_Zone=copy_tickets[0]["Current_Zone"], Rated=copy_tickets[0]["Rated"], 
					Event=(Movie(ID=Event[0]['ID'], Title=Event[0]['Title'], Release_date=Event[0]['Release date'], Rating=str(Event[0]['Rating']), Genre=Event[0]['Genre'])))
		except requests.RequestException as e:
			ticket = [tic for tic in copy_tickets[0] (tic['ID'] == TicketID)]
			return (Ticket(ID=copy_tickets[0]["0"], Barcode=copy_tickets[0]["Barcode"], EID=copy_tickets[0]["EID"], 
					Current_Zone=copy_tickets[0]["Current_Zone"], Rated=copy_tickets[0]["Rated"], 
					Event=[]))

	@spyne.srpc(Unicode,_returns=Array(Ticket))
	def getEventTickets(EventID):
		EventTickets = [ tic for tic in ticketsDB if (tic['EID'] == EventID)]
		m = []
		for ticket in EventTickets:
			m.append(Ticket(ID=ticket["ID"], Barcode=ticket["Barcode"], EID=ticket["EID"], Current_Zone=ticket["Current_Zone"], Rated=ticket["Rated"]))
		return m

	@spyne.srpc(Unicode,_returns=Ticket)
	def DeleteTicket(TicketID):
		ticket = [tic for tic in ticketsDB if (tic['ID'] == TicketID)]
		if (len(ticket) == 0):
			abort(404)
		if (ticket[0]['Barcode'] == ''):
			ticketsDB.remove(ticket[0])
			return (Ticket(ID=ticket[0]["ID"], Barcode=ticket[0]["Barcode"], EID=ticket[0]["EID"], Current_Zone=ticket[0]["Current_Zone"], Rated=ticket[0]["Rated"]))
		else:
			raise Fault(faultcode='Client', faultstring='NotAllowed', faultactor='', detail={'Message':'Error Ticket has a barcode generated and cannot be deleted'})

	@spyne.srpc(Unicode(default=''),Unicode(default=''), Unicode(default=''), Unicode(default=''),_returns=Ticket)
	def EditTicket(TicketID, EventID, Barcode, Current_Zone):
		ticket = [tic for tic in ticketsDB if (tic['ID'] == TicketID)]
		if (len(ticket) == 0):
			abort(404)
		if (len(EventID) != 0):
			ticket[0]['EID'] = EventID
		if (len(Current_Zone) != 0):
			ticket[0]['Current_Zone'] = Current_Zone
		if (len(Barcode) != 0):
			ticket[0]['Barcode'] = Barcode
		return (Ticket(ID=ticket[0]["ID"], Barcode=ticket[0]["Barcode"], EID=ticket[0]["EID"], Current_Zone=ticket[0]["Current_Zone"], Rated=ticket[0]["Rated"]))

	@spyne.srpc(Unicode,_returns=Ticket)
	def generateTicket(TicketID):
		randomBarcode = random.randint(10000000,100000000)
		ticket = [tic for tic in ticketsDB if (tic['ID'] == TicketID)]
		if(ticket[0]['Barcode'] == ''):
			ticket[0]['Barcode']  = randomBarcode
			return (Ticket(ID=ticket[0]["ID"], Barcode=ticket[0]["Barcode"], EID=ticket[0]["EID"], Current_Zone=ticket[0]["Current_Zone"], Rated=ticket[0]["Rated"]))
		else:
			raise Fault(faultcode='Client', faultstring='NotAllowed', faultactor='', detail={'Message':'Error Ticket has a barcode generated and cannot be created'})

	@spyne.srpc(Unicode,_returns=Array(Ticket))
	def generateEventTickets(EventID):
		ticket = [tic for tic in ticketsDB if (tic['EID'] == EventID)]
		m = []
		for eventsTic in ticket:
			if(eventsTic['Barcode'] == ''):
				randomBarcode = random.randint(100000,1000000)
				eventsTic['Barcode']  = randomBarcode
				m.append(Ticket(ID=eventsTic["ID"], Barcode=eventsTic["Barcode"], EID=eventsTic["EID"], Current_Zone=eventsTic["Current_Zone"], Rated=eventsTic["Rated"]))
		return m

	@spyne.srpc(Unicode, Integer,_returns=Array(Ticket))
	def addTicketToEvent(MovieName, NumberOfTickets):
		try:
			if(len(MovieName) == 0):
				raise Fault(faultcode='Client', faultstring='', faultactor='', detail={'Message':'Error. Title not provided or is invalid'})
			if(NumberOfTickets < 1):
				raise Fault(faultcode='Client', faultstring='', faultactor='', detail={'Error. TicNumber not provided or is invalid'})
			requestData = {'title' : MovieName}
			r = requests.get('http://service:81/movies', params=requestData)
			eventID = r.json()
			for i in range(0,NumberOfTickets):
				lastId = int(ticketsDB[len(ticketsDB) - 1]['ID']) + 1
				ticket = {
					'ID': str(lastId),
					'Barcode': '',
					'EID' : eventID[0]['ID'],
					'Current_Zone': '0',
					'Rated': '0'
				}
				ticketsDB.append(ticket)
			eventTickets = [ tic for tic in ticketsDB if (tic['EID'] == str(eventID[0]['ID']))]
			m = []
			for ticket in eventTickets:
				m.append(Ticket(ID=ticket["ID"], Barcode=ticket["Barcode"], EID=ticket["EID"], Current_Zone=ticket["Current_Zone"], Rated=ticket["Rated"]))
			return m
		except requests.RequestException as e:
			raise Fault(faultcode='503', faultstring='', faultactor='', detail={'Message':str(e)})

	@spyne.srpc(Unicode, Unicode,_returns=Movie)
	def addRatingToEvent(TicketID, Rating):
		if(len(TicketID) == 0):
			raise ValueError('Error. TicketID not provided or is invalid')

		ticket = [tic for tic in ticketsDB if (tic['ID'] == TicketID)]
		
		if(ticket[0]['Rated'] == "1"):
			raise ValueError('Error. Ticket already participated in rating')
		data = {
			"Rating": Rating
		}
		url = 'http://service:81/movies'
		r = requests.patch('{}/{}'.format(url, ticket[0]['EID']), json=data)
		if(r.status_code==200):
			ticket[0]['Rated'] = "1"
			Event =  r.json()
			return (Movie(ID=Event['ID'], Title=Event['Title'], Release_date=Event['Release date'], Rating=str(Event['Rating']), Genre=Event['Genre']))

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
