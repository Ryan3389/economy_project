import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

const METRICS = [
  { slug: "cpi", label: "CPI (Inflation)" },
  { slug: "unemployment", label: "Unemployment Rate" },
  { slug: "interest_rates", label: "Interest Rates" },
];

export default function TrendChart() {
  const [slug, setSlug] = useState("cpi");
  const [limit, setLimit] = useState(60);
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const metricLabel = useMemo(() => {
    return METRICS.find((m) => m.slug === slug)?.label ?? slug;
  }, [slug]);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchTrends() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(`/api/economy/trends/${slug}?limit=${limit}`, {
          signal: controller.signal,
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const json = await res.json();
        // expected: { metric: "cpi", data: [...] }
        setSeries(Array.isArray(json.data) ? json.data : []);
      } catch (e) {
        // ignore abort errors
        if (e.name !== "AbortError") setError(e.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTrends();
    return () => controller.abort();
  }, [slug, limit]);

  if (loading) return <div>Loading trend…</div>;
  if (error) return <div>Error loading trend: {error}</div>;

  return (
    <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>
      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <label>
          Metric:&nbsp;
          <select value={slug} onChange={(e) => setSlug(e.target.value)}>
            {METRICS.map((m) => (
              <option key={m.slug} value={m.slug}>
                {m.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Points:&nbsp;
          <input
            type="number"
            min={10}
            max={240}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            style={{ width: 90 }}
          />
        </label>
      </div>

      <div style={{ height: 320, marginTop: 16 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={series}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" name={metricLabel} dot={false} />
            <Line type="monotone" dataKey="rolling_3m_avg" name="Rolling 3M Avg" dot={false} />
            <Line type="monotone" dataKey="rolling_12m_avg" name="Rolling 12M Avg" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}


// import { useEffect, useMemo, useState } from "react";
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   Tooltip,
//   CartesianGrid,
//   ResponsiveContainer,
//   Legend,
// } from "recharts";

// const METRICS = [
//   { slug: "cpi", label: "CPI (Inflation)" },
//   { slug: "unemployment", label: "Unemployment Rate" },
//   { slug: "interest_rates", label: "Interest Rates" },
// ];

// function TrendChart(){
//     const [data, setData] = useState([])
//     useEffect(() => {
//         const fetchTrends = async() => {
//             try {
//                 const response = await fetch(`/api/economy/trends/cpi?limit=60`)

//                 if(!response.ok){
//                     throw new Error(`HTTP error ${response.status}`)
//                 }

//                 const result = await response.json()
//                 console.log(result)
//                 setData(result)
//             } catch (error) {
//                 setError(error)
//             }
//         }
//         fetchTrends()
//     }, [])
//     return(
//         <h1>Hello from the chart page</h1>
//     )
// }

// export default TrendChart