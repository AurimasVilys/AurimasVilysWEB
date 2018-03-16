# Ticket Stats

### Running
You need to have docker and docker-compose installed.
To build and run:

1. docker-compose build

2. docker-compose up -d

Port 5000 is used for this service.

### Queries:
1. Get all tickets -> http://localhost:5000/current
2. Get all tickets for specific event -> http://localhost:5000/current/<Event_Id>
3. Generate ticket -> http://localhost:5000/generateTicket/<Ticket_id>
4. Generate all tickets for specific event -> http://localhost:5000/generateEventTickets/<Event_id>
5. Scan ticket in -> http://localhost:5000/ScanIN (Parameters passed by JSON. id: string, "Barcode": number)
6. Scan ticket out -> http://localhost:5000/ScanOUT (Parameters passed by JSON. "id": string, "Barcode": number)
7. Add ticket to the event -> http://localhost:5000/addTicket (Parameters passed by JSON. "Event No": string)
8. Remove ticket http://localhost:5000/removeTicket/<ticketID>
