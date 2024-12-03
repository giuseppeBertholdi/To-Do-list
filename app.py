from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lê as tarefas passadas do arquivo
def ler_tarefas_passadas():
    try:
        with open('arquivoPassado.txt', 'r') as arquivo:
            return [linha.strip() for linha in arquivo.readlines()]
    except FileNotFoundError:
        return []

# Lê as tarefas atuais
def ler_tarefas_atuais():
    tarefas_atuais = []
    try:
        with open('arquivoAtuais.txt', 'r') as arquivo:
            tarefas_atuais = [linha.strip() for linha in arquivo.readlines()]
    except FileNotFoundError:
        pass
    return tarefas_atuais

@app.route('/')
def index():
    tarefas_passadas = ler_tarefas_passadas()  # Lê as tarefas passadas
    tarefas_atuais = ler_tarefas_atuais()  # Lê as tarefas atuais
    return render_template('index.html', tarefas_atuais=tarefas_atuais, tarefas_passadas=tarefas_passadas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nova_tarefa = request.form.get('tarefa')
    if nova_tarefa:
        # Adiciona a tarefa no arquivo de tarefas atuais
        with open('arquivoAtuais.txt', 'a') as arquivo:
            arquivo.write(nova_tarefa + '\n')
        # Também adiciona no arquivo de tarefas passadas
        with open('arquivoPassado.txt', 'a') as arquivo_passado:
            arquivo_passado.write(nova_tarefa + '\n')
    return redirect(url_for('index'))

@app.route('/remover', methods=['POST'])
def remover():
    tarefa = request.form['tarefa']
    
    # Lê as tarefas atuais
    tarefas_atuais = ler_tarefas_atuais()
    
    # Remove a tarefa da lista atual (não remove do arquivo de tarefas passadas)
    if tarefa in tarefas_atuais:
        tarefas_atuais.remove(tarefa)
        
        # Reescreve as tarefas atuais no arquivo de tarefas atuais
        with open('arquivoAtuais.txt', 'w') as arquivo:
            for t in tarefas_atuais:
                arquivo.write(t + '\n')

    return redirect(url_for('index'))

@app.route('/apagarConteudo', methods=['POST'])
def apagar_conteudo():
    try:
        # Abre o arquivo em modo de escrita e apaga o conteúdo
        with open('arquivoPassado.txt', 'w') as arquivo:
            # Não escreve nada no arquivo, assim ele será limpo
            pass
        return redirect(url_for('index'))  # Redireciona de volta para a página inicial ou outra
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"
    
if __name__ == '__main__':
    app.run(debug=True)
