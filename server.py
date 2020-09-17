import socket
import select
from threading import Thread
import os

files = dict()


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

                name, size = str(data.decode("utf-8")).split(",")
                size = int(size.replace("\\n", ""))

                print(self.name + ": get filename '" + name + "'")
                print(self.name + ": get filesize '" + str(size) + "'")
                
                if self.addr not in files:
                    files[self.addr] = []

                files[self.addr].append((name, size))

            else:
                # if we got no data – client has disconnected
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
        if (self.addr not in files) or (len(files[self.addr]) == 0):
            print(self.name + ": cannot find information about file")
            self._close()
        else:
            originalfilename, size = files[self.addr].pop(0)
            
            # Check if file already exists 
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
    portlist = [8800, 8801] # 8800 for info, 8801 for files

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

    	listener = 0
    	if port == 8800:
    		listener = ClientListener(name, addr[0], connection)
    	elif port == 8801:
    		listener = FileListener(name, addr[0], connection)

    	listener.run()



if __name__ == "__main__":
    main()