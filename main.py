import random
from operacoesbd import *
import os

def limparTela():
        # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

tipoManifestacao = ["Reclamação", "Sugestão", "Elogio"]
voltarMenu = 0
opcao = 0

conexao = criarConexao('127.0.0.1', 'root', '12345', 'ouvidoria')

while opcao != 7:
    limparTela()
    print(30 * "-=")
    print("Bem-vindo ao Sistema de Ouvidoria da UniPython\n")
    print("Menu:\n")
    print("1. Criar nova manifestação")  
    print("2. Listar manifestações")
    print("3. Listar manifestações por tipo")
    print("4. Exibir quantidade de manifestações")
    print("5. Pesquisar uma manifestação por código")
    print("6. Excluir uma manifestação pelo código")
    print("7. Sair")
    print(30 * "-=")
    opcao = int(input("\nEscolha uma opção: "))

    if opcao == 1:
        limparTela()
        listaManif = listarBancoDados(conexao, 'SELECT * FROM ouvidoriapy')
        print("Escolha um tipo de manifestação que deseja abrir:")
        print("\n1 - Reclamação\n2 - Sugestão\n3 - Elogio\n4 - Voltar ao menu")
        while True:
            op = int(input("\nEscolha uma opção (1-4): "))
            if 1 <= op <= 4:
                break
            else:
                print("Por favor, insira um número válido entre 1 e 4.")
        if not op == 4:
            novaManifestacao = input("\nDigite uma nova manifestação:\n")
            codigo = random.randint(100, 999)
            listaCodigo = listarBancoDados(conexao, 'SELECT codigo FROM ouvidoriapy')
            while True:
                # Gera um código único para a manifestação
                codigo = random.randint(100, 999)
                if codigo not in listaCodigo: #Se este codigo não estiver, ele salva. Pq n pode ter numero repetido(chave primaria)
                    dados = [codigo, tipoManifestacao[op - 1], novaManifestacao] #Declarei os dados como Lista, pra que possa ser colcoado como parametro da prox linha
                    insertNoBancoDados(conexao, 'INSERT INTO ouvidoriapy VALUES(%s,%s,%s)', dados) 
                    break
            limparTela()
            print(30 * "-=")
            print("Sua manifestação foi salva. Seu protocolo é: ", codigo)
            print(30 * "-=")
            while voltarMenu != 1:
                voltarMenu = int(input("Digite o número 1 para voltar ao menu principal: "))
                limparTela()
            voltarMenu = 0 
    if opcao == 2:
        listaManif = listarBancoDados(conexao, 'SELECT * FROM ouvidoriapy')
        limparTela()
        print("\nLista de manifestações:")
        if len(listaManif) != 0:
            for manifestacao in listaManif:
                print(30 * "-=")
                print("Protocolo:", manifestacao[0], "\nTipo de Manifestação:", manifestacao[1],"\nManifestacao: ",manifestacao[2],"\n")
        else:
            print("\n", 30 * "-=")
            print("Não há manifestações em aberto")
            print(30 * "-=")
        while voltarMenu != 1:
            voltarMenu = int(input("Digite o número 1 para voltar ao menu principal: ")) 
        voltarMenu = 0
    if opcao == 3:
        limparTela()
        print("Escolha um tipo de manifestação que deseja listar:")
        print("\n1 - Reclamação\n2 - Sugestão\n3 - Elogio\n4 - Voltar ao menu")
        while True:
            op = int(input("\nEscolha uma opção (1-4): "))
            if 1 <= op <= 4:
                break
            else:
                print("Por favor, insira um número válido entre 1 e 4.")
        limparTela()
        if not op == 4:
            listTipo = listarBancoDados(conexao, 'SELECT * FROM ouvidoriapy WHERE tipoManifestacao =' + "'" + tipoManifestacao[op-1] + "'")
            if len(listTipo) >= 1:
                for manifestacao in listTipo:
                    print(30 * "-=")
                    print("Protocolo:", manifestacao[0], "\nTipo de Manifestação:", manifestacao[1],"\nManifestacao: ",manifestacao[2])
            else:
                print(30 * "-=")
                print("Não há mais manifestações em aberto")
            while voltarMenu != 1:
                voltarMenu = int(input("\nDigite o número 1 para voltar ao menu principal: "))
            voltarMenu = 0
        limparTela()        
    if opcao == 4:
        qtdManif = listarBancoDados(conexao, 'SELECT COUNT(codigo) FROM ouvidoriapy')
        qtdManif = qtdManif[0][0]
        limparTela()
        if qtdManif == 1:
            print(30 * "-=")
            print("Há ", qtdManif, " manifestação em aberto")
            print(30 * "-=")
        elif qtdManif > 1: 
            print(30 * "-=")
            print("Há ", qtdManif, " manifestações em aberto")
            print(30 * "-=")
        elif qtdManif == 0:
            print(30 * "-=")
            print("Não há manifestações em aberto")
            print(30 * "-=")
        while voltarMenu != 1:
            voltarMenu = int(input("\nDigite o número 1 para voltar ao menu principal: "))
        voltarMenu = 0
        limparTela()
    if opcao == 5:
        limparTela()
        listaManif = listarBancoDados(conexao, 'SELECT * FROM ouvidoriapy')
        codigo = int(input("Digite o número do seu protocolo (apenas números): \n"))
        encontrado = False
        for manifestacao in listaManif:
            if codigo == manifestacao[0]:
                encontrado = True
                print(30 * "-=")
                print("Encontrado!\n\nProtocolo:", manifestacao[0], "\nTipo de Manifestação:", manifestacao[1],"\nManifestacao: ",manifestacao[2],"\n")
                print(30 * "-=")
                break
        if encontrado == False:
            print(30 * "-=")
            print("Não encontramos seu protocolo")   
            print(30 * "-=")
        while voltarMenu != 1:
            voltarMenu = int(input("\nDigite o número 1 para voltar ao menu principal: "))
        voltarMenu = 0
        limparTela()
    if opcao == 6:
        limparTela()
        listaManif = listarBancoDados(conexao, 'SELECT * FROM ouvidoriapy')

        #Listar todos os codigos abaixo
        if len(listaManif) != 0:
            for manifestacao in listaManif:
                print(30 * "-=")
                print("Protocolo:", manifestacao[0], "\nTipo de Manifestação:", manifestacao[1],"\nManifestacao: ",manifestacao[2],"\n")
        #Listar todos os codigos acima

        codigo = int(input("Digite o número do protocolo que queira excluir: "))
        print("")
        procurarCodigo = listarBancoDados(conexao, "SELECT codigo FROM ouvidoriapy WHERE codigo =" + str(codigo))
        if procurarCodigo and procurarCodigo[0][0] == codigo:
            atualizarBancoDados(conexao, "DELETE FROM ouvidoriapy WHERE codigo = (%s)", (codigo,))
            print("Protocolo ", codigo,"excluido com sucesso")
        else:
            print("Protocolo não encontrado")
        while voltarMenu != 1:
            voltarMenu = int(input("\nDigite o número 1 para voltar ao menu principal: "))
        voltarMenu = 0
    if opcao == 7:
        print(30 * "-=")
        encerrarBancoDados(conexao)
        print("Saindo do programa...")
