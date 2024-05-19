import psutil
import json
import time
import keyboard


# Functiile pentru monitorizare https://psutil.readthedocs.io/en/latest/
# Funcția pentru monitorizarea resurselor CPU

def monitor_cores():
    return psutil.cpu_count(logical=False)


def monitor_threads():
    return psutil.cpu_count(logical=True)


def monitor_cpu():
    return psutil.cpu_percent(interval=None)


# Funcția pentru monitorizarea resurselor RAM
def monitor_ram():
    return psutil.virtual_memory().percent


# Funcția pentru monitorizarea resurselor de rețea
def monitor_network():
    net = psutil.net_io_counters()
    return {
        'bytes_sent': net.bytes_sent,
        'bytes_recv': net.bytes_recv
    }


# Funcția pentru monitorizarea informațiilor despre procese
def monitor_processes():
    procs = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'memory_percent'])}
    return procs


# Functia pentru monitorizarea stocarii
def monitor_disks():
    disk = psutil.disk_io_counters()
    return {

        'read_bytes': disk.read_bytes,
        'write_bytes': disk.write_bytes,
        'read_time': disk.read_time,
        'write_time': disk.write_time
    }


def monitor_disk_usage():
    usage = psutil.disk_usage('/')
    return {
        'total bytes': usage.total,
        'used bytes': usage.used,
        'free bytes': usage.free,
        'disk percentage': usage.percent,

    }


# Functia pentru indentare json
def indentare():
    return '-'


# Funcția principală care rulează în buclă infinită și salvează datele agregate la intervale de timp specificate, si
# se opreste la apasarea tastei q
def main(interval, filename):
    stop_requested = False

    def stop_monitoring(event):
        nonlocal stop_requested
        stop_requested = True

    keyboard.on_press_key('q', stop_monitoring)

    # liniile 69-84 https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

    while not stop_requested:
        data = {
            'Informatii procesor': indentare(),
            'cores': monitor_cores(),
            'threads': monitor_threads(),
            'cpu_usage [%]': monitor_cpu(),

            'Informatii ram': indentare(),
            'ram_usage [%]': monitor_ram(),

            'Inforatii stocare': indentare(),
            'disk_speed': monitor_disks(),
            'disk_usage': monitor_disk_usage(),

            'Informatii network': indentare(),
            'network': monitor_network(),

            'Informatii procese': indentare(),
            'processes': monitor_processes(),
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=5, sort_keys=False)

        # cpu
        print('Specificatii CPU ')
        print('cpu_usage', monitor_cpu(), '%')
        print('cores', monitor_cores())
        print('threads', monitor_threads())
        print('--------------------')
        # ram
        print('Specificatii RAM ')
        print('ram_usage', monitor_ram(), '%')
        # network
        print('--------------------')
        print('Specificatii network')
        print('network', monitor_network())
        # storage
        print('--------------------')
        print('Specificatii stocare')
        print('disk_speed', monitor_disks())
        print('disk_usage', monitor_disk_usage())
        print('--------------------')
        print('Pentru oprire, apasa tasta Q')

        time.sleep(interval)

    keyboard.unhook_all()


if __name__ == "__main__":
    main(interval=3, filename="resource_monitoring.json")

# pip freeze > requirements.txt
