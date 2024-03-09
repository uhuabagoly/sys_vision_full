from customtkinter import *
from customtkinter import CTkLabel
from tkinter import filedialog
from tkinter import *
import customtkinter
import subprocess
import platform
import requests
import GPUtil
import getmac
import psutil 
import socket
import time
import uuid

customtkinter.set_appearance_mode("system")

app = customtkinter.CTk()
app.resizable(False,False)
app.title("Sys Vision")
app.geometry("1200x600")

color_1 = "#029cff"
color_2 = "#005eab"
color_3 = "#242424"

font_test = "Arial" #Helvetica

my_system = platform.uname()

frame01 = CTkFrame(app,
                   fg_color=color_2,
                   border_color=color_1,
                   border_width=4,
                   width=700,
                   height=450)
frame01.place(x=20, y=20)

label = customtkinter.CTkLabel(frame01, 
                               text=f"- Machine: {my_system.machine}",
                               font=(font_test, 18)).place(x=10, y=20)

def get_cpu_info():
    try:
        cpu_info = platform.processor()
        return cpu_info
    except Exception as e:
        print(f"Hiba történt: {e}")
    return None

label = customtkinter.CTkLabel(frame01, 
                               text=f"- Processor:{my_system.processor}",
                               font=(font_test, 18)).place(x=10, y=50)

memory = psutil.virtual_memory()
label = customtkinter.CTkLabel(frame01, 
                               text=f"- Total RAM: {round(memory.total / (1024 ** 3), 2)} GB",
                               font=(font_test, 18)).place(x=10, y=80)

lap_Board = subprocess.run(['wmic', 'baseboard', 'get', 'product'],capture_output=True, text=True)
lap = lap_Board.stdout.strip()

label = CTkLabel(frame01, 
                 text=f"- Board: {lap}", 
                 font=(font_test, 18)).place(x=10, y=110)

video_card_process = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'caption'], capture_output=True, text=True)
video_card_info = video_card_process.stdout.strip()

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()

        for idx, gpu in enumerate(gpus):
            print(f"GPU {idx + 1} márkája: {gpu.name}")
            print(f"GPU {idx + 1} memória: {gpu.memoryTotal} MB\n")
            print(f"Összesen {len(gpus)} GPU található.")
            
    except Exception as e:
        print(f"Hiba történt: {e}")

get_gpu_info()

label = CTkLabel(frame01, 
                 text=f"- Video card: {video_card_info}:", 
                 font=(font_test, 18)).place(x=10, y=180)

frame02 = CTkFrame(app,
                   fg_color=color_2,
                   border_color=color_1,
                   border_width=4,
                   width=440,
                   height=200,)
frame02.place(x=740, y=20)

label = customtkinter.CTkLabel(frame02, 
                               text=f"Internet speed test & router info(s)",
                               font=(font_test, 18)).place(x=15, y=20)

label = customtkinter.CTkLabel(frame02, 
                            text=f"----------------------------------------",
                            font=(font_test, 18)).place(x=15, y=48)

def calculate_download_speed(url, duration=5):
    start_time = time.time()
    downloaded_data = 0

    with requests.get(url, stream=True) as response:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                downloaded_data += len(chunk)
            
            if time.time() - start_time >= duration:
                break

    elapsed_time = time.time() - start_time
    download_speed = downloaded_data / elapsed_time / 1024
    return download_speed

url_to_test = "https://www.example.com"
speed = calculate_download_speed(url_to_test)

label = customtkinter.CTkLabel(frame02, 
                               text=f"Download / Writing speed: {speed:.2f} KB/s | {speed * 1024:.2f} MB/s",
                               font=(font_test, 18)).place(x=15, y=70)

def calculate_speed(url, direction, data=None, duration=5):
    start_time = time.time()
    data_transferred = 0

    if direction == "download":
        with requests.get(url, stream=True) as response:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    data_transferred += len(chunk)
                
                if time.time() - start_time >= duration:
                    break
    elif direction == "upload":
        response = requests.post(url, data=data.encode("utf-8"))
        data_transferred = len(response.content)

    elapsed_time = time.time() - start_time
    speed = data_transferred / elapsed_time / 1024  # in kilobytes per second
    return speed


upload_url = "https://www.example.com/upload"
upload_data = "Hello, this is an example upload data."
upload_speed = calculate_speed(upload_url, "upload", data=upload_data)
label = customtkinter.CTkLabel(frame02, 
                               text=f"Upload / Reading speed: {upload_speed:.2f} KB/s | {upload_speed * 1024:.2f} MB/s",
                               font=(font_test, 18)).place(x=15, y=95)

def get_router_ip():
    try:
        # Csatlakozás egy külső szerverhez (pl. Google DNS)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        router_ip = s.getsockname()[0]
        s.close()
        return router_ip
    except socket.error:
        return None
    
label = customtkinter.CTkLabel(frame02, 
                            text=f"----------------------------------------",
                            font=(font_test, 18)).place(x=15, y=115)

router_ip = get_router_ip()
url = router_ip

if router_ip:
    label = customtkinter.CTkLabel(frame02, 
                               text=f"Your router ip: {router_ip}",
                               font=(font_test, 18)).place(x=15, y=135)
else:
    label = customtkinter.CTkLabel(frame02, 
                               text=f"Your router ip: ~Not found~",
                               font=(font_test, 18)).place(x=15, y=135)
    
def get_router_mac(router_ip):
    try:
        router_mac = getmac.get_mac_address(ip=router_ip)
        return router_mac
    except:
        return None
    
router_mac = get_router_mac(router_ip)

if router_mac:
    label = customtkinter.CTkLabel(frame02, 
                               text=f"Your router mac address: {router_mac}",
                               font=(font_test, 18)).place(x=15, y=158)
else:
    label = customtkinter.CTkLabel(frame02, 
                               text=f"Your router mac address: ~Not found~",
                               font=(font_test, 18)).place(x=15, y=158)

frame03 = CTkFrame(app,
                   fg_color=color_2,
                   border_color=color_1,
                   border_width=4,
                   width=440,
                   height=230,)
frame03.place(x=740, y=240)

label = customtkinter.CTkLabel(frame03, 
                               text=f"System: {my_system.system}",
                               font=(font_test, 18)).place(x=20, y=20)

label = customtkinter.CTkLabel(frame03, 
                               text=f"System version: {my_system.version}",
                               font=(font_test, 18)).place(x=20, y=45)

label = customtkinter.CTkLabel(frame03, 
                               text=f"Node name: {my_system.node}",
                               font=(font_test, 18)).place(x=20, y=70)

arch = platform.architecture()
label = customtkinter.CTkLabel(frame03, 
                               text=f"Architecture: {arch}",
                               font=(font_test, 18)).place(x=20, y=95)

info = platform.platform()
label = customtkinter.CTkLabel(frame03, 
                               text=f"Platform Information: {info}",
                               font=(font_test, 18)).place(x=20, y=120)

def get_public_ip_address():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        ip_address = response.json().get('ip')
        return ip_address
    except requests.RequestException as e:
        print(f"Hiba történt: {e}")
        return None

public_ip_address = get_public_ip_address()
label = customtkinter.CTkLabel(frame03, 
                               text=f"Public ip address: {public_ip_address}",
                               font=(font_test, 18)).place(x=20, y=145)

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return mac

if __name__ == "__main__":
    mac_address = get_mac_address()

label = customtkinter.CTkLabel(frame03, 
                                text=f"MAC address: {mac_address}",
                                font=(font_test, 18)).place(x=20, y=170)

frame_footer = CTkFrame(app, fg_color="transparent",
                   border_color=color_3,
                   width=1200,
                   height=148,)

frame_footer.place(y=520)

def driver_info():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text files", ".txt"),
            ("HTML files", ".html"),
            ("All files", ".*"),
        ]
    )

    def get_processor_info():
        return platform.processor()

    def get_processor_generation(processor_info):
        if "Intel" in processor_info:
            return "Intel generáció"
        elif "AMD" in processor_info:
            return "AMD generáció"
        else:
            return "Ismeretlen generáció"

    def get_system_architecture():
        arch_info = platform.architecture()
        return arch_info

    def get_cpu_usage():
        cpu_percent = psutil.cpu_percent(interval=1)
        processor_info = get_processor_info()
        processor_generation = get_processor_generation(processor_info)
        cpu_frequency = psutil.cpu_freq().max
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        architecture_info = get_system_architecture()


        file.write("\n| CPU info\n")
        file.write(f"+ CPU brand: {processor_info}\n")
        file.write(f"+ CPU generation: {processor_generation}\n")
        file.write(f"+ CPU max speed: {cpu_frequency} MHz\n")
        file.write(f"+ Number of physical cores: {physical_cores}\n")
        file.write(f"+ Number of logic cores: {logical_cores}\n")
        file.write(f"+ Arch info: {architecture_info}\n")
        file.write(f"+ CPU load: {cpu_percent}%\n")

        return cpu_percent

    def print_memory_info():
        try:

            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            file.write("\n| Memory\n")
            file.write(f"+ Total Memory: {round(memory.total / (1024 ** 3), 2)} GB\n")
            file.write(f"+ Available Memory: {round(memory.available / (1024 ** 3), 2)} GB\n")
            file.write(f"+ Used Memory: {round(memory.used / (1024 ** 3), 2)} GB\n")
            file.write(f"+ Memory usage: {memory.percent}%\n")
            file.write(f"+ Total Swap Memory: {round(swap.total / (1024 ** 3), 2)} GB\n")
            file.write(f"+ Used Swap Memory: {round(swap.used / (1024 ** 3), 2)} GB\n")

            file.write(f"\n| Open memory \n")

            for process in psutil.process_iter(['pid', 'name', 'memory_info']):
                file.write(f"** PID: {process.info['pid']}, Name: {process.info['name']}, Memory: {process.info['memory_info'].rss / (1024 ** 2):.2f} MB \n")

        except Exception as e:
            print(f"Error while writing to file: {e}\n")

    def get_board_info():
        system_info = platform.system()

        if system_info == "Windows":
            lap_board = subprocess.run(['wmic', 'baseboard', 'get', 'product'], capture_output=True, text=True)
            with open(file_path, 'a') as file:
                file.write("\n| Board info\n")
                file.write(f"+ Board brand: {lap_board.stdout.strip()}\n")
        else:
            with open(file_path, 'a') as file:
                file.write("Code is running on a non-Windows system.\n")

    def print_gpu_info():
        try:
            gpu_info = [{'name': 'GPU1', 'manufacturer': 'NVIDIA', 'memory': {'total': 4096}, 'cuda_version': '11.0', 'driver_version': '460.39', 'utilization': {'gpu': 70, 'memory': 30}}]

            if gpu_info:
                file.write("\n| GPU Info\n")
                for gpu in gpu_info:
                    file.write(f"+ GPU name: {gpu['name']}\n")
                    file.write(f"+ Manufacturer: {gpu['manufacturer']}\n")
                    file.write(f"+ Memory size: {gpu['memory']['total']} MB\n")
                    file.write(f"+ CUDA version: {gpu['cuda_version']}\n")
                    file.write(f"+ Driver version: {gpu['driver_version']}\n")
                    file.write(f"+ GPU utilization: {gpu['utilization']['gpu']}%\n")
                    file.write(f"+ Memory utilization: {gpu['utilization']['memory']}%\n")

        except Exception as e:
            print(f"Error during GPU query: {e}\n")

    def get_disk_info():
        disk_info = []

        partitions = psutil.disk_partitions(all=True)

        for partition in partitions:
            partition_info = {}
            partition_info['device'] = partition.device

            try:
                usage = psutil.disk_usage(partition.device)
                partition_info['total'] = round(usage.total / (1024 ** 3), 2)
                partition_info['used'] = round(usage.used / (1024 ** 3), 2)
                partition_info['free'] = round(usage.free / (1024 ** 3), 2)
                partition_info['percent'] = usage.percent

                if 'ssd' in partition.opts.lower():
                    partition_info['type'] = 'SSD'
                elif 'hdd' in partition.opts.lower():
                    partition_info['type'] = 'HDD'
                else:
                    partition_info['type'] = 'Unknown'

                disk_info.append(partition_info)
            except Exception as e:
                print(f"Error while retrieving disk information ({partition.device}): {e}")

        return disk_info

    # Merevlemez információk lekérése
    disks = get_disk_info()

    # Kiírjuk a merevlemez információkat
    with open(file_path, 'w') as file:
        file.write(f"| Driver info ({time.ctime()})\n")
        file.write(50 * "-" + "\n")

        get_cpu_usage()

        get_board_info()

        print_gpu_info()

        print_memory_info()

        file.write("\n| HDD & SSD(s)\n")
        for disk in disks:
            file.write(f"+ Device: {disk['device']}\n")
            file.write(f"+ Type: {disk['type']}\n")
            file.write(f"+ Total: {disk['total']} GB\n")
            file.write(f"+ Used: {disk['used']} GB\n")
            file.write(f"+ Free: {disk['free']} GB\n")
            file.write(f"+ Percent Used: {disk['percent']}%\n")
            file.write(f"\n")

    

btn = customtkinter.CTkButton(frame_footer, 
                              text="Hardver info", 
                              font=(font_test, 18),
                              text_color=color_2,
                              corner_radius=16,
                              fg_color="transparent",
                              border_color="#029cff",
                              border_width=2,
                              height=37,
                              command=driver_info).place(x=350)

def get_network_connections():
    connections = psutil.net_connections()
    return connections

def sys_info():
    result1 = subprocess.run(['systeminfo'], capture_output=True, text=True)
    output1_text = result1.stdout

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", ".txt"),
                                                        ("HTML files", ".html"),
                                                        ("All files", ".*"),
                                                    ])

    if file_path:
        with open(file_path, 'w') as file:
            file.write(output1_text)

            network_connections = get_network_connections()
            file.write("\nNetwork Connections:")
            for conn in network_connections:
                file.write("\n" + str(conn))

btn = customtkinter.CTkButton(frame_footer, 
                              text="System info", 
                              font=(font_test, 18),
                              text_color=color_2,
                              corner_radius=16,
                              fg_color="transparent",
                              border_color="#029cff",
                              border_width=2,
                              height=37,
                              command=sys_info).place(x=700)

app.mainloop()