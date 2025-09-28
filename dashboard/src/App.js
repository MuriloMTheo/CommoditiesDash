import React, { useEffect, useState} from "react";
import { Line } from "react-chartjs-2";
import api from "./services/api";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App(){
  const[chartData, setChartData] = useState({
    labels:[],
    datasets: [],
  }); 
  const [CulturaSelecionada, setCulturaSelecionada] = useState(null);
  const [ultimoRegistro, setUltimoRegistro] = useState(null);

useEffect(() => {
  api.get("")
    .then(res => {
      console.log("Resposta da API:", res.data);
      const dados = res.data;

      if (!Array.isArray(dados)) {
      console.error("Dados da API não estão em formato esperado", dados);
      return;
      }

      const dadosFiltrados = CulturaSelecionada
      ? dados.filter(item => item.nome === CulturaSelecionada)
      : dados;
      const dadosOrdenados = [...dadosFiltrados].sort((a,b) => new Date(a.data_hora) - new Date(b.data_hora));
      const labels = dadosOrdenados.map(item => `${item.data_hora.substring(0, 10)}`);
      const valores = dadosOrdenados.map(item => item.valor_atual/100);
      const valoresFormatados = valores.map(val => (val /  100).toLocaleString("en-US",{ style: "currency", currency: "USD" }));
      
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
            fill: false,
          },
        ],
      });
      console.log("Labels:", labels);
      console.log("Valores formatados:", valoresFormatados);
    })
    .catch(err => console.log("Erro ao buscar dados:", err));
}, [CulturaSelecionada]);

  const options = 
    {
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
  <div className="dashboard-container">
    {}
    <div className="dashboard-title">
      <h2>Commodities</h2>
    </div>

    {}
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
        "Madeira Serrada"
      ].map(nome => (
        <button 
          key={nome} 
          onClick={() => setCulturaSelecionada(nome)}
          className={`botao-cultura ${CulturaSelecionada === nome ? "selecionado" : ""}`}
        >
          {nome}
        </button>
      ))}
    </div>

    <div class="cultura-container">
      <div class="cultura-titulo">{CulturaSelecionada ? CulturaSelecionada: "Selecione uma Cultura"}</div>
      
      <div class="cultura-valorcard">
        <div class="valor-item1">
          <div class="cultura-valortitle1">COTAÇÃO ATUAL</div>
          <div class="cultura-valoratual">{CulturaSelecionada && ultimoRegistro ? `$${ultimoRegistro.valor_atual/100}`: "-"}</div>
        </div>
        <div class="valor-item2">
          <div class="cultura-valortitle2">COTAÇÃO MÁXIMA</div>
          <div class="cultura-valormax">{CulturaSelecionada && ultimoRegistro ? `$${ultimoRegistro.valor_maximo/100}`: "-"}</div>
        </div>
        <div class="valor-item3">
          <div class="cultura-valortitle3">COTAÇÃO MÍNIMA</div>
          <div class="cultura-valormin">{CulturaSelecionada && ultimoRegistro ? `$${ultimoRegistro.valor_minimo/100}`: "-"}</div>
        </div>
        <div class="valor-item4">
          <div class="cultura-valortitle4">VARIAÇÃO</div>
          <div class="cultura-variacao">{CulturaSelecionada && ultimoRegistro ? `${ultimoRegistro.variacao > 0 ? "+" : ""} ${(ultimoRegistro.variacao/100).toFixed(2)}`: "-"}</div>
        </div>
        <div class="valor-item5">
          <div class="cultura-valortitle5">% VARIAÇÃO</div>
          <div class={`cultura-porcentagemvar ${CulturaSelecionada && ultimoRegistro ? ultimoRegistro.porcentagem_var.replace("%", "") >= 0 ? "positivo":"negativo": ""}`}>
            {CulturaSelecionada && ultimoRegistro ? (parseFloat(ultimoRegistro.porcentagem_var.replace("%", "")) / 100).toFixed(2)+"%": "-"}
          </div>
        </div>
      </div>

    </div>

    {}
    <div className="grafico-container">
       {chartData.labels.length > 0 ? (
        <Line data={chartData} options={options} />
       ) : (
      <p>Selecione uma cultura</p>  )}
    </div>
  </div>
);

}

export default App;