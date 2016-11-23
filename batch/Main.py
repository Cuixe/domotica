from batch.models.Socket import Socket


sockets = Socket.get_sockets()
for socket in sockets:
    print socket

socket.turn_off()
print 'Nuevos valores:'
sockets = Socket.get_sockets()
for socket in sockets:
    print socket