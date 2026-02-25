from fpdf import FPDF
import json
from datetime import datetime

with open('../findings/risk_report.json') as f:
    data = json.load(f)

class AuditReport(FPDF):
    def header(self):
        self.set_fill_color(30, 58, 95)
        self.rect(0, 0, 210, 20, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 12)
        self.set_y(6)
        self.cell(0, 8, 'CONFIDENTIAL - IT AUDIT REPORT', align='C')
        self.set_text_color(0, 0, 0)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | IT Audit Simulation | Abdulmuizz Wahab', align='C')

pdf = AuditReport()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title
pdf.set_font('Helvetica', 'B', 22)
pdf.set_text_color(30, 58, 95)
pdf.ln(4)
pdf.cell(0, 12, 'IT Security Audit Report', align='C')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 6, 'Mock Corporate Environment | NIST Cybersecurity Framework Assessment', align='C')
pdf.ln(5)
pdf.cell(0, 6, f'Audit Date: {datetime.now().strftime("%B %d, %Y")} | Auditor: Abdulmuizz Wahab', align='C')
pdf.ln(10)

# Divider
pdf.set_draw_color(30, 58, 95)
pdf.set_line_width(0.8)
pdf.line(15, pdf.get_y(), 195, pdf.get_y())
pdf.ln(8)

# Executive Summary
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(30, 58, 95)
pdf.cell(0, 8, '1. Executive Summary')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
total = data['total_score']
count = len(data['findings'])
critical = sum(1 for f in data['findings'] if f['risk'] == 'Critical')
high = sum(1 for f in data['findings'] if f['risk'] == 'High')
medium = sum(1 for f in data['findings'] if f['risk'] == 'Medium')

summary = (f"An IT security audit was conducted against a simulated three-tier corporate environment "
           f"consisting of a web server (Nginx), database server (MySQL 8.0), and employee workstation "
           f"(SSH server). The assessment evaluated technology controls across all five NIST Cybersecurity "
           f"Framework functions: Identify, Protect, Detect, Respond, and Recover. "
           f"The audit identified {count} control deficiencies with a cumulative risk score of {total}/20, "
           f"indicating a HIGH overall risk posture. Immediate remediation is recommended for "
           f"{critical} Critical and {high} High severity findings prior to any production deployment.")
pdf.multi_cell(0, 6, summary)
pdf.ln(6)

# Risk Summary Box
pdf.set_fill_color(240, 244, 250)
pdf.set_draw_color(30, 58, 95)
pdf.set_line_width(0.3)
pdf.rect(15, pdf.get_y(), 180, 28, 'DF')
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(30, 58, 95)
pdf.set_y(pdf.get_y() + 4)
pdf.cell(0, 6, 'Risk Summary', align='C')
pdf.ln(7)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.cell(45, 6, f'Total Score: {total}/20', align='C')
pdf.cell(45, 6, f'Critical: {critical}', align='C')
pdf.cell(45, 6, f'High: {high}', align='C')
pdf.cell(45, 6, f'Medium: {medium}', align='C')
pdf.ln(14)

# Scope
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(30, 58, 95)
pdf.cell(0, 8, '2. Audit Scope and Objectives')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
scope_text = ("This audit assessed three containerized systems deployed via Docker Compose on a Kali Linux "
              "host, simulating a small corporate environment. The audit framework used was the NIST "
              "Cybersecurity Framework (CSF) v1.1. Systems in scope included: Nginx web server (port 8080), "
              "MySQL 8.0 database server (port 3306), and a Linux SSH workstation (port 2222). "
              "Out of scope: network perimeter controls, physical security, and third-party vendor assessments.")
pdf.multi_cell(0, 6, scope_text)
pdf.ln(6)

# Methodology
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(30, 58, 95)
pdf.cell(0, 8, '3. Methodology')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
steps = [
    ('Asset Discovery', 'Conducted port scanning using Nmap and a custom Python scanner to inventory all running services and exposed ports.'),
    ('Access Control Testing', 'Attempted authentication to SSH and MySQL services using known weak and default credentials to assess PR.AC-1 compliance.'),
    ('Encryption Assessment', 'Queried MySQL system variables to determine encryption at rest configuration across all database components.'),
    ('Log Review', 'Collected and analyzed container logs from all three systems to assess detection capability and logging adequacy.'),
    ('Risk Scoring', 'Applied weighted risk scoring (Critical=4, High=3, Medium=2, Low=1) using an automated Python script to prioritize findings.')
]
for title, desc in steps:
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(5, 6, '')
    pdf.cell(0, 6, f'- {title}')
    pdf.ln(6)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(10, 6, '')
    pdf.multi_cell(175, 6, desc)
    pdf.ln(2)

pdf.ln(4)

def get_recommendation(control):
    recs = {
        'PR.AC-1': 'Enforce strong password policy (min 16 chars). Disable remote root database access. Implement multi-factor authentication where possible.',
        'PR.DS-1': 'Enable MySQL encryption at rest using InnoDB tablespace encryption. Encrypt redo and undo logs. Implement a key management solution.',
        'DE.CM-1': 'Deploy a centralized logging solution (e.g., Graylog or Splunk). Enable Nginx access logs. Implement IDS/IPS monitoring on all network segments.',
        'RS.RP-1': 'Develop and document a formal Incident Response Plan covering detection, containment, eradication, and recovery procedures.',
        'RC.RP-1': 'Implement automated daily backups with offsite storage. Document and test a Disaster Recovery Plan with defined RTO and RPO targets.'
    }
    return recs.get(control, 'Review and remediate control deficiency in accordance with NIST CSF guidelines.')

# Findings
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(30, 58, 95)
pdf.cell(0, 8, '4. Findings and Recommendations')
pdf.ln(8)

risk_colors = {
    'Critical': (180, 0, 0),
    'High':     (200, 80, 0),
    'Medium':   (180, 130, 0),
    'Low':      (0, 120, 0)
}

risk_bg = {
    'Critical': (255, 235, 235),
    'High':     (255, 243, 230),
    'Medium':   (255, 250, 220),
    'Low':      (235, 255, 235)
}

for i, finding in enumerate(data['findings'], 1):
    risk = finding['risk']
    color = risk_colors.get(risk, (0, 0, 0))
    bg = risk_bg.get(risk, (245, 245, 245))

    # Finding header
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*color)
    pdf.set_line_width(0.5)
    pdf.rect(15, pdf.get_y(), 180, 10, 'DF')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*color)
    pdf.cell(5, 10, '')
    pdf.cell(130, 10, f'Finding {i}: {finding["description"]} ({finding["control"]})')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(45, 10, f'Risk: {risk}', align='R')
    pdf.ln(12)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)

    details = {
        'Condition':      finding['finding'],
        'Criteria':       f'NIST CSF control {finding["control"]} requires adequate implementation of this security domain.',
        'Risk':           f'Failure to remediate this control increases exposure to unauthorized access, data breach, or operational disruption. Risk Score: {finding["score"]}/4.',
        'Recommendation': get_recommendation(finding['control'])
    }

    for label, text in details.items():
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(10, 6, '')
        pdf.cell(40, 6, f'{label}:')
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(140, 6, text)
        pdf.ln(1)

    pdf.ln(5)

# Conclusion
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(30, 58, 95)
pdf.cell(0, 8, '5. Conclusion')
pdf.ln(8)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
conclusion = ("The assessed environment demonstrates significant control deficiencies across multiple NIST CSF "
              "domains. The combination of weak credentials, absent encryption at rest, lack of network monitoring, "
              "and missing incident response and recovery plans represents an unacceptable risk posture for any "
              "production financial services environment. It is recommended that remediation of Critical and High "
              "findings be completed within 30 days, with Medium findings addressed within 90 days. A follow-up "
              "audit should be conducted after remediation to validate control effectiveness.")
pdf.multi_cell(0, 6, conclusion)

pdf.output('../reports/IT_Audit_Report.pdf')
print('Audit report generated: reports/IT_Audit_Report.pdf')
