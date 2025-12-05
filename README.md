# Keystroke Logger — AUTHORIZED RESEARCH / DEFENSIVE TOOL (LOCAL-ONLY)

> ⚠️ IMPORTANT — READ BEFORE USING  
> This repository contains a keystroke-capture program intended **only** for:
> - Security research in an isolated lab environment,  
> - Developing detection or mitigation techniques (defensive tools), or  
> - Accessibility experiments where explicit, informed consent has been obtained from all participants.  
>
> **Do not use this on any machine or account you do not own or do not have explicit written permission to test.**
> Misuse may be illegal in your jurisdiction and violate privacy and institutional policies.

---

## Purpose

This project demonstrates how keyboard events are captured programmatically and how logs can be handled **locally** for analysis. It is intended for educational and defensive purposes only: to help developers and security teams understand, detect, and mitigate key-logging techniques — not to surreptitiously record users.

---

## Key Principles & Ethics

- **Consent:** Always obtain explicit, documented consent from any participant or owner of a system before running this software.  
- **Transparency:** Use clear notices and audit logging when running on shared systems.  
- **Minimal Scope:** Keep the instrumented environment isolated (e.g., virtual machine, test network).  
- **Data Minimization:** Store logs only as long as necessary and securely delete them when finished.  
- **Legal Compliance:** Check local laws and organisational policies before conducting any monitoring.

---

## Features (for lab / defensive use)

- Capture keyboard events in real time.
- Option to write keystroke logs to a local file for offline analysis.
- Timed batching of logs (configurable interval).
- Simple filename format that includes timestamps for easy audit.

> NOTE: Any code that would send logs to remote servers (email or network exfiltration) MUST be disabled in production and is intentionally omitted from this README. If you need remote reporting for legitimate enterprise monitoring, that must be implemented with approval, secure channels, encryption, and audit trails — and I can help design that securely if you confirm authorized use.

---

## Repository Structure

proj/
keylogger.py # Keylogger implementation (local file reporting only)
config.example.yaml # Example config values
requirements.txt # Dependencies
README.md # This file


---

## Dependencies

The project uses small Python libraries to listen to keyboard events and manage timers. Install in a controlled environment (virtualenv/venv):


python -m venv venv
source venv/bin/activate   # linux/mac
venv\Scripts\activate      # windows

pip install -r requirements.txt
Example requirements.txt

keyboard
Only install the packages you need and only in isolated/test environments.

Safe Configuration
Use local-only logging (report_method="file") — do not enable remote or email sending.

Set a conservative reporting interval in seconds (e.g., 60 or higher) for tests.

Store logs on encrypted filesystems when feasible.

Ensure log files are only readable by the test user (restrict file permissions).

Example config.example.yaml:

send_report_every: 60
report_method: file
log_directory: ./logs
Running (Controlled Lab)
Ensure you have explicit authorization and are running in an isolated VM or test system.

Activate your virtual environment.

Run the script with local-file reporting:


python keylogger.py
To stop, use CTRL+C. After testing, securely delete any generated logs.

Secure Handling & Cleanup
After tests, securely delete logs (e.g., overwrite then delete) if they contain sensitive input.

Revoke any elevated permissions granted during testing.

Keep an audit record of who ran the test, when, and why.

Defensive / Detection Notes (How defenders can use this)
Use the project to generate benign samples to test endpoint detection rules (EDR) and SIEM alerts.

Monitor for suspicious processes that hook keyboard APIs or spawn timers with repetitive network activity.

Check for unexpected file writes in user directories and unusual child processes of common applications.

Implement application allowlisting for known good binaries and restrict installation rights for non-admin users.

Legal & Institutional Compliance
Before any deployment even in a research context:

Obtain written authorization from system owners.

Inform relevant stakeholders (privacy officer, legal counsel).

Maintain records of consent and test scopes.

