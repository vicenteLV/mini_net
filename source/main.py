import sys
import os
import time

import router
import dgrama


#lista de diccionarios para inicializar routers
routers = [
    {"nombre": "Router1","ip": "127.0.0.1", "port": 8881, "filename": "R1"},
    {"nombre": "Router2","ip": "127.0.0.1", "port": 8882, "filename": "R2"},
    {"nombre": "Router3","ip": "127.0.0.1", "port": 8883, "filename": "R3"},
    {"nombre": "Router3","ip": "127.0.0.1", "port": 8883, "filename": "R4"},
    {"nombre": "Router3","ip": "127.0.0.1", "port": 8883, "filename": "R5"} 
]
                

#TEST parte 2, cada router se conecta a la direccion asignada segun su diccionario
#resto de la logica se maneja en el main() de router.Router
for rt in routers:
    pid = os.fork()

    if pid == 0:
            #proceso hijo
            router.Router.main((rt["ip"], rt["port"]), rt["filename"])

            os._exit(0)
                
    else:
            print(f"[INFO] Proceso padre lanzó {rt["nombre"]} escuchando en {rt["ip"]}:{rt["port"]}")

    time.sleep(2) #para salida ordenada de logs en la consola

print("\n[INFO] Red de mini internet corriendo ...")
    

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("[INFO] Apagando la red ...\n")
    sys.exit(0)
    