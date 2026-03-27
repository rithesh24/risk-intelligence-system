from services.risk_engine import RiskEngine
from observability.agent_monitor import monitor

def main():
    engine = RiskEngine()
    
    print("\n=== Business Risk Intelligence System ===\n")
    
    company_description = input("Enter Company DEscription:\n> ")
    
    if not company_description.strip():
        print("No description provided. Exiting.")
        return
    
    result = engine.analyze_company(company_description)
    
    print("\n----- Risk Intelligence Output -----\n")
    
    risk_score = result["risk_score"]
    confidence = result["confidence"]
    
    print(f"Risk Score : {f'{risk_score:.2f}' if risk_score is not None else 'N/A'}")
    print(f"Confidence : {f'{confidence:.2f}' if confidence is not None else 'N/A'}\n")
    
    print("Explanation:")
    print(result["explanation"] or "No explanation generated.", "\n")
    
    print("Recommendations:")
    recommendations = result.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            print(f"  - {rec}")
    else:
        print("  No recommendations generated.")
    print("\n------------------------------------\n")
    
    print("\n----- Agent Logs -----\n")
    logs = monitor.get_logs()
    if logs:
        for log in logs:
            status = "❌ FAILED" if log["errored"] else "✅"
            print(f"{status} {log['agent']} — risk={log['risk_score']:.2f} confidence={log['confidence']:.2f}")
            print(f"   {log['reasoning']}\n")
    else:
        print("No agent logs found.")

    print("------------------------------------\n")
    
if __name__=="__main__":
    main()

