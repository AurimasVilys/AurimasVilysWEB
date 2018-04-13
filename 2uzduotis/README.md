# Ticket Stats

### Running
You need to have docker and docker-compose installed.
To build and run:

1. docker-compose build

2. docker-compose up -d

Used ports are 5000 and 81


### Queries 1FS TASK:
1. [GET] Get all tickets -> http://localhost:5000/tickets
2. [GET] Get single ticket info -> http://localhost:5000/tickets/<Ticket_ID>
2. [GET] Get all tickets for specific event -> http://localhost:5000/events/<Event_Id>/tickets
3. [PATCH] Generate barcode -> http://localhost:5000/tickets/<Ticket_id>
4. [PATCH] Generate all tickets barcode for specific event -> http://localhost:5000/events/<Event_id>/tickets
5. [PUT] Change ticket info (Only "Event No" and "Current zone". Parameter Passed by JSON ("Event No": string, "Current Zone": string)) -> http://localhost:5000/tickets/<ticketID>
6. [POST] Add ticket to the event -> http://localhost:5000/tickets (Parameters passed by JSON. "Event No": string)
7. [DELETE] Remove ticket http://localhost:5000/tickets/<ticketID>

### Queries 2ND TASK:
1. [GET] Get all events -> http://localhost:5000/events
2. [POST] Create tickets for event ('Title' (string) and 'TicNUmber' (number) passed by JSON ) -> http://localhost:5000/events/tickets
3. [PATCH] Rate film  ('Ticket ID' and 'Rating' passed by JSON (both strings))-> http://localhost:5000/events/rate

###JSON EXAMPLES
1. For creating event tickets:
{
	"Title": "Alpha",
	"TicNumber": 100
}
2. For rating movie:
{
	"Ticket ID": "44",
	"Rating": "9"
}