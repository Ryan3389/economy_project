from backend.server.db.db import get_connection
from backend.server.schemas.planModels import PlanningInput

def get_trend_meaning(indicator):
    match indicator:
        # Cases for inflation 
        case { "metric": "Inflation(cpi)", "trend": "Rising"}:
            return{ 
                "trend_meaning":"Cost of living increasing",
                "trend_summary": "Expect everyday goods to become more expensive over time"
                }
        case {"metric": "Inflation(cpi)", "trend": "Falling"}:
            return {
                "trend_meaning": "Cost of living is easing",
                "trend_summary": "falling inflation means prices are rising more slowly, which helps your money go further and makes everyday goods more affordable over time"
            }
            # return "Cost of living is easing",
        case {"metric": "Inflation(cpi)", "trend": "Stable"}:
            return {
                "trend_meaning": "Cost of living is stable",
                "trend_summary": "Prices are holding steady, providing a predictable environment where your money’s value doesn't change suddenly. This balance makes it much easier to plan your budget and make big financial decisions with confidence."
                }
        
        # Cases for interest rates
        case { "metric": "Interest_Rates", "trend": "Rising"}:
            return {
                "trend_meaning": "Borrowing more expensive, savings yields improve",
                "trend_summary": "Borrowing more expensive for things like credit cards and mortgages, which usually slows down spending to help lower inflation. On the positive side, you will likely earn more interest on the money sitting in your savings account."
                }
        case {"metric": "Interest_Rates", "trend": "Falling"}:
            return {
                "trend_meaning": "Loans cheaper, savings returns lower",
                "trend_summary":"It becomes cheaper to take out loans or refinance a home, which encourages people to spend and businesses to grow. While this can boost the economy, it also means you will earn less interest on your personal savings."
                },
        case {"metric": "Interest_Rates", "trend": "Stable"}:
            return {
                "trend_meaning": "Borrowing is stable",
                "trend_summary": "Stable interest rates mean that borrowing costs and savings returns are staying the same, creating a predictable environment for your monthly budget. This consistency allows you to make long-term financial plans without worrying about your loan payments or investment income changing suddenly"
                }
        
        # Cases for unemployment rates
        case { "metric": "Unemployment_Rate", "trend": "Rising"}:
            return { 
                "trend_meaning": "Labor market weakening, income risk higher",
                "trend_summary": "When unemployment is increasing, it signals a weakening job market where it is harder for people to find work, leading to less consumer spending overall. This often results in employers offering fewer jobs and potentially cutting benefits or wages for existing workers."
                }
        case {"metric": "Unemployment_Rate", "trend": "Falling"}:
            return {
                "trend_meaning": "Job market strengthening",
                "trend_summary": "Decreasing unemployment means the job market is strengthening and businesses are hiring, making it easier to find a new job or negotiate a better salary. This typically leads to more people having steady paychecks, which boosts overall consumer spending and the economy."
                }
        case {"metric": "Unemployment_Rate", "trend": "Stable"}:
            return {
                "trend_meaning":"Job market is is stable",
                "trend_summary":"Stable unemployment means the number of available jobs is consistent and predictable, creating a balanced and reliable environment for those currently employed. While job seekers still need to compete for roles, the steady rate suggests no major economic shifts are likely in the immediate future."
                }

def overall_insight_summary(trend_direction):
    match trend_direction:
        #1. Inflation up, unemployment  upm interest rates up
        case ("Rising", "Rising", "Rising"):
            return {
                "headline": "Stagflation Warning: Prices, Interest Rates, and Unemployment Soaring Simultaneously, Signaling Economic Storm.",
                "explanation": "Prices are soaring, and borrowing is expensive, yet the job market is weakenign. It signals a period of severe hardship for households, as your paycheck buys less at the exact same time",
                "who_it_affects": "low-income households, recent homebuyers with variable debt, small business owners, and job seekers. They face the direct impact of simultaneously rising living costs, more expensive borrowing, and fewer available jobs.",
                "watch_next": "watch next"
            }
        #2. Inflation up,  unemploymenr down, interest rates up
        case ("Rising", "Falling", "Rising"):
            return {
                "headline": "Economic Rescue at a Price: Rates Slashed to Save Jobs as Living Costs Continue to Climb",
                "explanation":"the economy is shrinking so fast that the government is making it cheaper to borrow money to save jobs, despite the fact that everything is already getting more expensive. For you, it means your money is losing its value and your job security is lower, but it may be a good time to refinance debt if you are lucky enough to stay employed.",
                "who_it_affects": "this scenario punishes savers and workers who lose their purchasing power and job security, while rewarding debt-heavy individuals and asset owners who benefit from cheaper borrowing and rising property values.",
                "watch_next": "watch next"
                }
        # 3. Inflation down, uemployment down, inflation stable
        case ("Falling", "Falling", "Stable"):
            return {
                "headline": "The Soft Landing Arrives: Falling Prices and Lower Rates Signal a Strong Economic Finish to 2025.",
                "explanation":"the economy has returned to a healthy balance where your money goes further, your job is secure, and it is getting cheaper to borrow for big purchases. It is a period of economic healing where the stress of high living costs is finally fading.",
                "who_it_affects": "Who",
                "watch_next": "watch next"
                }
        # 4. Inflation down, unemployment up, interest rates falling
        case ("Falling", "Rising", "Falling"):
            return {
                "headline": "Economic Overdrive: Interest Rates Climb to Cool a Booming Job Market as Price Pressures Fade.",
                "explanation":"the economy is doing so well that the government is raising interest rates to keep things from getting out of control, even though prices are already starting to behave. For you, it means your job is very secure and your money buys more, but it is an expensive time to take on new debt or buy a house.",
                "who_it_affects": "who",
                "watch_next": "watch next"
                }
        # 5. Interest rates down, inflation stable, unemployment stable
        case ("Falling", "Stable", "Stable"):
            return {
                "headline": "Economic Stability Locked In: Prices Cool as the Job Market and Interest Rates Hold Steady.",
                "explanation":"Inflation is dropping toward the target without the need for further interest rate hikes, and the job market is holding steady rather than collapsing. It is a sign that the economy is cooling down just enough to be healthy without becoming cold.",
                "who_it_affects": "who",
                "watch_next": "watch next"
                }
        case ("Rising", "Stable", "Falling"):
            return {
                "headline": "Economy Runs Hot: Booming Job Market Ignites Price Hikes While Interest Rates Hold Steady",
                "explanation":"the job market is booming and it is easy to find work, but the cost of living is starting to climb again because the economy is moving too fast. It is a great time for job security, but you should prepare for interest rates to go up soon as the government tries to bring prices back under control.",
                "who_it_affects": "who",
                "watch_next": "watch next"
                }
        case _:
            return "Conflicting signals"
            
def econ_context():
    plan_sql_query = """
         SELECT 
            metric_name, 
            trend_direction, 
            latest_value, 
            mom_pct_change, 
            yoy_pct_change, 
            as_of_date
        FROM economic_signals
            WHERE metric_name IN ('Inflation(cpi)', 'Interest_Rates', 'Unemployment_Rate');
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                    cur.execute(plan_sql_query)
                    rows = cur.fetchall()

                    trends = {}
                    context = {}
                    insight_summary = {}

                    for row in rows:
                        #  data =  {"metric": row[0], "trend": row}
                         if(row[0] == "Inflation(cpi)"): 
                            metric_name = "Inflation" 
                            metric_unit = "Index"
                         elif(row[0] == "Interest_Rates"): 
                             metric_name = "Interest_Rate"
                             metric_unit = "Percent"
                         else: 
                             metric_name = "Unemployment_Rate"
                             metric_unit = "Percent"
                         metric_key = row[0]  
                         trend_direction = row[1]
                         latest_value = row[2] 
                         mom_pct_change = row[3]
                         yoy_pct_change = row[4]
                         as_of_date = row[5]

                         trend_meaning = {"metric": metric_key, "trend": trend_direction}
                         metric_meaning = get_trend_meaning(trend_meaning)
                         insight_summary[metric_key] = {
                             "trend_direction": trend_direction
                         }
                        #  inflation_trend = trends["Inflation(cpi)"]["trend_direction"]
                        #  interest_rates_trend = trends["Interest_Rates"]["trend_direction"]
                        #  unemployment_trend = trends["Unemployment_Rate"]["trend_direction"]

                        #  trends_combo = (inflation_trend, interest_rates_trend, unemployment_trend)

                        #  insights_trend_summary = overall_insight_summary(trends_combo)
                    
                         trends[metric_name] = {
                              "metric_name": metric_name,
                              "trend_direction": trend_direction,
                              "latest_value": latest_value,
                              "latest_value_unit": metric_unit,
                              "mom_pct_change": mom_pct_change,
                              "yoy_pct_change": yoy_pct_change,
                              "as_of_date": as_of_date
                         }  
                         context[metric_name] = {
                             "metric_name": metric_name,
                              "latest_value_unit": metric_unit,
                              "trend_direction": trend_direction,
                              "trend_meaning": metric_meaning
                         }  
                    inflation_trend = trends["Inflation"]["trend_direction"]
                    interest_rates_trend = trends["Interest_Rate"]["trend_direction"]
                    unemployment_trend = trends["Unemployment_Rate"]["trend_direction"]
                    trends_combo = (inflation_trend, interest_rates_trend, unemployment_trend)
                    insights_trend_summary = overall_insight_summary(trends_combo)
                    print(trends_combo)
                     
                    
                    
    finally:
        conn.close()
    
    insights = [{
        "trends": trends,
        "context": context,
        "overall_insights": insights_trend_summary
    }]


    return insights

   