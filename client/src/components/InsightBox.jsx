import { useEffect, useState } from "react";

function InsightBox() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const response = await fetch("/api/economy/insight");
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const result = await response.json();
        setData(result ?? {});
      } catch (error) {
        setError(error.message ?? String(error));
      } finally {
        setLoading(false);
      }
    };
    fetchInsights();
  }, []);

  if (loading) return <div>Loading insight…</div>;
  if (error) return <div>Error loading insight: {error}</div>;

  return (
    <section>
      <h3 className="insightHeadline">{data.headline}</h3>
      <p className="insightText">{data.explanation}</p>
      <p className="insightFoot">As of: {data.as_of_date}</p>
    </section>
  );
}

export default InsightBox;

// import { useEffect, useState } from "react"
// function InsightBox (){
//     const [data, setData] = useState([])
//     const [loading, setLoading] = useState(true)
//     const [error, setError] = useState(null)

//     useEffect(() => {
//         const fetchInsights = async() => {
//             try {
//                 const response = await fetch("/api/economy/insight")

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
//         fetchInsights()
//     }, [])

//     return (
//         <section>
//             <h3>{data.headline}</h3>
//             <p>{data.explanation}</p>
//             <p>As of: {data.as_of_date}</p>
//         </section>
//     )
// }

// export default InsightBox