# 🌦️ Estação Meteorológica

Sistema de monitoramento meteorológico desenvolvido como projeto acadêmico da UNIP. A aplicação recebe dados enviados por uma estação baseada em ESP32, armazena as medições em um banco de dados SQLite e apresenta as informações em uma interface web.

## 📌 Funcionalidades

- Recebimento de medições por requisições HTTP.
- Armazenamento dos dados no banco SQLite.
- Exibição da última medição registrada.
- Atualização automática da tela principal a cada 2 segundos.
- Consulta do histórico das últimas 100 medições.
- Validação dos dados recebidos pela API.

## 🧰 Tecnologias utilizadas

- **Python** — linguagem utilizada no servidor.
- **Flask** — criação da aplicação e das rotas da API.
- **Flask-CORS** — configuração de acesso entre origens.
- **SQLite** — armazenamento das medições.
- **HTML5** — estrutura das páginas.
- **CSS3** — estilização e responsividade.
- **JavaScript** — comunicação com a API e atualização das informações.
- **ESP32** — dispositivo responsável pelo envio das medições.

## 📁 Estrutura do projeto

```text
Projeto-2-Unip-termodin-mica-/
├── app.py             # Servidor Flask e API
├── estacao.db         # Banco de dados SQLite
├── estacao.sqbpro     # Arquivo do projeto do banco
├── index.html         # Painel principal
├── historico.html     # Página de histórico
├── script.js          # Atualização dos dados do painel
├── historico.js       # Consulta e exibição do histórico
├── style.css          # Estilos das páginas
└── README.md          # Documentação do projeto
```

## ⚙️ Como executar

### 1. Pré-requisitos

Tenha o Python 3 instalado. É recomendado utilizar um ambiente virtual.

### 2. Instale as dependências

No terminal, dentro da pasta do projeto, execute:

```bash
python -m venv .venv
```

No Windows, ative o ambiente virtual:

```bash
.venv\Scripts\activate
```

Instale as bibliotecas necessárias:

```bash
pip install Flask flask-cors
```

### 3. Inicie o servidor

Execute:

```bash
python app.py
```

Por padrão, o Flask inicia na porta **5000**.

### 4. Acesse a interface

Com o servidor em execução, abra o arquivo `index.html` no navegador. A página principal consulta a API para exibir a última medição, enquanto a página `historico.html` apresenta os registros armazenados.

> **Importante:** os arquivos JavaScript estão configurados para acessar `http://127.0.0.1:5000`. Esse endereço funciona quando o navegador e o servidor estão na mesma máquina. Para acessar de outro dispositivo ou receber dados do ESP32 pela rede, substitua o endereço pelo IP da máquina que executa o Flask, mantendo a porta 5000.

## 🔌 API

O servidor disponibiliza as seguintes rotas:

| Método | Rota | Descrição |
|---|---|---|
| POST | `/dados` | Recebe e armazena uma nova medição. |
| GET | `/dados` | Retorna a medição mais recente. |
| GET | `/historico` | Retorna as últimas 100 medições. |

### Dados recebidos

A rota `POST /dados` espera um JSON com os campos numéricos:

```json
{
  "temperatura": 25.5,
  "umidade": 60.0,
  "pressao": 1013.2,
  "qualidade_ar": 120,
  "luminosidade": 450,
  "pluviometria": 0.0
}
```

A API valida os campos antes de registrar a medição. Os campos `qualidade_ar` e `luminosidade` devem ser números inteiros.

## 🔄 Funcionamento geral

1. O ESP32 realiza as leituras dos sensores.
2. Os dados são enviados ao servidor Flask por uma requisição HTTP.
3. O servidor valida as informações recebidas.
4. As medições são armazenadas no banco SQLite com data e hora.
5. A interface web consulta a API e apresenta os dados atualizados.
6. A página de histórico permite consultar os registros anteriores.

## 🎯 Objetivo

O projeto tem como objetivo aplicar conhecimentos de desenvolvimento web, programação em Python, comunicação entre dispositivos, criação de APIs e persistência de dados, integrando hardware e software em uma solução de monitoramento meteorológico.

---

**Projeto acadêmico — Ciência da Computação | UNIP**
