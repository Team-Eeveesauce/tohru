import socket
import threading
import base64
import sys


#This is a beta version and as such is not recommened
#Author: Eskebre

class common:

    def __init__(self) -> None:
        pass

    def packet_handler(data):
        if isinstance(data, bytes):
            data = data.decode()
        data = str(data)
        packet_args = common.packet_to_dict(data)
        packet_args.setdefault('type',"")
        packet_args.setdefault('data',"") 
        packet_args['data'] = common.decode_data(packet_args['type'], packet_args['data'])
        return packet_args
    
    def decode_data(type, data):
        match type:
            case "b64":
                 return base64.b64decode(data).decode()
            case _:
                return data

    def packet_to_dict(packet): #The packet data structure key and value are seperated by a colon and entries by a comma 
        output: dict = {}       #e.g. <key>:<value>,<key>:<value>
        for i in packet.split(','):
            j = i.split(':')
            if (len(j) <= 1):
                j.append('true')
            output[j[0]] = j[1]
        return output
    
    def recieve(client, recv_buffer, buffer):
        
        recv_buffer += client.recv(buffer)
        term_pos = recv_buffer.find(b';')
        if term_pos == -1: #if no semicolon
            return recv_buffer, None
        packet = recv_buffer[:term_pos]
        recv_buffer = recv_buffer[(term_pos+1):]
        data = common.packet_handler(packet)
        return recv_buffer, data
    
    def packet_builder(data: dict) -> str:
        stringbuilder: str = ""
        if len(data) == 0:
            return ""
        for key, value in data.items():
            stringbuilder += f"{key}:{value},"
        stringbuilder = stringbuilder.removesuffix(',')
        stringbuilder += ';'
        return stringbuilder
    
    def type_encoder(data: str, encode_type):
        output = data
        match encode_type:
            case 'b64':
                output = base64.b64encode(data.encode()).decode()
            case _:
                pass

        return output

    

class client:

    def __init__(self, host: str = "127.0.0.1", port: int = 10000) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_thread = threading.Thread(target=self.receive)
        self.HOST = host
        self.PORT = port
        self.serverKey = None
        self.buffer = 1024

    def connect(self):
        self.client.connect((self.HOST,self.PORT))
        print("Connected to server")
        self.on_connect()
        self.receive_thread.start()

    def receive(self):
        recv_buffer = bytes()
        while True:
            recv_buffer, data = common.recieve(self.client, recv_buffer, self.buffer)
            if data is not None:
                    self.on_receive(data)
            

    def on_receive(self, data):
        pass

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def close(self):
        self.client.close()

    def send(self, data: str, encode_type = "none"):
        data = common.type_encoder(data, encode_type)
        packet_dict = {'data': data,'type': encode_type}
        packet: str = common.packet_builder(packet_dict)
        self.client.send(packet.encode())
    

class server:

    def __init__(self, host: str = "0.0.0.0", port: int = 10000) -> None:
        self.HOST = host
        self.PORT = port
        self.buffer = 1024
        self.protocol_Version = "eskcompro"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.HOST, self.PORT))
        self.id_counter: int = 0
        self.clients = {}
        self.clients_address = {}
        

    def start(self) -> None:
        self.server.listen()
        print("server started")
        self.connection_handler()
        
        


    def client_handler(self, client: socket, id: int):
        recv_buffer = bytes()
        self.on_connect(client)
        while True:
            try:
                recv_buffer, data = common.recieve(client, recv_buffer, self.buffer)
                if data is not None:
                    self.on_receive(data, id)
            except socket.timeout as e:
                print(f"Client Timeout: {e}")
                break
            except Exception as e:
                print(f"Client handler error: {e}")
                break
                
        self.on_disconnect(client)
        self.remove_client(id)

    def send(self, data, encode_type = "none", id = None, client = None):
        if id is not None:
            client = self.get_client(id)
        if client is None:
            print(f"No client found")
            return
      
            
        
        data = common.type_encoder(data, encode_type)
        packet_dict = {'data': data, 'type': encode_type}
        packet: str = common.packet_builder(packet_dict)
        client.send(packet.encode())

    def broadcast(self, data, encode_type = "none"):
        for i in self.clients.keys():
            self.send(data, encode_type, id=i)


    
    def encryption(data: str):
        return base64.b64encode(data)

    def connection_handler(self):
        while True:
            client, address = self.server.accept()
            print("Client connect")
            id = self.add_client(client, address)
            thread = threading.Thread(
                target=self.client_handler, 
                args=(client,id),
            )
            

            thread.start()
        pass
    
    def get_client(self, id) -> socket.socket:
        return self.clients.get(id)

    def add_client(self, client: socket.socket, address) -> int:
        while (self.id_counter in self.clients.keys()):
            self.id_counter += 1
        id = self.id_counter
        self.clients[id] = client
        self.clients_address[id] = address
        return id

    def remove_client(self, id) -> bool:
        try:
            self.get_client(id).close()
        except:
            pass
        try:
            self.clients.pop(id)
            self.clients_address.pop(id)
            return True
        except KeyError as ke:
            return False
        

    def on_receive(self, data, client):
        return

    def on_connect(self, client):
        return
    
    def on_disconnect(self, client):
        pass
        

def on_recv(data, client_id):
    print(data['data'])
