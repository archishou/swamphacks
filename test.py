from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("ACc52c75209500e9dbc4f046fc3979a8c7", "8f4281143bfcf6cbc3b4e8ceeb7d1f80")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+18137345578", 
                       from_="+17196940306", 
                       body="Hello from Python!")
