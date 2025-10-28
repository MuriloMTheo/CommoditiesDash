import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import api from "./services/api";
import { Sidebar, Menu, MenuItem } from "react-pro-sidebar";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function BotaoSelectData({ opcoesBotao, indice, setIndice }) {
  const handleChange = (event) => {
    setIndice(Number(event.target.value));
  };

  return (
    <select value={indice} onChange={handleChange}>
      {opcoesBotao.map((opcao, i) => (
        <option key={i} value={i}>
          {opcao}
        </option>
      ))}
    </select>
  );
}

function App() {
  const opcoesBotao = ["Tudo", "7 dias", "15 dias", "30 dias", "90 dias"];
  const [indice, setIndice] = useState(0); /*indices de 0-4*/
  const diasMap = { 0: 0, 1: 7, 2: 15, 3: 30, 4: 90 };

  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [],
  });
  const [CulturaSelecionada, setCulturaSelecionada] = useState(null);
  const [ultimoRegistro, setUltimoRegistro] = useState(null);

  useEffect(() => {
    const QntDiaSelecionado = diasMap[indice];
    api
      .get("", {
        params: {
          dias: QntDiaSelecionado,
        },
      })
      .then((res) => {
        console.log("Resposta da API:", res.data);
        const dados = res.data;

        if (!Array.isArray(dados)) {
          console.error("Dados da API não estão em formato esperado", dados);
          return;
        }

        const dadosFiltrados = CulturaSelecionada
          ? dados.filter((item) => item.nome === CulturaSelecionada)
          : dados;
        const dadosOrdenados = [...dadosFiltrados].sort(
          (a, b) => new Date(a.data_hora) - new Date(b.data_hora)
        );
        const labels = dadosOrdenados.map(
          (item) => `${item.data_hora.substring(0, 10)}`
        );
        const valores = dadosOrdenados.map((item) => item.valor_atual / 100);
        const valoresFormatados = valores.map((val) =>
          (val / 100).toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
          })
        );

        const ultimo = dadosOrdenados[dadosOrdenados.length - 1];
        setUltimoRegistro(ultimo);

        setChartData({
          labels,
          datasets: [
            {
              label: "Preço do Commodity",
              data: CulturaSelecionada ? valores : [],
              borderColor: "rgba(30, 216, 216, 0.5)",
              backgroundColor: "rgba(20, 117, 117, 0.5)",
              fill: true,
              tension: 0.1,
            },
          ],
        });
        console.log("Labels:", labels);
        console.log("Valores formatados:", valoresFormatados);
      })
      .catch((err) => console.log("Erro ao buscar dados:", err));
  }, [CulturaSelecionada, indice]);

  const options = {
    type: "line",
    responsive: true,
    maintainAspectRatio: false, //toda div no grafico
    plugins: {
      legend: {
        labels: {
          color: "#ffffff",
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#ffffff", // cor dos labels do eixo X
        },
        grid: {
          color: "rgba(255,255,255,0.1)", //grid X
        },
      },
      y: {
        ticks: {
          color: "#ffffff",
        },
        grid: {
          color: "rgba(255,255,255,0.1)", //grid y
        },
      },
    },
  };

  return (
    <div className="dashboard-layout">
      {/* Faixa lateral */}
      <Sidebar
        backgroundColor="#0c0c18"
        color="white"
        width="200px"
        height="101vh"
        className="sidebar"
        hoverBgColor="#1ed8d8"
      >
        <Menu>
          <MenuItem>Dashboard</MenuItem>
          <MenuItem>Relatórios</MenuItem>
          <MenuItem>Configurações</MenuItem>
        </Menu>
      </Sidebar>

      {/* Conteúdo principal do dashboard */}
      <div className="dashboard-main">
        {/* Título */}
        <div className="dashboard-title">
          <h2>Commodities</h2>
        </div>

        {/* Conteúdo */}
        <div className="dashboard-container">
          {/* Botões */}
          <div className="botao-container">
            {[
              "Cacau de Londres",
              "Café Londres",
              "Açúcar Londres",
              "Cacau NY",
              "Suco de Laranja NY",
              "Açúcar NY nº11",
              "Café Contrato C",
              "Algodão nº2",
              "Madeira Serrada",
            ].map((nome) => (
              <button
                key={nome}
                onClick={() => setCulturaSelecionada(nome)}
                className={`botao-cultura ${
                  CulturaSelecionada === nome ? "selecionado" : ""
                }`}
              >
                {nome}
              </button>
            ))}
          </div>

          {/* Cards principais */}
          <div className="cultura-container">
            <div className="cultura-titulo">
              {CulturaSelecionada
                ? CulturaSelecionada
                : "Selecione uma Cultura"}
            </div>

            <div className="cultura-valorcard">
              <div className="valor-item1">
                <div className="cultura-valortitle1">COTAÇÃO ATUAL</div>
                <div className="cultura-valoratual">
                  {CulturaSelecionada && ultimoRegistro
                    ? `$${ultimoRegistro.valor_atual / 100}`
                    : "-"}
                </div>
              </div>
              <div className="valor-item2">
                <div className="cultura-valortitle2">COTAÇÃO MÁXIMA</div>
                <div className="cultura-valormax">
                  {CulturaSelecionada && ultimoRegistro
                    ? `$${ultimoRegistro.valor_maximo / 100}`
                    : "-"}
                </div>
              </div>
              <div className="valor-item3">
                <div className="cultura-valortitle3">COTAÇÃO MÍNIMA</div>
                <div className="cultura-valormin">
                  {CulturaSelecionada && ultimoRegistro
                    ? `$${ultimoRegistro.valor_minimo / 100}`
                    : "-"}
                </div>
              </div>
            </div>
          </div>

          {/* Coluna de variações e datas */}
          <div className="cultura-container-coluna">
            <div className="valor-item6">
              <div className="cultura-valortitle6">DATA ÚLTIMA COTAÇÃO</div>
              <div className="cultura-diacotacao">
                {CulturaSelecionada && ultimoRegistro
                  ? `${ultimoRegistro.data_hora.substring(0, 10)}`
                  : "-"}
              </div>
            </div>
            <div className="valor-item4">
              <div className="cultura-valortitle4">VARIAÇÃO</div>
              <div className="cultura-variacao">
                {CulturaSelecionada && ultimoRegistro
                  ? `${ultimoRegistro.variacao > 0 ? "+" : ""} ${(
                      ultimoRegistro.variacao / 100
                    ).toFixed(2)}`
                  : "-"}
              </div>
            </div>
            <div className="valor-item5">
              <div className="cultura-valortitle5">% VARIAÇÃO</div>
              <div
                className={`cultura-porcentagemvar ${
                  CulturaSelecionada && ultimoRegistro
                    ? parseFloat(
                        ultimoRegistro.porcentagem_var.replace("%", "")
                      ) >= 0
                      ? "positivo"
                      : "negativo"
                    : ""
                }`}
              >
                {CulturaSelecionada && ultimoRegistro
                  ? (
                      parseFloat(
                        ultimoRegistro.porcentagem_var.replace("%", "")
                      ) / 100
                    ).toFixed(2) + "%"
                  : "-"}
              </div>
            </div>
          </div>

          {/* Gráfico */}
          <div className="grafico-container">
            {chartData.labels.length > 0 ? (
              <Line data={chartData} options={options} />
            ) : (
              <p>Selecione uma cultura</p>
            )}
          </div>

          {/* Botão de seleção de datas */}
          <BotaoSelectData
            opcoesBotao={opcoesBotao}
            indice={indice}
            setIndice={setIndice}
          />

          {/* Título evolução */}
          <div className="SelecaoData-container">
            <h3>Evolução de {opcoesBotao[indice]}</h3>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
