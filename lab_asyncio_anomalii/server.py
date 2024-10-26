import asyncio
import statistics

# Configurații server
HOST = '127.0.0.1'  # IP-ul serverului
PORT = 12345        # Portul serverului

# Variabile globale
reference_values = []  # Primele 10 valori considerate corecte

# Funcția de detectare a anomaliei
def is_anomalous(value, reference_values):
    mean = statistics.mean(reference_values)
    stdev = statistics.stdev(reference_values) if len(reference_values) > 1 else 0
    threshold = 3  # De exemplu, o anomalie este definită ca o valoare în afara a 3 deviații standard

    # Verificăm dacă valoarea este în afara limitelor de 3 stdev
    if abs(value - mean) > threshold * stdev:
        return True
    return False

# Handler pentru fiecare client
async def handle_client(reader, writer):
    global reference_values

    # Buclă pentru a primi date de la client
    while True:
        try:
            data = await reader.read(100)
            if not data:
                break

            # Prelucrează valoarea primită
            value = float(data.decode().strip())
            print(f"Valoare primită: {value}")

            # Detectare anomalie
            if len(reference_values) < 10:
                reference_values.append(value)
                print(f"Valoarea {value} a fost adăugată la referințe inițiale.")
            else:
                if is_anomalous(value, reference_values):
                    print(f"Anomalie detectată: {value}")
                else:
                    # Dacă valoarea nu este o anomalie, o adăugăm la referințe pentru verificări viitoare
                    reference_values.pop(0)
                    reference_values.append(value)

            # Așteaptă puțin pentru a simula verificările
            await asyncio.sleep(0.1)

        except ValueError as e:
            print("Eroare la conversia valorii primite:", e)
            continue

    # Închide conexiunea cu clientul
    writer.close()
    await writer.wait_closed()
    print("Conexiune închisă cu clientul.")

# Funcția principală a serverului
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Server pornit pe {addr}")

    # Rulează serverul până la închidere
    async with server:
        await server.serve_forever()

# Rulează serverul
if __name__ == '__main__':
    asyncio.run(main())
