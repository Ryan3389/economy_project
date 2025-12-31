import { useState, useEffect } from "react";


function ForecastPage() {
  const [forecastInput, setForecastInput] = useState({
    horizon_months: "1",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForecastInput({ ...forecastInput, [name]: value });
  };

  const handleRunForecast = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("/api/forecast/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          horizon_months: Number(forecastInput.horizon_months),
        }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Forecast error: ", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("ForecastInput updated: ", forecastInput);
  }, [forecastInput]);

  const horizonLabel =
    forecastInput.horizon_months === "1"
      ? "1 Month"
      : forecastInput.horizon_months === "3"
      ? "3 Months"
      : "6 Months";

  const predicted =
    result?.model_prediction !== undefined && result?.model_prediction !== null
      ? Number(result.model_prediction)
      : null;

  const generatedAt = result?.generated_at || "Latest run";
  const modelName = result?.model_name || "Linear Regression";

  return (
    <div className="forecastPage">
      <header className="forecastHeader">
        <div>
          <h1 className="forecastTitle">Inflation Forecast</h1>
          <p className="forecastSubtitle">Forecast CPI using trained models</p>
        </div>
        <div className="forecastMeta">
          <span className="forecastChip">As of: latest available data</span>
        </div>
      </header>

      <main className="forecastGrid">
        {/* Input panel */}
        <section className="panel">
          <div className="panelHeader">
            <h2 className="panelTitle">Run a forecast</h2>
            <p className="panelHint">Choose a horizon and generate a new prediction</p>
          </div>

          <form className="forecastForm" onSubmit={handleRunForecast}>
            <label className="field">
              <span className="fieldLabel">Forecast horizon</span>
              <select
                className="select"
                name="horizon_months"
                id="horizon_months"
                value={forecastInput.horizon_months}
                onChange={handleChange}
              >
                <option value="1">1 Month</option>
                <option value="3">3 Months</option>
                <option value="6">6 Months</option>
              </select>
            </label>

            <button className="btnPrimary" type="submit" disabled={loading}>
              {loading ? "Running..." : "Run Forecast"}
            </button>
          </form>

          <div className="forecastTips">
            <p className="tipText">
              Short horizons are generally more stable. Longer horizons carry more uncertainty.
            </p>
            <ul className="tipList">
              <li>Uses the latest engineered macro features</li>
              <li>Returns a single-point CPI estimate for the selected horizon</li>
            </ul>
          </div>
        </section>

        {/* Result panel */}
        <section className="panel panel--result">
          <div className="panelHeader">
            <h2 className="panelTitle">Forecast result</h2>
            <p className="panelHint">Latest prediction output</p>
          </div>

          <div className="resultCard">
            <div className="resultTop">
              <span className="badge badge--flat">CPI Forecast</span>
              <span className="resultHorizon">{horizonLabel}</span>
            </div>

            <div className="resultValue">
              {predicted === null ? "—" : predicted.toLocaleString(undefined, { maximumFractionDigits: 2 })}
            </div>

            <div className="resultMeta">
              <div className="metaItem">
                <div className="metaLabel">Model</div>
                <div className="metaValue">{modelName}</div>
              </div>
              <div className="metaItem">
                <div className="metaLabel">Generated</div>
                <div className="metaValue">{generatedAt}</div>
              </div>
              <div className="metaItem">
                <div className="metaLabel">Horizon</div>
                <div className="metaValue">{result?.horizon_months ?? forecastInput.horizon_months} months</div>
              </div>
            </div>

            <p className="resultExplain">
              This estimate assumes current macroeconomic conditions persist over the selected horizon.
            </p>
          </div>
        </section>

        {/* Transparency panel */}
        <section className="panel panel--transparency">
          <div className="panelHeader">
            <h2 className="panelTitle">Model transparency</h2>
            <p className="panelHint">How this forecast is produced</p>
          </div>

          <div className="transparencyGrid">
            <div className="infoCard">
              <div className="infoLabel">Model type</div>
              <div className="infoValue">{modelName}</div>
            </div>

            <div className="infoCard">
              <div className="infoLabel">Training data</div>
              <div className="infoValue">Macroeconomic indicators</div>
            </div>

            <div className="infoCard">
              <div className="infoLabel">Retraining</div>
              <div className="infoValue">Automated via Prefect Flow</div>
            </div>

            <div className="infoCard">
              <div className="infoLabel">Storage</div>
              <div className="infoValue">Predictions stored in DB</div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default ForecastPage;
    
// import { useState, useEffect } from "react"
// function ForecastPage(){
//   const [forecastInput, setForecastInput] = useState({
//     horizon_months: "1"
//   })

//   const [result, setResult] = useState(null)
//   const [ loading, setLoading] = useState(false)

//   const handleChange = (e) => {
//     const { name, value } = e.target
//     setForecastInput({
//         ...forecastInput,
//         [name]: value
//     })
//   }

//   const handleRunForecast = async(e) => {
//     e.preventDefault()
//     setLoading(true)

//     try {
//         console.log("Sending horizon:", forecastInput.horizon_months)
//         const response = await fetch("/api/forecast/predict", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 horizon_months: Number(forecastInput.horizon_months)
//             })
//         })



//       const data = await response.json()
//       console.log("Forecast response: ", data)
//       setResult(data)
//     } catch (error) {
//       console.error("Forecast error: ", error)
//     } finally{
//         setLoading(false)
//     }
//   }

//   useEffect(() => {
//     console.log("ForecastInput updated: ", forecastInput)
//   }, [forecastInput])

//     return (
//         <section>
//             <div>
//                <h1>Inflation Forecast</h1>
//                <p>Forecast CPI using trained models</p>
//                <p>As of: latest available data</p>
//             </div>

//         <div>
//             <form onSubmit={handleRunForecast}>
//                 <label htmlFor="horizon">Forecast Horizon</label>
//                     <select
//                         name="horizon_months"          
//                         id="horizon_months"
//                         value={forecastInput.horizon_months}
//                         onChange={handleChange}>
//                         <option value="1">1 Month</option>
//                         <option value="3">3 Months</option>
//                         <option value="6">6 Months</option>
//                     </select>

//                     <button type="Submit" disabled={loading}>{loading ? "Running...": "Run Forecast"}</button>
//             </form>
//         </div>
            
//             <div>
//                 <h2>Forecast Result</h2>
//                 <p>CPI Forecast</p>
//                 <p>Predicted CPI Index: {result ? result.model_prediction : 0}</p>
//                 <p>Horizon: {result ? result.horizon_months : "Select horizon month"}</p>
//                 <p>Model: Linear Regression</p>
//                 <p>Generated At: 2025-12-28</p>
//             </div>

//             <div>
//                 <p>This forecast estimates where CPI is likely to be one month from now, assuming current macroeconomic conditions persists.</p>
//                 <ul>
//                     <li>Short term forecasts are more stable</li>
//                     <li>Longer horizons carry more uncertainty</li>
//                 </ul>
//             </div>

//             <div>
//                 <h3>Model Transparency</h3>
//                 <p>Model Type: Linear Regression</p>
//                 <p>Training Data: Macroeconomic indicators</p>
//                 <p>Last retrained: via Prefect Flow</p>
//                 <p>Predictions stored in DB</p>
//             </div>
//         </section>
        

//     )
// }

// export default ForecastPage     