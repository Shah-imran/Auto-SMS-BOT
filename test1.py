from signalwire.rest import Client as signalwire_client

client = signalwire_client("9103da5a-c761-4aad-a8d6-ad34acba708a", "PT707ecf7c969419fe89c874a99590ed22d7fba91b0b10a23c", signalwire_space_url = 'selfoffer.signalwire.com')

message = client.messages.create(
                              from_='+12764774094',
                              body='Hello World!',
                              to='+13177213016'
                          )

print(message.sid)