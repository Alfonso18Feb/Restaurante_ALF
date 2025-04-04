import random
import threading
import queue
import time
import matplotlib.pyplot as plt
from collections import Counter


class Restaurante:
    def __init__(self):
        self.reservas = {}
        self.clientes = []
        self.sem = threading.Semaphore(60)  # Capacidad máxima (aforo)
        self.pedidos = queue.Queue()

        # Registro de pedidos
        self.registro_pedidos = Counter()  # Contador para los pedidos realizados

        # Recursos compartidos
        self.recursos = {
            'Pasta': threading.Semaphore(3),             # 3 fuegos
            'Carnes': threading.Lock(),                  # 1 freidora
            'Ensaladas': threading.Semaphore(2),         # 2 estaciones de ensaladas
            'Bocadillos': threading.Lock(),              # 1 bocadillero
            'Platos Especiales': threading.Lock()        # 1 horno
        }
        self.clientes_terminados = 0  # Contador para clientes que han terminado de comer

    def agregar_cliente(self, nombre, comida):
        if nombre not in [c[0] for c in self.clientes]:
            self.clientes.append((nombre, comida))
            return f"Cliente {nombre} agregado con comida {comida}."
        return f"El cliente {nombre} ya existe."

    def hacer_reserva(self, nombre_reservante, comida, fecha, hora, invitados, barrier):
        print(f"{nombre_reservante} intentando hacer la reserva...")

        # Intentar hacer la reserva en un bucle mientras no haya espacio
        while True:
            if self.sem.acquire(blocking=False):  # Intentamos adquirir un semáforo sin bloquear
                print(f"{nombre_reservante} ha entrado al restaurante.")

                clave = f"{fecha} {hora}"
                if clave in self.reservas:
                    self.sem.release()  # Liberar el semáforo si no se puede hacer la reserva
                    return "Lo siento, ya hay una reserva en ese horario."
                if nombre_reservante not in [cliente[0] for cliente in self.clientes]:
                    self.sem.release()  # Liberar el semáforo si el cliente no está en la lista
                    return "El cliente que hace la reserva no está en la lista."
                if any(invitado not in [cliente[0] for cliente in self.clientes] for invitado in invitados):
                    self.sem.release()  # Liberar el semáforo si hay invitados no registrados
                    return "Uno o más invitados no están en la lista de clientes."

                self.reservas[clave] = {'reservante': nombre_reservante, 'comida': comida, 'invitados': invitados}
                print(f"Reserva confirmada para {nombre_reservante} el {fecha} a las {hora} para {len(invitados) + 1} personas.")

                # Hacer los pedidos para el reservante y sus invitados
                for invitado in [nombre_reservante] + invitados:
                    self.pedidos.put((invitado, comida))  # Los clientes hacen sus pedidos
                    self.registro_pedidos[comida] += 1  # Registrar el pedido en el contador

                barrier.wait()

                # Cliente realiza pedido
                print(f"{nombre_reservante} ha terminado de hacer la reserva y está esperando su comida.")
                break  # Salir del bucle cuando la reserva se haya realizado correctamente

            else:
                # Si no hay espacio, esperar un poco antes de volver a intentar
                print(f"{nombre_reservante} no pudo hacer la reserva, el restaurante está lleno. Esperando...")
                time.sleep(2)  # Esperar 2 segundos antes de intentar nuevamente

    def ver_reservas(self):
        if not self.reservas:
            return "No hay reservas registradas."
        resultado = []
        for k, v in self.reservas.items():
            invitados = ", ".join(v['invitados'])
            resultado.append(f"{k}: {v['reservante']} con {v['comida']} y los invitados: {invitados}")
        return "\n".join(resultado)

    def obtener_recurso_por_comida(self, comida):
        if comida in comidas['Pasta']:
            return self.recursos['Pasta']
        elif comida in comidas['Carnes']:
            return self.recursos['Carnes']
        elif comida in comidas['Ensaladas']:
            return self.recursos['Ensaladas']
        elif comida in comidas['Bocadillos']:
            return self.recursos['Bocadillos']
        elif comida in comidas['Platos Especiales']:
            return self.recursos['Platos Especiales']
        else:
            return threading.Lock()

    def cocinero(self, id_cocinero):
        while True:
            try:
                cliente, comida = self.pedidos.get(timeout=5)
            except queue.Empty:
                print(f"Cocinero {id_cocinero} no recibió más pedidos. Cerrando.")
                break

            recurso = self.obtener_recurso_por_comida(comida)
            print(f"Cocinero {id_cocinero} preparando {comida} para {cliente}...")

            with recurso:
                time.sleep(random.uniform(1.0, 2.5))  # Tiempo de cocción
                print(f"Cocinero {id_cocinero} terminó {comida} para {cliente}.")

            print(f"{cliente} recibió su {comida} y está comiendo...")
            time.sleep(5)  # Tiempo de comer
            print(f"{cliente} ha terminado de comer y se va del restaurante.")
            
            # Liberar espacio para nuevas reservas
            self.sem.release()
            self.clientes_terminados += 1

            # Si ya han terminado 4 clientes, permitir nuevas reservas
            if self.clientes_terminados >= 4:
                print("Se permite realizar nuevas reservas, el restaurante tiene espacio.")
                self.clientes_terminados = 0  # Resetear el contador

            self.pedidos.task_done()

    def generar_histograma(self):
        # Generar un histograma de los pedidos
        comidas_pedidas = list(self.registro_pedidos.elements())  # Obtener todos los pedidos realizados
        comida_counts = dict(self.registro_pedidos)  # Contar los pedidos por comida
        
        # Crear el histograma
        plt.figure(figsize=(10, 6))
        plt.bar(comida_counts.keys(), comida_counts.values(), color='skyblue', edgecolor='black')
        plt.title('Frecuencia de Pedidos en el Restaurante')
        plt.xlabel('Tipo de Comida')
        plt.ylabel('Cantidad de Pedidos')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Mostrar el histograma
        plt.show()


# ---------------------------- 
# PROGRAMA PRINCIPAL
# ----------------------------

if __name__ == "__main__":
    restaurante = Restaurante()

    # Comidas disponibles
    comidas = {
        'Carnes': ["Pollo", "Pavo", "Cordero", "Cerdo", "Ternera"],
        'Ensaladas': ["Cesar", "Wolskiana", "Tartavia", "Capresse", "Nizza"],
        'Pasta': ["Spaghetti", "Fusilli", "Farfalle", "Penne", "Rigatoni", "Caracolas", "Tagliatelle"],
        'Bocadillos': ["Big Cheese Burger", "ALF Burger", "ALF Big Sandwich"],
        'Platos Especiales': ["Pizza", "Lasagna"]
    }

    # Lista de nombres
    nombres = ["Antonio", "Alejandro", "Guillermo", "Alfonso", "Fabiola", "Juan", "Ruben", "Álvaro", "Javier", "Pablo",
               "Paula", "Maria", "Marta", "Judith", "Víctor", "Jacinto", "Roman", "Fausto", "Jose"]

    # Agregar 100 clientes aleatorios
    for _ in range(100):
        nombre = random.choice(nombres)
        categoria = random.choice(list(comidas.keys()))
        comida = random.choice(comidas[categoria])
        print(restaurante.agregar_cliente(nombre, comida))

    # Crear barrier para sincronizar las reservas
    barrier = threading.Barrier(len(restaurante.clientes))

    # Iniciar cocineros (5 cocineros)
    for i in range(5):
        threading.Thread(target=restaurante.cocinero, args=(i,), daemon=True).start()

    # Crear hilos de clientes que hacen reservas
    hilos = []
    clientes = restaurante.clientes

    for i in range(len(clientes)):
        nombre_reservante, comida = clientes[i]
        fecha = "2025-04-10"
        hora = f"{8 + i}:00"
        num_invitados = random.randint(1, 3)
        invitados = random.sample([c[0] for c in clientes if c[0] != nombre_reservante], num_invitados)

        h = threading.Thread(target=restaurante.hacer_reserva, args=(nombre_reservante, comida, fecha, hora, invitados, barrier))
        hilos.append(h)
        h.start()

    # Esperar que terminen todos los hilos
    for h in hilos:
        h.join()

    # Esperar a que se cocinen todos los pedidos
    restaurante.pedidos.join()

    print("\nReservas realizadas:\n")
    print(restaurante.ver_reservas())

    # Generar y mostrar el histograma de los pedidos
    restaurante.generar_histograma()
