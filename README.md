# P2P File Sharing with Django

A simple peer-to-peer file sharing application built with Django that allows users to share files securely between computers.

## Features

- Web-based interface for file sharing
- Secure file transfer with encryption
- Simple and intuitive UI
- Direct peer-to-peer file transfer
- View shared files in browser

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **File Transfer**: Socket programming
- **Encryption**: Fernet symmetric encryption

## Project Structure

- **Django Web Server**: Handles the web interface and initiates file transfers
- **Receiver Server**: Listens for incoming file transfers on port 5001

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/P2P_File_Sharing_Django.git
   cd P2P_File_Sharing_Django
   ```

2. Install dependencies:
   ```
   pip install django cryptography
   ```

3. Run the Django server:
   ```
   python manage.py runserver
   ```

4. Run the receiver server in a separate terminal:
   ```
   python receiver_server.py
   ```

5. Access the web interface at http://127.0.0.1:8000/

## How to Use

1. Place files you want to share in the `shared_files` directory
2. Open the web interface at http://127.0.0.1:8000/
3. To send a file:
   - Enter the receiver's IP address
   - Enter the receiver's port (default: 5001)
   - Enter the filename from the shared_files directory
   - Click "Send File"
4. Received files will be saved in the `shared_files` directory with a "RECEIVED_" prefix

## Security

Files are encrypted using Fernet symmetric encryption before transmission. A secret key is generated and stored on your desktop the first time you run the application.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created by Aun Ali
