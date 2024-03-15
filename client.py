import socket
import threading

from setting import settings


class Client:
    def __init__(self, hostname=settings.hostname, port=settings.port):
        self.hostname = hostname
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.hostname, self.port))

    def send_message(self, message):
        try:
            message_length = str(len(message))
            message_length += " " * (1024 - len(message_length))
            self.client.send(bytes(message_length, "utf-8"))
            self.client.send(bytes(message, "utf-8"))
        except ConnectionResetError:
            print(
                "Unable to send message to server. Make sure server is running..."
            )
            return True

    def receive_message(self):
        while True:
            try:
                length = int(self.client.recv(1024).decode())
                if length:
                    message = self.client.recv(length).decode(
                        "utf-8"
                    )  # remove utf-8 after testing to check behavior
                    print(message)
            except ConnectionResetError or ValueError:
                print(
                    "Error in connecting to server. Make sure server is running..."
                )
                break

    def run(self):
        threading.Thread(target=self.receive_message).start()
        name = input("Enter your name -> ")
        self.send_message(name)
        print("Type your message and press enter to send")
        while True:
            message = input("")
            if self.send_message(message):
                break


if __name__ == "__main__":
    client = Client()
    client.run()
