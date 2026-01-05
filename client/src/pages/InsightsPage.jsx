import { useState, useEffect } from "react";
import HeroCard from "../components/pageBComponents/HeroCard";
import MetricInterpretation from "../components/pageBComponents/MetricInterpretation";


function InsightsPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/planning/context");
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);
        const results = await response.json();
        setData(results);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <p className="pageB-state">Loading...</p>;
  if (error) return <p className="pageB-state">{error.message}</p>;
  if (!data.length) return <p className="pageB-state">No data returned.</p>;

  const page = data[0];

  return (
    <div className="pageB">
      <header className="pageB-header">
        <div>
          <h1 className="pageB-title">Economic Context & Interpretation</h1>
          <p className="pageB-subtitle">
            Plain-English explanation of current economic signals
          </p>
        </div>

        <div className="pageB-meta">
          <span className="pageB-chip">As of: March 2025</span>
        </div>
      </header>

      <main className="pageB-grid">
        <section className="pageB-panel pageB-panel--hero">
          <HeroCard
            headline={page.overall_insights.headline}
            explanation={page.overall_insights.explanation}
            watch_next={page.overall_insights.watch_next}
          />
        </section>

        <section className="pageB-panel">
          <MetricInterpretation
            metric={page.context.Inflation}
            trends={page.trends.Inflation}
          />
        </section>

        <section className="pageB-panel">
          <MetricInterpretation
            metric={page.context.Interest_Rate}
            trends={page.trends.Interest_Rate}
          />
        </section>

        <section className="pageB-panel">
          <MetricInterpretation
            metric={page.context.Unemployment_Rate}
            trends={page.trends.Unemployment_Rate}
          />
        </section>
      </main>
    </div>
  );
}

export default InsightsPage


// import { useState, useEffect } from "react";
// import HeroCard from "../components/pageBComponents/HeroCard";
// import MetricInterpretation from "../components/pageBComponents/MetricInterpretation";

// function PageB() {
//   const [data, setData] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const response = await fetch("/api/planning/context");
//         if (!response.ok) throw new Error(`HTTP error ${response.status}`);
//         const results = await response.json();
//         setData(results);
//       } catch (err) {
//         setError(err);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchData();
//   }, []);

//   if (loading) return <p>Loading...</p>;
//   if (error) return <p>{error.message}</p>;
//   if (!data.length) return <p>No data returned.</p>;

//   const page = data[0];
//   const metricKeys = Object.keys(page.trends);
//   console.log("data")
//   console.log(data)

//   return (
//     <>
//       <div>
//         <h1>Economic Context & Interpretation</h1>
//         <p>Plain-English explanation of current economic signals</p>
//         <p>As of: March 2025</p>
//       </div>

//       <HeroCard
//         headline={page.overall_insights.headline}
//         explanation={page.overall_insights.explanation}
//         watch_next={page.overall_insights.watch_next}
//       />

//         <MetricInterpretation
//             metric={data[0].context.Inflation}
//             trends={data[0].trends.Inflation}
//         />
//         <MetricInterpretation
//         metric={data[0].context.Interest_Rate}
//         trends={data[0].trends.Interest_Rate}
//         />
//         <MetricInterpretation
//         metric={data[0].context.Unemployment_Rate}
//         trends={data[0].trends.Unemployment_Rate}
//         />
//     </>
//   );
// }

// export default PageB;


