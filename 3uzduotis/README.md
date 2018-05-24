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

00. Add Tickets to Event
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:addTicketToEvent>
         <tns:MovieName>Movie_1</tns:MovieName>
         <tns:NumberOfTickets>10</tns:NumberOfTickets>
      </tns:addTicketToEvent>
   </soapenv:Body>
</soapenv:Envelope>

00. Get information about ticket
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:getTicket>
         <tns:TicketID>1</tns:TicketID>
      </tns:getTicket>
   </soapenv:Body>
</soapenv:Envelope>

00. Rate event (film) by Ticket ID
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:addRatingToEvent>
         <tns:TicketID>3</tns:TicketID>
         <tns:Rating>5</tns:Rating>
      </tns:addRatingToEvent>
   </soapenv:Body>
</soapenv:Envelope>

00. Generate barcode for ticket
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:generateEventTickets>
         <tns:EventID>2</tns:EventID>
      </tns:generateEventTickets>
   </soapenv:Body>
</soapenv:Envelope>

00. Delete ticket
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:DeleteTicket>
         <!--Optional:-->
         <tns:TicketID>3</tns:TicketID>
      </tns:DeleteTicket>
   </soapenv:Body>
</soapenv:Envelope>

00. Change information about ticket
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:EditTicket>
         <!--Optional:-->
         <tns:TicketID>4</tns:TicketID>
         <!--Optional:-->
         <tns:EventID>3</tns:EventID>
         <!--Optional:-->
         <tns:Barcode>123</tns:Barcode>
         <!--Optional:-->
         <tns:Current_Zone>1</tns:Current_Zone>
      </tns:EditTicket>
   </soapenv:Body>
</soapenv:Envelope>
