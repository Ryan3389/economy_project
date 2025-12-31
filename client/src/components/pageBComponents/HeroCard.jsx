function HeroCard({ headline, explanation, watch_next }) {
  return (
    <div className="heroCard">
      <h2 className="heroTitle">{headline}</h2>
      <p className="heroText">{explanation}</p>

      <div className="heroNext">
        <span className="heroNextLabel">Watch next</span>
        <p className="heroNextText">{watch_next}</p>
      </div>
    </div>
  );
}

export default HeroCard;

// function HeroCard({headline, explanation, watch_next}){
//     console.log(watch_next)
//     return (
//         <>
//             <h2>{headline}</h2>
//             <p>{explanation}</p>
//             <p>{watch_next}</p>
//         </>
//     )
// }

// export default HeroCard