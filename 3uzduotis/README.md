# Ticket Stats

### Running
You need to have docker and docker-compose installed.
To build and run:

1. docker-compose build

2. docker-compose up -d

Used ports are 5000 and 81

### WSDL FILE
URL: http://localhost:5000/soap/tickets?wsdl

### Queries 3RD TASK:
0. [GET] Get all tickets with events (Embeded parameter) -> http://localhost:5000/tickets?embedded=events
00. [GET] Get single ticket info (Embeded paramater) -> http://localhost:5000/tickets/<Ticket_ID>?embedded=events
1. [GET] Get all events -> http://localhost:5000/events
2. [POST] Create tickets for event ('Title' (string) and 'TicNumber' (number) passed by JSON ) -> http://localhost:5000/events/tickets
3. [POST] Create new film and tickets using embeded parameter "movie". TicNumber, and Movie(Title,Release date, Rating, Genre) passed by JSON -> localhost:5000/events/tickets?embedded=movie
4. [PATCH] Rate film  ('Ticket ID' and 'Rating' passed by JSON (both strings))-> http://localhost:5000/events/rates

### JSON EXAMPLES
1. For creating event tickets:
{
	"Title": "Alpha",
	"TicNumber": 100
}
2. For creating movie and event tickets:
{
	"TicNumber": 100,
	"Movie": {"Title": "Venom", "Release_date": "2018", "Rating": "Not Rated", "Genre": "Horror"}
}
3. For rating movie:
{ 
	"Ticket ID": "1",
	"Rating": "9"
}