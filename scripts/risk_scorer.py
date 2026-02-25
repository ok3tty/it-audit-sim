import csv
import json 
import os

risk_weights = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}

findings = []
total_score = 0

if os.path.exists("../findings/audit_checklist.csv"):
    with open('../findings/audit_checklist.csv') as file:

        reader = csv.DictReader(file)
        for row in reader:
            if row['Result'] == 'FAIL':
                score = risk_weights.get(row['Risk Level'], 0)
                total_score += score

                findings.append({
                    'control': row['Control ID'],
                    'description': row['Control Description'],
                    'risk': row['Risk Level'],
                    'finding': row['Finding'],
                    'score': score
                })
    findings.sort(key=lambda x:['score'], reverse=True)


    print(f'Total Risk Score: {total_score}')
    print(f'Nummber of Findings: {len(findings)}')
    print('\nTop Findings:')
    
    for f in findings[:3]:
        print(f'   [{f["risk"]}] {f["control"]}: {f["finding"]}')


    with open('../findings/risk_report.json', 'w') as out:
        json.dump({'total_score': total_score, 'findings':findings}, out, indent=2)
