# File Client and Server
Souce code for server and client for lab6 tasks. Here you can see an implementation of simple server and client for sending files. There is some simple protocol for it and it uses combination of threads and selectors.

## Download server
You can download the server file using the following command:
```
curl https://raw.githubusercontent.com/bogotolec/DS_lab6/master/server.py?token=AF3NNJXRZ3M3F6B5T7G7QVC7NSS7C > server.py
```
or
```
wget https://raw.githubusercontent.com/bogotolec/DS_lab6/master/server.py?token=AF3NNJXRZ3M3F6B5T7G7QVC7NSS7C -O server.py
```

## Run server
You can run server using the following command:
```
python3 server.py
```
After it, server will accept connections on defined ports (8801 for information, 8801 for files by default) on all interfaces.


## Client usage
You can send file to the server using the following command:
```
python3 client.py filename host port
```
