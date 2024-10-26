import socket
import math
import random
import time
import math

# Configurații pentru client
SERVER_HOST = '127.0.0.1'  # IP-ul serverului
SERVER_PORT = 12345        # Portul serverului
INTERVAL = 0.5             # Intervalul dintre trimiteri, în secunde

# Funcția pentru a genera valori conform f(x)
def generate_values():
    step = 0.5  # Step for each x value
    x = -math.pi
    values = []

    while x <= 8 * math.pi:
        # Calculate f(x) = |sin(x)| * e^(-sin(x))
        f_x = abs(math.sin(x)) * math.exp(-math.sin(x))
        values.append(f_x)  # Store f(x)
        x += step

    return values

# Funcția pentru a insera anomalii în valori
def insert_anomalies(values):
    anomalies = [-999, 9999, -8888]  # Exemplu de valori anormale
    anomaly_indices = random.sample(range(len(values)), 3)  # Alege 3 indici pentru anomalii
    for idx, anomaly in zip(anomaly_indices, anomalies):
        values[idx] = anomaly
    return values

# Funcția principală pentru client
def client_program():
    # Inițializează clientul
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Conectat la server.")

    try:
        # Generează și trimite valorile
        values = generate_values()
        values_with_anomalies = insert_anomalies(values)

        for value in values_with_anomalies:
            # Trimite valoarea curentă către server
            client_socket.sendall(f"{value:.2f}".encode())
            print(f"Trimis valoarea: {value:.2f}")

            # Așteaptă înainte de a trimite următoarea valoare
            time.sleep(INTERVAL)

    except Exception as e:
        print("Eroare:", e)
    finally:
        # Închide conexiunea
        client_socket.close()
        print("Conexiunea a fost închisă.")

# Rulează clientul
if __name__ == "__main__":
    client_program()
