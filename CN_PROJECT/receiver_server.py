import socket
import threading
import os
from cryptography.fernet import Fernet

RECEIVE_PORT = 5001
SHARED_FOLDER = "shared_files"
os.makedirs(SHARED_FOLDER, exist_ok=True)

key_file = os.path.join(os.path.expanduser("~"), "Desktop", "secret.key")
fernet = Fernet(open(key_file, "rb").read())

def handle_client(conn):
    try:
        header = conn.recv(4)
        if header != b"FILE":
            conn.close()
            return

        filename = conn.recv(1024).decode()
        conn.send(b"OK")

        encrypted_data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            encrypted_data += chunk

        data = fernet.decrypt(encrypted_data)
        save_path = os.path.join(SHARED_FOLDER, "RECEIVED_" + filename)
        with open(save_path, "wb") as f:
            f.write(data)

        print(f"[RECEIVED] File saved: RECEIVED_{filename}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket()
    server.bind(("", RECEIVE_PORT))
    server.listen(5)
    print(f"[LISTENING] Receiving server on port {RECEIVE_PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] From {addr}")
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
