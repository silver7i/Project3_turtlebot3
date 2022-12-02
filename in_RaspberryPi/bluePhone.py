import bluetooth
import serial
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
ser = serial.Serial('/dev/ttyUSB1', 115200,timeout = 1)
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
client_socket,address = server_socket.accept()


class bluetoothpy(Node):
	def __init__(self):
		while 1:
			data = client_socket.recv(1024)
			print("REceived : %s" % data)
			if (data == b'a'):
				ser.write("close")
			elif (data == b'b'):
				ser.write("open")
			
			elif (data == b'q'):
				print ("Quit")
				client_socket.close()
				server_socket.close()
				break
def main():
	print("Accepted connection from ",address)
	bluetoothpy()
	

if __name__ == '__main__':
    main()
    
