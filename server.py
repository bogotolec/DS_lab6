import socket
import select
from threading import Thread
import os

files = dict()

CLIENTPORT = 8800
FILEPORT = 8801

# Thread to listen one particular client
class ClientListener(Thread):
	def __init__(self, name: str, addr, sock: socket.socket):
		super().__init__(daemon=True)
		self.sock = sock
		self.name = "Client listener " + name
		self.addr = addr

	def _close(self):
		self.sock.close()
		print(self.name + ' disconnected')

	def run(self):

		while True:

			# try to read 1024 bytes from user
			# this is blocking call, thread will be paused here
			data = self.sock.recv(1024)
			if data:
				if b"end" == data:
					# send port where client should send file 
					self.sock.send(str(FILEPORT).encode('utf-8'))
				else:
					# get information about the file
					name, size = str(data.decode("utf-8")).split(",")
					size = int(size.replace("\\n", ""))

					# print information about the file
					print(self.name + ": get filename '" + name + "'")
					print(self.name + ": get filesize '" + str(size) + "'")
					
					# add information about the file into the dictionary
					if self.addr not in files:
						files[self.addr] = []

					files[self.addr].append((name, size))

					self.sock.send(b"got data")
			else:

				# close connection
				self._close()
				return

# Thread to listen one particular client
class FileListener(Thread):
	def __init__(self, name: str, addr, sock: socket.socket):
		super().__init__(daemon=True)
		self.sock = sock
		self.name = "File listener " + name
		self.addr = addr

	def _close(self):
		self.sock.close()
		print(self.name + ' disconnected')

	def run(self):

		# check if we have information about the file
		if (self.addr not in files) or (len(files[self.addr]) == 0):
			print(self.name + ": cannot find information about file")
			self._close()
		else:
			originalfilename, size = files[self.addr].pop(0)
			
			# check if file already exists,
			# in this case we try to save file
			# as *_copyN.* 
			filename = originalfilename
			i = 1
			while os.path.isfile(filename):
				splitted = originalfilename.split('.')
				splitted[0] += "_copy" + str(i)
				filename = ".".join(splitted)
				i += 1

			# Read and write the file
			f = open(filename, "wb")

			blocksize = 1024
			for i in range(0, size + 16, blocksize):
				data = self.sock.recv(blocksize)
				f.write(data)

			f.close()
			self._close()


def main():
	servers = []
	portlist = [CLIENTPORT, FILEPORT]

	for i in portlist:
		ds = ('', i)

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind(ds)
		server.listen(10)

		servers.append(server)

	i = 1
	while True:
		readable,_,_ = select.select(servers, [], [])
		ready_server = readable.pop(0)

		connection, addr = ready_server.accept()
		port = connection.getsockname()[1]

		print("New connection at " + addr[0] + ":" + str(port))
		name = 'u' + str(i)
		i += 1

		listener = None
		if port == CLIENTPORT:
			listener = ClientListener(name, addr[0], connection)
		elif port == FILEPORT:
			listener = FileListener(name, addr[0], connection)

		if listener != None:
			listener.run()


if __name__ == "__main__":
	main()