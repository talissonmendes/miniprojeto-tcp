import socket
import threading
import json
import time
import random
from datetime import datetime


class CurrencyServer:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Cotações iniciais (em relação ao USD)
        self.rates = {
            "USD": 1.0,
            "BRL": 4.95,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 149.50,
            "CAD": 1.36,
            "AUD": 1.53,
            "CHF": 0.88,
            "CNY": 7.24,
            "MXN": 17.12,
        }

        self.lock = threading.Lock()
        self.running = True

    def start(self):
        """Inicia o servidor"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"[SERVIDOR] Iniciado em {self.host}:{self.port}")
        print(f"[SERVIDOR] Aguardando conexões...\n")

        # Thread para atualizar cotações periodicamente
        update_thread = threading.Thread(target=self.update_rates, daemon=True)
        update_thread.start()

        try:
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    print(f"[CONEXÃO] Nova conexão de {address}")

                    # Thread para cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True,
                    )
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        print(f"[ERRO] Erro ao aceitar conexão: {e}")
        except KeyboardInterrupt:
            print("\n[SERVIDOR] Encerrando...")
        finally:
            self.stop()

    def update_rates(self):
        """Atualiza as cotações periodicamente (simulação)"""
        while self.running:
            time.sleep(5)  # Atualiza a cada 5 segundos

            with self.lock:
                for currency in self.rates:
                    if currency != "USD":
                        # Variação aleatória entre -1% e +1%
                        variation = random.uniform(-0.01, 0.01)
                        self.rates[currency] *= 1 + variation

            print(
                f"[ATUALIZAÇÃO] Cotações atualizadas às {datetime.now().strftime('%H:%M:%S')}"
            )

    def handle_client(self, client_socket, address):
        """Gerencia as requisições de um cliente"""
        try:
            while True:
                data = client_socket.recv(1024).decode("utf-8").strip()

                if not data:
                    break

                print(f"[{address}] Comando recebido: {data}")

                # Processa o comando
                response = self.process_command(data)

                # Envia resposta
                client_socket.send(response.encode("utf-8"))

        except Exception as e:
            print(f"[ERRO] Erro ao processar cliente {address}: {e}")
        finally:
            client_socket.close()
            print(f"[DESCONEXÃO] Cliente {address} desconectado")

    def process_command(self, command):
        """Processa os comandos recebidos"""
        parts = command.split()

        if not parts:
            return "ERRO: Comando vazio\n"

        cmd = parts[0].upper()

        try:
            if cmd == "LIST":
                return self.cmd_list(parts)
            elif cmd == "RATE":
                return self.cmd_rate(parts)
            elif cmd == "CONVERT":
                return self.cmd_convert(parts)
            elif cmd == "QUIT":
                return "BYE\n"
            else:
                return f"ERRO: Comando desconhecido '{cmd}'\n"
        except Exception as e:
            return f"ERRO: {str(e)}\n"

    def cmd_list(self, parts):
        """Lista todas as moedas e suas cotações em relação a uma base"""
        base = "USD"
        if len(parts) > 1:
            base = parts[1].upper()

        with self.lock:
            if base not in self.rates:
                return f"ERRO: Moeda base '{base}' não encontrada\n"

            base_rate = self.rates[base]
            result = f"Cotações em relação a {base}:\n"
            result += "-" * 40 + "\n"

            for currency, rate in sorted(self.rates.items()):
                # Converte a taxa em relação à moeda base
                converted_rate = rate / base_rate
                result += f"{currency}: {converted_rate:.4f}\n"

            result += "-" * 40 + "\n"

        return result

    def cmd_rate(self, parts):
        """Retorna a taxa de câmbio entre duas moedas"""
        if len(parts) < 3:
            return "ERRO: Uso correto: RATE <origem> <destino>\n"

        origin = parts[1].upper()
        destination = parts[2].upper()

        with self.lock:
            if origin not in self.rates:
                return f"ERRO: Moeda de origem '{origin}' não encontrada\n"
            if destination not in self.rates:
                return f"ERRO: Moeda de destino '{destination}' não encontrada\n"

            # Calcula a taxa de conversão
            rate = self.rates[destination] / self.rates[origin]

        return f"TAXA: 1 {origin} = {rate:.4f} {destination}\n"

    def cmd_convert(self, parts):
        """Converte um valor de uma moeda para outra"""
        if len(parts) < 4:
            return "ERRO: Uso correto: CONVERT <origem> <destino> <valor>\n"

        origin = parts[1].upper()
        destination = parts[2].upper()

        try:
            value = float(parts[3])
        except ValueError:
            return "ERRO: Valor inválido\n"

        with self.lock:
            if origin not in self.rates:
                return f"ERRO: Moeda de origem '{origin}' não encontrada\n"
            if destination not in self.rates:
                return f"ERRO: Moeda de destino '{destination}' não encontrada\n"

            # Calcula a conversão
            rate = self.rates[destination] / self.rates[origin]
            converted = value * rate

        return f"CONVERSÃO: {value:.2f} {origin} = {converted:.2f} {destination}\n"

    def stop(self):
        """Encerra o servidor"""
        self.running = False
        self.socket.close()


if __name__ == "__main__":
    server = CurrencyServer()
    server.start()
