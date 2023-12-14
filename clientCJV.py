#Carson Vanderheyden (100882481)
#TPRG 2131-01
#This program is strictly my own work. Any material
#beyond course learning materials that is taken from  
#the Web or other souces is properly cited, giving
#credit to the origonal author(s).
import json
import socket
import subprocess
import time
from tkinter import *

def get_vcgencmd_output(command):
    result = subprocess.run(['vcgencmd', command], capture_output=True, text=True)
    output = result.stdout.strip()

    try:
        if 'temp=' in output:
            temperature_str = output.split('=')[1].split('\'')[0]
            temperature = float(temperature_str)
            return temperature
        else:
            frequency_str = output.split('=')[1].split(' ')[0].replace('\n', '')
            frequency = float(frequency_str)
            return frequency
    except (ValueError, IndexError):
        print(f"Error parsing value from '{output}'")
        return None

def collate_data(iteration_count):
    arm_core_speed = get_vcgencmd_output('measure_clock arm')
    gpu_core_speed = get_vcgencmd_output('measure_clock core')
    h264_block_speed = get_vcgencmd_output('measure_clock v3d')
    isp_speed = get_vcgencmd_output('measure_clock vpu')
    core_temp = get_vcgencmd_output('measure_temp')

    if any(speed is None for speed in [arm_core_speed, gpu_core_speed, h264_block_speed, isp_speed, core_temp]):
        print("Error getting VCGencmd values")
        return None

    data = {
        "iteration_count": iteration_count,
        "arm_core_speed": round(arm_core_speed, 1),
        "gpu_core_speed": round(gpu_core_speed, 1),
        "h264_block_speed": round(h264_block_speed, 1),
        "isp_speed": round(isp_speed, 1),
        "core_temp": round(core_temp, 1)
    }
    return data

def update_labels(labels, data):
    for key, value in data.items():
        labels[key].config(text=f"{key}: {value}")

def main():
    server_address = ('10.102.13.217', 8000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connecting to server at {server_address}")
        client_socket.connect(server_address)

        root = Tk()
        root.title("Client")

        labels = {}
        keys = ["iteration_count", "arm_core_speed", "gpu_core_speed", "h264_block_speed", "isp_speed", "core_temp"]
        for key in keys:
            label = Label(root, text=f"{key}: 0.0")
            label.pack()
            labels[key] = label

        def update_gui():
            nonlocal labels
            for iteration in range(50):
                data_to_send = collate_data(iteration)
                if data_to_send is not None:
                    try:
                        client_socket.send(json.dumps(data_to_send).encode('utf-8'))
                    except BrokenPipeError:
                        print("Connection closed by the server.")
                        break

                    update_labels(labels, data_to_send)
                    root.update()
                    time.sleep(2)

            client_socket.close()  
            root.destroy()  # Close the Tkinter window

        
        root.after(0, update_gui)

        # Start the Tkinter event loop
        root.mainloop()

    except ConnectionRefusedError:
        print("Connection refused. Is the server running?")

if __name__ == "__main__":
    main()                   