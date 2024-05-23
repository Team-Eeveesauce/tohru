import socket
import subprocess
import os
from dotenv import load_dotenv
from win11toast import toast

# Define singular variable
load_dotenv()
PORT = int(os.getenv('PORT'))

# Define special commands
def runme(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        return(b"no")
    else:
        print(result.stdout)
        return(b"ok")

# Show toast ontifcations in Windows on certain occasions
def show_notification(title, message):
  toast(title, message)


# Main loop
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("0.0.0.0", PORT))
    s.listen()
    print("Kanna active!")
    show_notification("Kanna", "Kanna service is active!")

    while True:
        print("Waiting for something to do...")
        conn, addr = s.accept()
        with conn:
            print(f'Connected to {addr}')
            data = conn.recv(1024)
            if not data:
                break

            print(f"Received: {data.decode()}")

            # Message Handling Logic
            if data.decode() == 'connect':
                print("Was pinged! Sent a reply.")
                show_notification("Kanna", "You've been pinged!")
                reply = b"ok"
            # elif data.decode() == 'gaming':
            #     print("Opening Epic Launcher...")
            #     reply = runme("\"C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe\"")
            #     conn.sendall(b"ok")
            elif data.decode() == 'emby':
                print("Restarting Emby... Probably.")
                reply = runme("\"E:\\Streamable - The Return\\Emby-Server\\system\\EmbyServer.exe\"")
                show_notification("Kanna", "Emby is restarting!")
            elif data.decode() == 'download_spigg':
                conn.sendall(b"no")
                print("Downloading spigg... OR NOT!!")
            elif data.decode() == 'restart':
                conn.sendall(b"no")
                print("Restarting bot... OR NOT!!")
            else:
                reply = b"bad"
                print("Command failed!")
                show_notification("Kanna", "Recieved bad command from Tohru!")

            conn.sendall(reply)
            show_notification("Kanna", "Apparently we replied too...")
