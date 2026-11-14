
const SERVIDOR = "http://127.0.0.1:5000/dados";

async function atualizarDados() {

    try {

        const resposta = await fetch(SERVIDOR);

        if (!resposta.ok) {
            throw new Error("Erro na comunicação com o servidor");
        }

        const dados = await resposta.json();

        // Verifica se existem medições cadastradas
        if (!dados || !dados.id_leitura) {
            document.getElementById("conexao").innerText =
                "Servidor conectado, aguardando medições";

            document.getElementById("conexao").style.color = "orange";

            return;
        }

        // Atualiza os seis sensores
        document.getElementById("temperatura").innerText =
            dados.temperatura + " °C";

        document.getElementById("umidade").innerText =
            dados.umidade + " %";

        document.getElementById("pressao").innerText =
            dados.pressao + " hPa";

        document.getElementById("qualidade_ar").innerText =
            dados.qualidade_ar;

        document.getElementById("luminosidade").innerText =
            dados.luminosidade + " lux";

        document.getElementById("pluviometria").innerText =
            dados.pluviometria + " mm";

        // Status da conexão
        document.getElementById("conexao").innerText =
            "Conectado";

        document.getElementById("conexao").style.color = "green";

        // Horário registrado no banco
        document.getElementById("atualizacao").innerText =
            dados.data_hora || "--";

    } catch (erro) {

        document.getElementById("conexao").innerText =
            "Sem conexão com o servidor";

        document.getElementById("conexao").style.color = "red";

        console.error("Erro ao receber dados:", erro);

    }

}

// Busca os dados imediatamente
atualizarDados();

// Atualiza automaticamente a cada 2 segundos
setInterval(atualizarDados, 2000);
