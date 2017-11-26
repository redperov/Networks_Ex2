import sys
from Cache import Cache
from socket import socket, AF_INET, SOCK_DGRAM

server_cache = Cache()
server_cache.load_file()
