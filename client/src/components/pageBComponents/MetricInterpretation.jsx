function MetricInterpretation({ metric, trends }) {
  const dir = (metric?.trend_direction || "").toLowerCase();

  const badgeClass =
    dir.includes("rising") || dir.includes("up")
      ? "badge badge--up"
      : dir.includes("falling") || dir.includes("down")
      ? "badge badge--down"
      : "badge badge--flat";

  const fmtPct = (n) => {
    if (n === null || n === undefined || Number.isNaN(Number(n))) return "—";
    return `${Number(n).toFixed(2)}%`;
    };

  const fmtNum = (n) => {
    if (n === null || n === undefined || Number.isNaN(Number(n))) return "—";
    return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 });
  };

  return (
    <article className="interpretCard">
      <div className="interpretTop">
        <h2 className="interpretTitle">{metric.metric_name}</h2>
        <span className={badgeClass}>{metric.trend_direction}</span>
      </div>

      <div className="interpretStats">
        <div className="stat">
          <div className="statLabel">Latest</div>
          <div className="statValue">{fmtNum(trends.latest_value)}</div>
        </div>
        <div className="stat">
          <div className="statLabel">MoM</div>
          <div className="statValue">{fmtPct(trends.mom_pct_change)}</div>
        </div>
        <div className="stat">
          <div className="statLabel">YoY</div>
          <div className="statValue">{fmtPct(trends.yoy_pct_change)}</div>
        </div>
        <div className="stat">
          <div className="statLabel">As of</div>
          <div className="statValue">{trends.as_of_date || "—"}</div>
        </div>
      </div>

      <div className="interpretBody">
        <h3 className="interpretSubhead">What this means</h3>
        <p className="interpretText">{metric.trend_meaning.trend_meaning}</p>

        <h3 className="interpretSubhead">Summary</h3>
        <p className="interpretText">{metric.trend_meaning.trend_summary}</p>
      </div>
    </article>
  );
}

export default MetricInterpretation;

// function MetricInterpretation({metric, trends}){

//     console.log("Trends")
//     console.log(trends)
//     return(
//         <>
//         <h2>{metric.metric_name}</h2>
//         <p>{metric.trend_direction}</p>
//         <p>Latest Value: {trends.latest_value}</p>
//         <p>As of: {trends.as_of_date}</p>
//         <p>MoM: {trends.mom_pct_change}</p>
//         <p>YoY: {trends.yoy_pct_change}</p>
//         <p>{metric.trend_meaning.trend_meaning}</p>
//         <p>{metric.trend_meaning.trend_summary}</p>
//         </>
//     )
// }

// export default MetricInterpretation