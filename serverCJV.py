#Carson Vanderheyden (100882481)
#TPRG 2131-01
#This program is strictly my own work. Any material
#beyond course learning materials that is taken from  
#the Web or other souces is properly cited, giving
#credit to the origonal author(s).
import json
import socketserver
from tkinter import *

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_received = self.request.recv(1024).decode('utf-8')
        process_data(json.loads(data_received))

def process_data(data):
    # Implement your code to extract and process data from the JSON object
    # Display the data in the GUI
    print("Received data:", data)

class ServerGUI:
    def __init__(self, root):
        self.root = root

        # Labels to display server status
        self.label_status = Label(root, text="Server Status: Waiting for connections")
        self.label_status.pack()

        # Start the server in a separate thread
        self.server_thread = socketserver.ThreadingTCPServer(('127.0.0.1', 8000), MyTCPHandler)
        self.server_thread.allow_reuse_address = True
        self.server_thread_thread = threading.Thread(target=self.server_thread.serve_forever)
        self.server_thread_thread.daemon = True
        self.server_thread_thread.start()

        # Add a button to stop the server
        self.button_stop_server = Button(root, text="Stop Server", command=self.stop_server)
        self.button_stop_server.pack()

    def stop_server(self):
        self.server_thread.shutdown()
        self.server_thread.server_close()
        self.label_status.config(text="Server Status: Stopped")

def main():
    # Create GUI window for the server
    root = Tk()
    root.title("Server")

    server_gui = ServerGUI(root)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()