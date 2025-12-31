import MetricCard from "../components/MetricCards";
import InsightBox from "../components/InsightBox";
import TrendChart from "../components/TrendChart";

function Dashboard() {
  return (
    <div className="page">
      <header className="pageHeader">
        <div>
          <h1 className="pageTitle">Economic Dashboard</h1>
          <p className="pageSubtitle">
            Live economic signals pulled from the FRED API and served via your API
          </p>
        </div>
      </header>

      <main className="grid">
        <section className="panel panel--cards">
          <div className="panelHeader">
            <h2 className="panelTitle">Latest Summary</h2>
            <p className="panelHint">Most recent values + MoM / YoY changes</p>
          </div>
          <MetricCard />
        </section>

        <section className="panel panel--chart">
          <div className="panelHeader">
            <h2 className="panelTitle">Trends</h2>
            <p className="panelHint">Compare raw series vs rolling averages</p>
          </div>
          <TrendChart />
        </section>

        <section className="panel panel--insight">
          <div className="panelHeader">
            <h2 className="panelTitle">So What?</h2>
            <p className="panelHint">Plain-language interpretation</p>
          </div>
          <InsightBox />
        </section>
      </main>
    </div>
  );
}

export default Dashboard;

// import MetricCard from "../components/MetricCards"
// import InsightBox from "../components/InsightBox"
// import TrendChart from "../components/TrendChart"
// function Dashboard(){
//     return(
//         <div style={{padding: "24px", maxWidth: "1100px", margin: "0 auto"}}>
//             <h1>Economic Dashboard</h1>
//             <p>Live economic signals pulled from the FRED API and served via your API</p>

//             <section style={{marginTop: "24px"}}>
//                 <h2>Latest Summary</h2>
//                 <MetricCard/>
//             </section>
//             <section style={{marginTop: "24px"}}>
//                 <h2>Trends</h2>
//                 <TrendChart/>
//             </section>
//             <section style={{marginTop: "24px"}}>
//                 {/* <h2>So What?</h2> */}
//                 <InsightBox/>
//             </section>
//         </div>
//     )
// }

// export default Dashboard