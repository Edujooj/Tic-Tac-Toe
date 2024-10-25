document.addEventListener('DOMContentLoaded', () => { // ao carregar a pagina
    const listaPosicao = document.querySelectorAll('div.celula'); // pega todas as celulas através da classe 'celula'

    listaPosicao.forEach((cell, index) => { // para cada célula

        cell.addEventListener('click', () => { // adiciona um evento de clique
            const lista = Array.from(listaPosicao).map((celula, i) => { // cria uma lista que diferencia outras células da célula clicada
                return i === index ? "aqui" : "";
            });

            enviar(lista);
        });
    });
});


function enviar(celula) {
    fetch('/update_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ //criando o JSON
            celula: celula
        })
    })
        .then(envio => envio.json())
        .then(informacao => {
            if (informacao['msg']) {
                console.log(informacao['turno'] + " Jogou: " + informacao['index'])
                alterarCelula(informacao['index'], informacao['turno']);

                respostaContraJogador(informacao, celula)

                if (informacao['ganhador'] != -1) {
                    const toast = document.getElementById('toast');
                    const toastHeader = document.getElementById('toastHeader');
                    const msg = document.getElementById('texto');

                    if (informacao['ganhador'] == 0) {
                        msg.textContent = "Vitória";
                        toast.children[0].setAttribute('class', 'toast rounded-pill bg-light-subtle d-block');
                        toastHeader.children[0].setAttribute('class', 'bi bi-circle fs-4');
                        toastHeader.children[2].setAttribute('class', 'bi bi-circle fs-4');
                    } else if (informacao['ganhador'] == 1) {
                        msg.textContent = "Vitória";
                        toast.children[0].setAttribute('class', 'toast rounded-pill bg-light-subtle d-block');
                        toastHeader.children[0].setAttribute('class', 'bi bi-x-lg fs-4');
                        toastHeader.children[2].setAttribute('class', 'bi bi-x-lg fs-4');
                    }
                    const hr = document.getElementById('linha');
                    const tabuleiro = document.getElementById('tabuleiro');
                    const altura = tabuleiro.offsetHeight;
                    const largura = tabuleiro.offsetWidth;

                    if (informacao['analise'].includes("l")) {
                        let valorLinha = altura / 3;
                        let linha = parseInt(informacao["analise"].replace("l", ""));

                        let posicao = (valorLinha * (linha + 1) - 50 - 5 / 2); // 5/2 é referente a espessura
                        hr.setAttribute("style", "width:" + largura + "px; top: " + posicao + "px;");

                    } else if (informacao['analise'].includes("c")) {
                        let valorColuna = largura / 3;
                        let coluna = parseInt(informacao["analise"].replace("c", ""));

                        let posicao = (valorColuna * (coluna + 1) - 50) - 5 - 14 - (largura / 2) + 16;
                        hr.setAttribute("style", "width: " + altura + "px; top:" + ((altura / 2) - 6) + "px; left: " + posicao + "px; transform: rotate(90deg)");
                    } else if (informacao['analise'].includes("d")) {
                        let metadeAltura = altura / 2;

                        let hipotenusa = Math.sqrt((altura * altura) + (largura * largura));

                        let radiano = Math.atan(altura / largura);

                        hr.setAttribute("style", "width: " + hipotenusa + "px; top:" + metadeAltura +
                            "px; left: " + (((- altura / 2) / 2) + 14) + "px; transform: rotate(" + radiano + "rad)");
                    } else if (informacao['analise'].includes("i")) {
                        let metadeAltura = altura / 2;

                        let hipotenusa = Math.sqrt((altura * altura) + (largura * largura));

                        let radiano = Math.atan(altura / largura);

                        hr.setAttribute("style", "width: " + hipotenusa + "px; top:" + metadeAltura +
                            "px; right: " + (((- altura / 2) / 2) + 14) + "px; transform: rotate(" + (-radiano) + "rad)");
                    } else {
                        msg.textContent = "Empate";
                        toast.children[0].setAttribute('class', 'toast rounded-pill d-block');
                        toastHeader.setAttribute('class', 'toast-header rounded-pill p-0 px-2 bg-warning-subtle');
                        toastHeader.children[0].setAttribute('class', 'bi bi-x-circle fs-4');
                        toastHeader.children[2].setAttribute('class', 'bi bi-x-circle fs-4');
                    }
                }
            } else {
                window.alert("Algo deu errado\nPor favor, tente novamente!");
            }
        })
        .catch(erro => {
            console.error(erro);
        });
}

function respostaContraJogador(informacao, celula) {
    if (informacao['turno'] == 0 && informacao['analise'] != "e" && informacao['ganhador'] == -1) {
        enviar(celula);
    }
}

function alterarCelula(index, turno) {
    const listaPosicao = document.querySelectorAll('div.celula');

    if (turno == 0) {
        listaPosicao[index].children[0].setAttribute('class', 'bi bi-x-lg fs-3');
    } else {
        listaPosicao[index].children[0].setAttribute('class', 'bi bi-circle fs-3');
    }
}