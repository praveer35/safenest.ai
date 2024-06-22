import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    try:
        while True:
            response = client.recv(4096)
            if not response:
                break
            print(response.decode('utf-8'))
    finally:
        client.close()

if __name__ == "__main__":
    main()
