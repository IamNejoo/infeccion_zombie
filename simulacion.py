import random 
import time    
import json    

# Clase Sensor
class Sensor:
    def __init__(self):
        self.state = 'normal'  # Estado inicial del sensor

    def set_alert(self):
        self.state = 'alert'  # Cambiar a estado de alerta

    def reset(self):
        self.state = 'normal'  # Restablecer a estado normal

    def __str__(self):
        return f"Sensor state: {self.state}"  # Representación en cadena


# Clase Room
class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.sensor = Sensor()
        self.has_zombies = False  # Inicialmente no hay zombis
        self.is_blocked = False   # Inicialmente no está bloqueada

    def add_zombies(self):
        if not self.is_blocked:  # Solo infectar si no está bloqueada
            self.has_zombies = True
            self.sensor.set_alert()

    def remove_zombies(self):
        self.has_zombies = False # Limpiar la habitación

    def block_room(self):
        self.is_blocked = True  # Bloquear la habitación

    def unblock_room(self):
        self.is_blocked = False  # Desbloquear la habitación

    def reset_sensor(self):
        self.sensor.reset()  # Resetear el sensor 

    def __str__(self):
        status = "Zombies: Yes" if self.has_zombies else "Zombies: No"
        blocked = " (Bloqueada)" if self.is_blocked else ""
        return f"Room {self.room_number} - {status}{blocked} | {self.sensor}"


# Clase Floor
class Floor:
    def __init__(self, floor_number, rooms_per_floor):
        self.floor_number = floor_number
        self.rooms = [Room(i) for i in range(rooms_per_floor)]  # Lista de habitaciones

    def is_fully_infected(self):
        # Verifica si todas las habitaciones del piso están infectadas
        return all(room.has_zombies for room in self.rooms)

    def __str__(self):
        floor_status = f"Floor {self.floor_number}\n"
        for room in self.rooms:
            floor_status += str(room) + '\n'
        return floor_status


# Clase Building 
class Building:
    def __init__(self, floors, rooms_per_floor):
        self.floors = [Floor(i, rooms_per_floor) for i in range(floors)]
        self.infect_random_room()  # Infectar una habitación aleatoria al inicio
        
    def load_state(self, filename):
        try:
            with open(filename, 'r') as file:
                state = json.load(file)
                
                # Reconstruir el edificio con las dimensiones del archivo
                floors_count = len(state["floors"])
                rooms_per_floor = len(state["floors"][0]["rooms"])
                self.floors = [Floor(i, rooms_per_floor) for i in range(floors_count)]
                
                # Actualizar el estado de cada habitación
                for floor_data in state["floors"]:
                    floor_num = floor_data["floor_number"]
                    for room_data in floor_data["rooms"]:
                        room_num = room_data["room_number"]
                        room = self.floors[floor_num].rooms[room_num]
                        room.has_zombies = room_data["has_zombies"]
                        room.is_blocked = room_data["is_blocked"]
                        room.sensor.state = room_data["sensor_state"]
                        
            print(f"Estado cargado desde {filename}")
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no existe.")
        except json.JSONDecodeError:
            print(f"Error: El archivo {filename} no tiene un formato JSON válido.")
        except KeyError as e:
            print(f"Error: El archivo {filename} está mal formateado. Falta la clave: {e}")
        except Exception as e:
            print(f"Error inesperado al cargar el estado: {e}")
            
    def infect_random_room(self):
        # Seleccionar un piso y una habitación al azar
        floor_num = random.randint(0, len(self.floors) - 1)
        room_num = random.randint(0, len(self.floors[floor_num].rooms) - 1)
        # Infectar la habitación seleccionada
        self.floors[floor_num].rooms[room_num].add_zombies()

    def is_fully_infected(self):
        # Verifica si todas las habitaciones del edificio están infectadas
        return all(floor.is_fully_infected() for floor in self.floors)

    def __str__(self):
        building_status = 'Estado del edificio:\n'
        for floor in self.floors:
            building_status += str(floor)
        return building_status

    def save_state(self, filename):
        # Guardar el estado del edificio en un archivo JSON
        state = {
            "floors": [
                {
                    "floor_number": floor.floor_number,
                    "rooms": [
                        {
                            "room_number": room.room_number,
                            "has_zombies": room.has_zombies,
                            "is_blocked": room.is_blocked,
                            "sensor_state": room.sensor.state
                        }
                        for room in floor.rooms
                    ]
                }
                for floor in self.floors
            ]
        }
        with open(filename, 'w') as file:
            json.dump(state, file, indent=4)
        print(f"Estado guardado en {filename}")


# Clase Simulation 
class Simulation:
    def __init__(self):
        self.building = None
        self.turn_count = 0  # Contador de turnos

    def setup_building(self, floors_count, rooms_per_floor):
        self.building = Building(floors_count, rooms_per_floor)
        print("¡Edificio configurado correctamente!")
        print("¡Una habitación ha sido infectada aleatoriamente!")

    def show_status(self):
        if self.building:
            print(self.building)
        else:
            print("El edificio aún no ha sido configurado.")

    def advance_turn(self):
        if not self.building:
            print("El edificio aún no ha sido configurado.")
            return

        self.turn_count += 1
        print(f"\n--- Turno {self.turn_count} ---")

        nuevas_infecciones = []
        for floor_num, floor in enumerate(self.building.floors):
            for room in floor.rooms:
                # Solo expandir si la habitación tiene zombis y no está bloqueada
                if room.has_zombies and not room.is_blocked:
                    # Expansión a habitaciones adyacentes en el mismo piso
                    room_index = room.room_number
                    if room_index > 0:  # Habitación izquierda
                        nuevas_infecciones.append((floor_num, room_index - 1))
                    if room_index < len(floor.rooms) - 1:  # Habitación derecha
                        nuevas_infecciones.append((floor_num, room_index + 1))
                    # Expansión a habitaciones correspondientes en pisos adyacentes (vertical)
                    if floor_num > 0 and random.random() < 0.3:  # Piso inferior
                        nuevas_infecciones.append((floor_num - 1, room_index))
                    if floor_num < len(self.building.floors) - 1 and random.random() < 0.3:  # Piso superior
                        nuevas_infecciones.append((floor_num + 1, room_index))

            # Si el piso está completamente infectado, infectar pisos adyacentes
            if floor.is_fully_infected():
                if floor_num > 0:  # Piso inferior
                    nuevas_infecciones.append((floor_num - 1, 0))
                if floor_num < len(self.building.floors) - 1:  # Piso superior
                    nuevas_infecciones.append((floor_num + 1, 0))

        # Añadir zombis a las nuevas habitaciones
        for floor_num, room_num in nuevas_infecciones:
            room = self.building.floors[floor_num].rooms[room_num]
            if not room.has_zombies and not room.is_blocked:
                room.add_zombies()
                print(f"🧟 Zombis han infectado Piso {floor_num}, Habitación {room_num}")

    def clean_room(self, floor_num, room_num):
        # Limpiar una habitación (eliminar zombis)
        room = self.building.floors[floor_num].rooms[room_num]
        if room.has_zombies:
            room.remove_zombies()
            print(f"🧼 Habitación {room_num} del piso {floor_num} ha sido limpiada.")
        else:
            print(f"La habitación {room_num} del piso {floor_num} no tiene zombis.")

    def reset_sensor(self, floor_num, room_num):
        # Resetear el sensor de una habitación
        room = self.building.floors[floor_num].rooms[room_num]
        if not room.has_zombies:
            room.reset_sensor()
            print(f"🔄 Sensor de la habitación {room_num} del piso {floor_num} ha sido reseteado.")
        else:
            print(f"No se puede resetear el sensor: la habitación {room_num} del piso {floor_num} tiene zombis.")

    def run_simulation(self):
        if not self.building:
            print("El edificio aún no ha sido configurado.")
            return

        while not self.building.is_fully_infected():
            print(f"\n--- Turno {self.turn_count + 1} ---")
            self.show_status()
            self.advance_turn()
            time.sleep(1)  # Pausa de 1 segundo entre turnos

        print("\n¡El edificio está completamente infectado!")
        self.show_status()


# Función principal
def main():
    simulacion = Simulation()
    while True:
        print("\n--- Simulación de Edificio con Zombis ---")
        print("1. Configurar edificio")
        print("2. Mostrar estado del edificio")
        print("3. Avanzar turno")
        print("4. Bloquear habitación")
        print("5. Desbloquear habitación")
        print("6. Limpiar habitación")
        print("7. Resetear sensor")
        print("8. Guardar estado")
        print("9. Cargar estado")
        print("10. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            num_pisos = int(input("Ingresa el número de pisos: "))
            habitaciones_por_piso = int(input("Ingresa el número de habitaciones por piso: "))
            simulacion.setup_building(num_pisos, habitaciones_por_piso)
        elif opcion == "2":
            simulacion.show_status()
        elif opcion == "3":
            simulacion.advance_turn()
        elif opcion == "4":
            piso = int(input("Ingresa el número de piso: "))
            habitacion = int(input("Ingresa el número de habitación: "))
            if 0 <= piso < len(simulacion.building.floors):
                piso_obj = simulacion.building.floors[piso]
                if 0 <= habitacion < len(piso_obj.rooms):
                    simulacion.building.floors[piso].rooms[habitacion].block_room()
                    print(f"🚫 Habitación {habitacion} del piso {piso} ha sido bloqueada.")
            else:
                print("Habitación o piso inválido. Por favor, intenta de nuevo.")
                simulacion.show_status()

        elif opcion == "5":
            piso = int(input("Ingresa el número de piso: "))
            habitacion = int(input("Ingresa el número de habitación: "))
            if 0 <= piso < len(simulacion.building.floors):
                piso_obj = simulacion.building.floors[piso]
                if 0 <= habitacion < len(piso_obj.rooms):
                    simulacion.building.floors[piso].rooms[habitacion].unblock_room()
                    print(f"✅ Habitación {habitacion} del piso {piso} ha sido desbloqueada.")
            else:
                print("Habitación o piso inválido. Por favor, intenta de nuevo.")
                simulacion.show_status
        elif opcion == "6":
            piso = int(input("Ingresa el número de piso: "))
            habitacion = int(input("Ingresa el número de habitación: "))
            if 0 <= piso < len(simulacion.building.floors):
                piso_obj = simulacion.building.floors[piso]
                if 0 <= habitacion < len(piso_obj.rooms):
                    simulacion.clean_room(piso, habitacion)
            else:
                print("Habitación o piso inválido. Por favor, intenta de nuevo.")
                simulacion.show_status()
        elif opcion == "7":
            piso = int(input("Ingresa el número de piso: "))
            habitacion = int(input("Ingresa el número de habitación: "))
            if 0 <= piso < len(simulacion.building.floors):
                piso_obj = simulacion.building.floors[piso]
                if 0 <= habitacion < len(piso_obj.rooms):
                    simulacion.reset_sensor(piso, habitacion)
            else:
                print("Habitación o piso inválido. Por favor, intenta de nuevo.")
                simulacion.show_status()
        elif opcion == "8":
            filename = input("Ingresa el nombre del archivo para guardar: ")
            simulacion.building.save_state(filename)
        elif opcion == "9":  
            filename = input("Ingresa el nombre del archivo para cargar: ")
            if simulacion.building is None:
                simulacion.building = Building(1, 1) 
            simulacion.building.load_state(filename)
            simulacion.turn_count = 0  
            print("Estado cargado correctamente. La simulación ha sido sobrescrita.")
        elif opcion == "10":
            print("Saliendo de la simulación. ¡Adiós!")
            break
        else:
            print("Opción inválida. Por favor, intenta de nuevo.")


if __name__ == "__main__":
    main()
    
    
    
