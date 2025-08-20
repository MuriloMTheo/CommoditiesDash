import React, { useEffect, useState} from "react";
import { Line } from "react-chartjs-2";
import api from "./services/api";

function App(){
  const[chartData, setChartData] = useState({
    labels:[],
    datasets: [],
  });

useEffect(() => {
  api.get("/")
    .then(res => {
      console.log("Resposta da API:", res.data);
      const dados = res.data;

      setChartData({
        labels: dados.map(item => item.data_hora),
        datasets: [
          {
            label: "Preço do Commodity",
            data: dados.map(item => item.valor_atual),
            borderColor: "rgba(75,192,192,1)",
            fill: false,
          },
        ],
      });
    })
    .catch(err => console.log("Erro ao buscar dados:", err));
}, []);

  return (
    <div style={{ width: "80%", margin: "50px auto"}}>
      <h2>DashBoard de Commodities</h2>
      {chartData.labels.length > 0 ? <Line data={chartData} /> : <p>Carregando dados...</p>}
    </div>
 );
}

export default App;