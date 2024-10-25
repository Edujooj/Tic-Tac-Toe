from main import app
from flask import render_template, request, redirect, url_for, jsonify
from logica_do_jogo import logica_do_jogo

logica_do_jogo = logica_do_jogo(True, logica_do_jogo.criar_matriz_jogador(), 1)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/update_game', methods=['POST'])
def update_game():
    informacao_celula = request.get_json()  # Pega os dados enviados pelo fetch
    celula = informacao_celula.get('celula', [])
    
    celula_index = celula.index("aqui")
    jogada = logica_do_jogo.alocar_na_matriz(celula_index)

    if jogada != "N":
        ganhador = -1
        analise = logica_do_jogo.analisar_matriz(logica_do_jogo.posicao_na_matriz(jogada))

        if analise:
            ganhador = logica_do_jogo.turno
            print(f"Ganhador: {ganhador}")

        logica_do_jogo.alterar_turno()
        return  jsonify({'index': jogada,
                         'turno': logica_do_jogo.turno,
                         'ganhador': ganhador,
                         'analise': analise,
                         'msg': True})
    return jsonify({'msg': False})

@app.route('/reiniciar_partida')
def reiniciar_partida():
    logica_do_jogo.reiniciar_partida()
    return redirect(url_for('index'))