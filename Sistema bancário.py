from datetime import datetime


class ContaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.saldo = saldo_inicial
        self.extrato = []
        self.saques_diarios = {}
        self.LIMITE_SAQUE_DIARIO = 500.00
        self.MAX_SAQUES_DIARIOS = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"{datetime.now()} - Depósito: +R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido. Tente novamente.")

    def pode_sacar(self, valor):
        hoje = datetime.now().date()
        if hoje not in self.saques_diarios:
            self.saques_diarios[hoje] = {'valor_total': 0, 'quantidade': 0}
        saques_hoje = self.saques_diarios[hoje]
        if saques_hoje['quantidade'] >= self.MAX_SAQUES_DIARIOS:
            print("Número máximo de saques diários atingido.")
            return False
        if saques_hoje['valor_total'] + valor > self.LIMITE_SAQUE_DIARIO:
            print("Limite diário de saque excedido.")
            return False
        return True

    def registrar_saque(self, valor):
        hoje = datetime.now().date()
        self.saques_diarios[hoje]['valor_total'] += valor
        self.saques_diarios[hoje]['quantidade'] += 1

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            if self.pode_sacar(valor):
                self.saldo -= valor
                self.registrar_saque(valor)
                self.extrato.append(f"{datetime.now()} - Saque: -R${valor:.2f}")
                print(f"Saque de R${valor:.2f} realizado com sucesso.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        else:
            print("Valor de saque inválido. Tente novamente.")

    def ver_extrato(self):
        print(f"\nExtrato da conta de {self.titular}:")
        for transacao in self.extrato:
            print(transacao)
        print(f"Saldo atual: R${self.saldo:.2f}\n")


# Função para validar entradas numéricas
def obter_valor_positivo(prompt):
    while True:
        try:
            valor = float(input(prompt))
            if valor > 0:
                return valor
            else:
                print("Por favor, insira um valor positivo.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")


# Função principal para interagir com o usuário
def sistema_bancario():
    titular = input("Digite o nome do titular da conta: ")
    saldo_inicial = obter_valor_positivo("Digite o saldo inicial da conta: ")
    conta = ContaBancaria(titular, saldo_inicial)

    while True:
        print("\nEscolha uma operação:")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Ver Extrato")
        print("4. Sair")

        opcao = input("Digite a opção desejada (1, 2, 3, 4): ")

        if opcao == '1':
            valor = obter_valor_positivo("Digite o valor a ser depositado: ")
            conta.depositar(valor)
        elif opcao == '2':
            valor = obter_valor_positivo("Digite o valor a ser sacado: ")
            conta.sacar(valor)
        elif opcao == '3':
            conta.ver_extrato()
        elif opcao == '4':
            print("Obrigado por usar o nosso banco,volte sempre :)!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Iniciar o sistema bancário
sistema_bancario()
