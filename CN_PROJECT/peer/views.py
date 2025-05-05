import os
import socket
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from cryptography.fernet import Fernet
from django.views.decorators.csrf import csrf_exempt

SHARED_FOLDER = "shared_files"
os.makedirs(SHARED_FOLDER, exist_ok=True)

key_file = os.path.join(os.path.expanduser("~"), "Desktop", "secret.key")

if not os.path.exists(key_file):
    with open(key_file, "wb") as f:
        f.write(Fernet.generate_key())
fernet = Fernet(open(key_file, "rb").read())

def index(request):
    files = os.listdir(SHARED_FOLDER)
    return render(request, "peer/index.html", {"files": files})

@csrf_exempt
def send_file_view(request):
    if request.method == "POST":
        ip = request.POST.get("ip")
        port = int(request.POST.get("port"))
        filename = request.POST.get("filename")
        file_path = os.path.join(SHARED_FOLDER, filename)

        if not os.path.exists(file_path):
            return JsonResponse({"message": "File not found."})

        try:
            s = socket.socket()
            s.connect((ip, port))
            s.send(b"FILE")  # Protocol header
            s.send(filename.encode())
            ack = s.recv(1024)

            with open(file_path, "rb") as f:
                data = f.read()
                encrypted = fernet.encrypt(data)
                s.sendall(encrypted)

            s.close()
            return JsonResponse({"message": "File sent successfully."})
        except Exception as e:
            return JsonResponse({"message": f"Error: {e}"})

    return JsonResponse({"message": "Invalid request method."})

def file_content_view(request, filename):
    file_path = os.path.join(SHARED_FOLDER, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return HttpResponse(f.read(), content_type="text/plain")
        except Exception as e:
            return HttpResponse(f"Error reading file: {e}", content_type="text/plain")
    return HttpResponse("File not found.", content_type="text/plain")
