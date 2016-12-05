from batch.networking import Client

client = Client()
client.start(attempts=5)
client.send_message(message="Otro Mensaje")