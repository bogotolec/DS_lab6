import sys
import os
import socket
from pathlib import Path

def print_progress(now, total):
	print("\r" + str(int((now / total) * 100)) + "%", end = "")

def main():
	# print command line arguments
	if len(sys.argv) != 4:
		print("usage: " + sys.argv[0] + " filename ip_address|hostname port")
	else:
		# File check
		filename = sys.argv[1]
		if not os.path.isfile(filename):
			print("File "  + filename + "does not exist")
		filesize = Path(filename).stat().st_size

		host = sys.argv[2]
		port = int(sys.argv[3])

		# Send info
		sock = socket.socket()
		sock.connect((host, port))
		sock.send(filename.encode('utf-8') + b"," + str(filesize).encode('utf-8'))
		sock.close()

		# Send file
		sock = socket.socket()

		f = open(filename, "rb")
		blocksize = 1024

		print_progress(0, filesize)

		sock.connect((host, 8801))
		for i in range(0, filesize, blocksize):
			data=f.read(blocksize)
			sock.send(data)
			print_progress(i, filesize)

		print_progress(filesize, filesize)
		print()
		print("Done")

		sock.close()

if __name__ == "__main__":
    main()