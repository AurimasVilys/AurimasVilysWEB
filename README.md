# Ticket Stats

### Running
You need to have docker and docker-compose installed.
To build and run:

1. docker-compose build

2. docker-compose up -d

Port 5000 is used for this service.

### Queries:
1. [GET] Get all tickets -> http://localhost:5000/tickets
2. [GET] Get single ticket info -> http://localhost:5000/tickets/1
2. [GET] Get all tickets for specific event -> http://localhost:5000/events/<Event_Id>/tickets
3. [PATCH] Generate ticket -> http://localhost:5000/tickets/<Ticket_id>
4. [PATCH] Generate all tickets for specific event -> http://localhost:5000/events/<Event_id>/tickets
5. [PUT] Change ticket info (Only "Event No" and "Current zone") -> http://localhost:5000/tickets/<ticketID>
6. [PATCH] Scan ticket in -> http://localhost:5000/tickets/in (Parameters passed by JSON. "id": string, "Barcode": number)
7. [PATCH] Scan ticket out -> http://localhost:5000/tickets/out (Parameters passed by JSON. "id": string, "Barcode": number)
8. [POST] Add ticket to the event -> http://localhost:5000/tickets (Parameters passed by JSON. "Event No": string)
9. [DELETE] Remove ticket http://localhost:5000/tickets/<ticketID>
