import datetime


class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco


class ContaCorrente:
    proximo_numero_conta = 1

    def __init__(self, usuario):
        self.agencia = '0001'
        self.numero_conta = ContaCorrente.proximo_numero_conta
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = []
        self.saques_diarios = {}
        self.LIMITE_SAQUE_DIARIO = 500.00
        self.MAX_SAQUES_DIARIOS = 3
        ContaCorrente.proximo_numero_conta += 1

    def pode_sacar(self, valor):
        hoje = datetime.date.today()
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

    def sacar(self, valor):
        if valor > 0 and self.saldo >= valor:
            if self.pode_sacar(valor):
                self.saldo -= valor
                self.extrato.append(f"{datetime.datetime.now()} - Saque: -R${valor:.2f}")
                self.saques_diarios[datetime.date.today()]['valor_total'] += valor
                self.saques_diarios[datetime.date.today()]['quantidade'] += 1
                print(f"Saque de R${valor:.2f} realizado com sucesso.")
            else:
                print("Operação de saque não permitida.")
        else:
            print("Saldo insuficiente ou valor de saque inválido.")

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"{datetime.datetime.now()} - Depósito: +R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido.")

    def ver_extrato(self):
        print("\nExtrato da conta:")
        for transacao in self.extrato:
            print(transacao)
        print(f"Saldo atual: R${self.saldo:.2f}\n")


class SistemaBancario:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        # Verifica se o CPF já está cadastrado
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                print("CPF já cadastrado. Não é possível cadastrar o usuário.")
                return

        # Extrai apenas os números do CPF
        cpf_numeros = ''.join(filter(str.isdigit, cpf))

        # Cria o usuário e o adiciona à lista de usuários
        usuario = Usuario(nome, data_nascimento, cpf_numeros, endereco)
        self.usuarios.append(usuario)
        print("Usuário cadastrado com sucesso.")
        return usuario

    def cadastrar_conta_corrente(self, cpf_usuario):
        # Busca o usuário pelo CPF
        usuario = None
        for u in self.usuarios:
            if u.cpf == cpf_usuario:
                usuario = u
                break

        if usuario is None:
            print(f"Usuário com CPF {cpf_usuario} não encontrado.")
            return None

        # Cria uma nova conta corrente para o usuário
        conta = ContaCorrente(usuario)
        self.contas.append(conta)
        print(f"Conta corrente cadastrada para o usuário {usuario.nome}.")
        return conta

    def buscar_conta_por_cpf(self, cpf):
        # Busca a conta corrente pelo CPF do usuário associado
        for conta in self.contas:
            if conta.usuario.cpf == cpf:
                return conta
        return None

    def buscar_usuario_por_cpf(self, cpf):
        # Busca um usuário pelo CPF
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None


# Função para validar a data de nascimento
def validar_data_nascimento(data):
    try:
        datetime.datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False


# Função para cadastrar um novo usuário
def cadastrar_novo_usuario(sistema_bancario):
    print("Cadastro de Novo Usuário")
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
    while not validar_data_nascimento(data_nascimento):
        print("Formato de data inválido. Use dd/mm/aaaa.")
        data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
    cpf = input("CPF (somente números): ")
    endereco = input("Endereço (formato: logradouro, nro - bairro - cidade/UF): ")

    usuario = sistema_bancario.cadastrar_usuario(nome, data_nascimento, cpf, endereco)
    return usuario


# Função para cadastrar uma nova conta corrente
def cadastrar_nova_conta_corrente(sistema_bancario):
    cpf = input("Digite o CPF do usuário para cadastrar a conta corrente: ")
    conta = sistema_bancario.cadastrar_conta_corrente(cpf)
    return conta


# Função principal para interação com o usuário
def menu_principal(sistema_bancario):
    while True:
        print("\nMenu Principal")
        print("1. Cadastrar Novo Usuário")
        print("2. Cadastrar Conta Corrente")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Ver Extrato")
        print("6. Sair")

        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            cadastrar_novo_usuario(sistema_bancario)
        elif opcao == '2':
            cadastrar_nova_conta_corrente(sistema_bancario)
        elif opcao == '3':
            cpf = input("Digite o CPF do usuário para realizar o depósito: ")
            conta = sistema_bancario.buscar_conta_por_cpf(cpf)
            if conta:
                valor = float(input("Digite o valor a ser depositado: "))
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")
        elif opcao == '4':
            cpf = input("Digite o CPF do usuário para realizar o saque: ")
            conta = sistema_bancario.buscar_conta_por_cpf(cpf)
            if conta:
                valor = float(input("Digite o valor a ser sacado: "))
                conta.sacar(valor)
            else:
                print("Conta não encontrada.")
        elif opcao == '5':
            cpf = input("Digite o CPF do usuário para ver o extrato: ")
            conta = sistema_bancario.buscar_conta_por_cpf(cpf)
            if conta:
                conta.ver_extrato()
            else:
                print("Conta não encontrada.")
        elif opcao == '6':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Iniciar o sistema bancário
sistema = SistemaBancario()
menu_principal(sistema)
