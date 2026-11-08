import os
import time
import router

routers = [
    {"nombre": "Router1", "ip": "127.0.0.1", "puerto": "8881", "filename": "rutasR1.txt"},
    {"nombre": "Router2", "ip": "127.0.0.1", "puerto": "8882", "filename": "rutasR2.txt"},
    {"nombre": "Router3", "ip": "127.0.0.1", "puerto": "8883", "filename": "rutasR3.txt"}
]


for rt in routers:
    pid = os.fork()

    if pid == 0:
        #proceso hijo
        router.Router.main(rt["ip"], rt["puerto"], rt["filename"])

        os._exit(0)

    else:
        print(f"Proceso padre lanzó {rt["nombre"]}, escuchando en {(rt["ip"], rt["puerto"])}")
        print(f"PID: {pid}")


print("[INFO] Red de mini internet corriendo ...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[INFO] APAGANDO LA RED ...\n")