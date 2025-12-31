import { useState, useEffect } from "react";

function trendBadgeClass(direction = "") {
  const d = direction.toLowerCase();
  if (d.includes("rising") || d.includes("up")) return "badge badge--up";
  if (d.includes("falling") || d.includes("down")) return "badge badge--down";
  return "badge badge--flat";
}

function fmtNum(n) {
  if (n === null || n === undefined || Number.isNaN(Number(n))) return "—";
  const num = Number(n);
  return num.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function fmtPct(n) {
  if (n === null || n === undefined || Number.isNaN(Number(n))) return "—";
  const num = Number(n);
  return `${num.toFixed(2)}%`;
}

function MetricCard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await fetch("/api/economy/summary");
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const result = await response.json();
        setData(Array.isArray(result) ? result : []);
      } catch (error) {
        setError(error.message ?? String(error));
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, []);

  if (loading) return <div>Loading summary…</div>;
  if (error) return <div>Error loading summary: {error}</div>;

  return (
    <div className="metricGrid">
      {data.map((item) => (
        <article className="metricCard" key={item.metric_name}>
          <div className="metricTop">
            <h3 className="metricName">{item.metric_name}</h3>
            <span className={trendBadgeClass(item.trend_direction)}>
              {item.trend_direction ?? "—"}
            </span>
          </div>

          <p className="metricDate">As of {item.as_of_date ?? "—"}</p>

          <div className="metricValue">{fmtNum(item.latest_value)}</div>

          <div className="metricMeta">
            <span>MoM: {fmtPct(item.mom_pct_change)}</span>
            <span>YoY: {fmtPct(item.yoy_pct_change)}</span>
          </div>

          <p className="metricSummary">{item.summary}</p>
        </article>
      ))}
    </div>
  );
}

export default MetricCard;

// import { useState, useEffect } from "react"
// function MetricCard(){
//     const [data, setData] = useState([])
//     const [loading, setLoading] = useState(true)
//     const [error, setError] = useState(null)

//     useEffect(() => {
//         const fetchSummary = async() => {
//             try {
//                 const response = await fetch("/api/economy/summary")

//                 if(!response.ok){
//                     throw new Error(`HTTP error ${response.status}`)
//                 }

//                 const result = await response.json()
//                 console.log(result)
//                 setData(result)
//             } catch (error) {
//                 setError(error)
//             } finally{
//                 setLoading(false)
//             }
//         }
//         fetchSummary()
//     }, [])
//     return(
//         <section className="metric_summary_section">
//             <div>
//                 {data.map((item) => (
//                     <div>
//                         <h3>{item.metric_name}</h3>
//                         <p>{item.as_of_date}</p>
//                         <p>{item.latest_value}</p>
//                         <p>{item.mom_pct_change}</p>
//                         <p>{item.yoy_pct_change}</p>
//                         <p>{item.trend_direction}</p>
//                         <p>{item.summary}</p>
//                         <p></p>
//                     </div>

                    
//                 //   <li key={item.metric_name}>
//                 //     <strong>{item.metric_name}</strong>: {item.latest_value}
//                 //   </li>
//                 ))}
//             </div>

//     </section>
//   );
    
// }

// export default MetricCard

