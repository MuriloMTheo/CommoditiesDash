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
      const dadosOrdenados = [...dadosFiltrados].sort((a,b) => a.data_hora - b.data_hora);
      const labels = dadosOrdenados.map(item => `${item.nome} - ${item.data_hora.substring(0, 10)}`);
      const valores = dadosOrdenados.map(item => item.valor_atual/100);
      const valoresFormatados = valores.map(val => (val /  100).toLocaleString("en-US",{ style: "currency", currency: "USD" }));

      setChartData({
        labels,
        datasets: [
          {
            label: "Preço do Commodity",
            data: valores,
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
        "Açúcar NY nº11",
        "Cacau NY",
        "Café Contrato C",
        "Suco de Laranja NY",
        "Algodão nº2",
        "Madeira Serrada",
        "Açúcar Londres"
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

    {}
    <div className="grafico-container">
       {chartData.labels.length > 0 ? (
        <Line data={chartData} options={options} />
       ) : (
      <p>Carregando dados...</p>  )}
    </div>
  </div>
);

}

export default App;