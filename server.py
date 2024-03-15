import socket
import threading

from setting import settings


class Server:
    def __init__(self, hostname=settings.hostname, port=settings.port):
        self.hostname = hostname
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.hostname, self.port))
        self.server.listen(5)
        self.clients = []

    def get_message_length(self, conn):
        try:
            message_length = int(conn.recv(1024).decode())
            return message_length
        except ConnectionResetError:
            for i, client in enumerate(self.clients):
                if client[0] == self.server:
                    self.clients.pop(i)

    def send_message(self, conn, id, message):
        message_length = str(len(message))
        message_length += " " * (1024 - len(message_length))
        try:
            conn.send(bytes(message_length, "utf-8"))
            conn.send(bytes(message, "utf-8"))
        except Exception:
            print(f"[Connection closed] {id}")
            for index, client in enumerate(self.clients):
                if client[1] == id:
                    self.clients.pop(index)
                    print(f"{client[1]} disconnected!")

    def receive_and_send(self, conn, id):
        while True:
            message_length = self.get_message_length(conn)
            if not message_length:
                return
            message = f"[{id}] "
            message += conn.recv(message_length).decode()
            print(message)
            for client in self.clients:
                if client[1] == id:
                    return
                self.send_message(client[0], client[1], message)

    def handle_client(self, conn, id):
        message = f"Welcome to the chatroom, your id is {id}"
        self.send_message(conn, id, message)
        chatroom = threading.Thread(
            target=self.receive_and_send, args=(conn, id)
        )
        chatroom.start()

    def serve(self):
        print(f"{self.hostname} is the server name")
        while True:
            conn, address = self.server.accept()
            name = conn.recv(self.get_message_length(conn)).decode(
                "utf-8"
            )  # to remove if doesn't work
            id = name + str(address[1])
            self.clients.append((conn, id))
            print(f"[New Connection] Connected to {id}")
            self.handle_client(conn, id)


if __name__ == "__main__":
    server = Server()
    server.serve()
