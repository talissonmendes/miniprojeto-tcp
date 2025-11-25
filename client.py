import socket
import sys


class CurrencyClient:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Conecta ao servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Conectado ao servidor {self.host}:{self.port}\n")
            return True
        except Exception as e:
            print(f"ERRO: Não foi possível conectar ao servidor: {e}")
            return False

    def send_command(self, command):
        """Envia um comando ao servidor e recebe a resposta"""
        try:
            self.socket.send(command.encode("utf-8"))
            response = self.socket.recv(4096).decode("utf-8")
            return response
        except Exception as e:
            print(f"ERRO: Falha na comunicação: {e}")
            return None

    def run(self):
        """Executa o cliente interativo"""
        if not self.connect():
            return
        print("-" * 50)
        print("SISTEMA DE COTAÇÕES DE MOEDAS")
        print("-" * 50)
        print("\nComandos disponíveis:")
        print("  LIST [moeda_base]          - Lista todas as cotações")
        print("  RATE <origem> <destino>    - Taxa de câmbio")
        print("  CONVERT <origem> <destino> <valor> - Converter valor")
        print("  QUIT                       - Sair")
        print("\nExemplos:")
        print("  LIST USD")
        print("  RATE BRL USD")
        print("  CONVERT USD BRL 100")
        print("-" * 50 + "\n")
        try:
            while True:
                command = input(">>> ").strip()
                if not command:
                    continue
                response = self.send_command(command)
                if response:
                    print(response)
                    if command.upper() == "QUIT":
                        break
                else:
                    print("Erro ao receber resposta do servidor")
                    break
        except KeyboardInterrupt:
            print("\n\nEncerrando cliente...")
        except Exception as e:
            print(f"ERRO: {e}")
        finally:
            self.close()

    def close(self):
        """Fecha a conexão"""
        if self.socket:
            self.socket.close()
            print("Conexão encerrada.")


if __name__ == "__main__":
    # Permite passar host e porta como argumentos
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

    client = CurrencyClient(host, port)
client.run()
