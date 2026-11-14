
const SERVIDOR = "http://127.0.0.1:5000/historico";

async function carregarHistorico() {
    const tabela = document.getElementById("tabela-historico");
    const status = document.getElementById("status");

    try {
        const resposta = await fetch(SERVIDOR);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar o histórico");
        }

        const dados = await resposta.json();

        tabela.innerHTML = "";

        if (!Array.isArray(dados) || dados.length === 0) {
            tabela.innerHTML = `
                <tr>
                    <td colspan="7">Nenhuma medição encontrada.</td>
                </tr>
            `;

            status.innerText = "Nenhum registro disponível.";
            return;
        }

        dados.forEach(leitura => {
            const linha = document.createElement("tr");

            const data = leitura.data_hora
                ? new Date(leitura.data_hora.replace(" ", "T"))
                    .toLocaleString("pt-BR")
                : "--";

            linha.innerHTML = `
                <td>${data}</td>
                <td>${leitura.temperatura ?? "--"} °C</td>
                <td>${leitura.umidade ?? "--"} %</td>
                <td>${leitura.pressao ?? "--"} hPa</td>
                <td>${leitura.qualidade_ar ?? "--"}</td>
                <td>${leitura.luminosidade ?? "--"} lux</td>
                <td>${leitura.pluviometria ?? "--"} mm</td>
            `;

            tabela.appendChild(linha);
        });

        status.innerText = `Foram encontrados ${dados.length} registros.`;

    } catch (erro) {
        tabela.innerHTML = `
            <tr>
                <td colspan="7">Não foi possível carregar o histórico.</td>
            </tr>
        `;

        status.innerText = "Erro de conexão com o servidor.";
        console.error("Erro:", erro);
    }
}

carregarHistorico();
