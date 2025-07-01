from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import sqlite3
import json
from datetime import datetime
from database import init_database, save_control, get_controls as db_get_controls, save_poam, update_poam, delete_poam, get_poams as db_get_poams

app = Flask(__name__)
upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database on startup
init_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('uploaded_file', filename=file.filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/controls')
def get_controls():
    # Check if controls exist in database, if not, populate with defaults
    db_controls = db_get_controls()
    if not db_controls:
        # Load all controls from cmmc_data.py
        from cmmc_data import CMMC_LEVEL2_CONTROLS
        
        # Use all controls for complete implementation
        controls = CMMC_LEVEL2_CONTROLS
        
        # If cmmc_data doesn't have enough controls, fallback to basic set
        if len(controls) < 10:
            controls = [
        # Access Control (AC)
        {
            'id': 'AC.L2-3.1.1',
            'name': 'Limit information system access to authorized users',
            'description': 'Limit information system access to authorized users, processes acting on behalf of authorized users, or devices (including other information systems).',
            'domain': 'AC',
            'status': 'implemented'
        },
        {
            'id': 'AC.L2-3.1.2',
            'name': 'Limit information system access to types of transactions',
            'description': 'Limit information system access to the types of transactions and functions that authorized users are permitted to execute.',
            'domain': 'AC',
            'status': 'partial'
        },
        {
            'id': 'AC.L2-3.1.3',
            'name': 'Control information posted on publicly accessible systems',
            'description': 'Control information posted or processed on publicly accessible information systems.',
            'domain': 'AC',
            'status': 'not-implemented'
        },
        {
            'id': 'AC.L2-3.1.20',
            'name': 'Limit use of portable storage devices',
            'description': 'Limit use of portable storage devices on external information systems.',
            'domain': 'AC',
            'status': 'partial'
        },
        {
            'id': 'AC.L2-3.1.22',
            'name': 'Control information posting on publicly accessible systems',
            'description': 'Control information posted or processed on publicly accessible information systems.',
            'domain': 'AC',
            'status': 'not-implemented'
        },
        # Awareness and Training (AT)
        {
            'id': 'AT.L2-3.2.1',
            'name': 'Ensure managers and users are aware of security risks',
            'description': 'Ensure that managers, system administrators, and users of organizational information systems are made aware of the security risks associated with their activities.',
            'domain': 'AT',
            'status': 'implemented'
        },
        {
            'id': 'AT.L2-3.2.2',
            'name': 'Ensure personnel are trained for assigned roles',
            'description': 'Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.',
            'domain': 'AT',
            'status': 'partial'
        },
        # Audit and Accountability (AU)
        {
            'id': 'AU.L2-3.3.1',
            'name': 'Create and retain audit records',
            'description': 'Create and retain information system audit logs and audit records to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized information system activity.',
            'domain': 'AU',
            'status': 'not-implemented'
        },
        {
            'id': 'AU.L2-3.3.2',
            'name': 'Ensure audit records can be sorted and searched',
            'description': 'Ensure that the actions of individual information system users can be uniquely traced to those users so they can be held accountable for their actions.',
            'domain': 'AU',
            'status': 'not-implemented'
        },
        {
            'id': 'AU.L2-3.3.3',
            'name': 'Review and update logged events',
            'description': 'Review and update logged events.',
            'domain': 'AU',
            'status': 'partial'
        },
        {
            'id': 'AU.L2-3.3.4',
            'name': 'Alert in event of audit logging process failure',
            'description': 'Alert in the event of an audit logging process failure.',
            'domain': 'AU',
            'status': 'not-implemented'
        },
        {
            'id': 'AU.L2-3.3.5',
            'name': 'Correlate audit record review and analysis',
            'description': 'Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.',
            'domain': 'AU',
            'status': 'not-implemented'
        },
        {
            'id': 'AU.L2-3.3.6',
            'name': 'Provide audit record reduction and report generation',
            'description': 'Provide audit record reduction and report generation to support on-demand analysis and reporting.',
            'domain': 'AU',
            'status': 'partial'
        },
        {
            'id': 'AU.L2-3.3.7',
            'name': 'Provide system activity for anomalous behavior',
            'description': 'Provide an information system capability that compares and synchronizes audit records across a network of information systems.',
            'domain': 'AU',
            'status': 'not-implemented'
        },
        {
            'id': 'AU.L2-3.3.8',
            'name': 'Protect audit information and audit logging tools',
            'description': 'Protect audit information and audit logging tools from unauthorized access, modification, and deletion.',
            'domain': 'AU',
            'status': 'partial'
        },
        {
            'id': 'AU.L2-3.3.9',
            'name': 'Limit management of audit logging to privileged users',
            'description': 'Limit management of audit logging functionality to a subset of privileged users.',
            'domain': 'AU',
            'status': 'implemented'
        },
        # Configuration Management (CM)
        {
            'id': 'CM.L2-3.4.1',
            'name': 'Establish and maintain baseline configurations',
            'description': 'Establish and maintain baseline configurations and inventories of organizational information systems.',
            'domain': 'CM',
            'status': 'partial'
        },
        {
            'id': 'CM.L2-3.4.2',
            'name': 'Establish and enforce security configuration settings',
            'description': 'Establish and enforce security configuration settings for information technology products employed within organizational information systems.',
            'domain': 'CM',
            'status': 'implemented'
        },
        {
            'id': 'CM.L2-3.4.3',
            'name': 'Track and control changes to information systems',
            'description': 'Track, review, approve or disapprove, and log changes to organizational information systems.',
            'domain': 'CM',
            'status': 'partial'
        },
        {
            'id': 'CM.L2-3.4.4',
            'name': 'Analyze security impact of changes',
            'description': 'Analyze the security impact of changes prior to implementation.',
            'domain': 'CM',
            'status': 'not-implemented'
        },
        {
            'id': 'CM.L2-3.4.5',
            'name': 'Define and enforce access restrictions',
            'description': 'Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational information systems.',
            'domain': 'CM',
            'status': 'partial'
        },
        {
            'id': 'CM.L2-3.4.6',
            'name': 'Employ least functionality principle',
            'description': 'Employ the principle of least functionality by configuring organizational information systems to provide only essential capabilities.',
            'domain': 'CM',
            'status': 'implemented'
        },
        {
            'id': 'CM.L2-3.4.7',
            'name': 'Restrict and monitor user-installed software',
            'description': 'Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.',
            'domain': 'CM',
            'status': 'partial'
        },
        {
            'id': 'CM.L2-3.4.8',
            'name': 'Apply deny-by-exception policy to software programs',
            'description': 'Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software.',
            'domain': 'CM',
            'status': 'not-implemented'
        },
        {
            'id': 'CM.L2-3.4.9',
            'name': 'Control and monitor user-installed software',
            'description': 'Control and monitor user-installed software.',
            'domain': 'CM',
            'status': 'partial'
        },
        # Identification and Authentication (IA)
        {
            'id': 'IA.L2-3.5.1',
            'name': 'Identify information system users',
            'description': 'Identify information system users, processes acting on behalf of users, or devices.',
            'domain': 'IA',
            'status': 'implemented'
        },
        {
            'id': 'IA.L2-3.5.2',
            'name': 'Authenticate users, processes, or devices',
            'description': 'Authenticate (or verify) the identities of those users, processes, or devices, as a prerequisite to allowing access to organizational information systems.',
            'domain': 'IA',
            'status': 'partial'
        },
        {
            'id': 'IA.L2-3.5.3',
            'name': 'Use multifactor authentication',
            'description': 'Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.',
            'domain': 'IA',
            'status': 'not-implemented'
        },
        {
            'id': 'IA.L2-3.5.4',
            'name': 'Employ replay-resistant authentication mechanisms',
            'description': 'Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.',
            'domain': 'IA',
            'status': 'not-implemented'
        },
        {
            'id': 'IA.L2-3.5.5',
            'name': 'Prevent reuse of identifiers',
            'description': 'Prevent reuse of identifiers for a defined period.',
            'domain': 'IA',
            'status': 'partial'
        },
        {
            'id': 'IA.L2-3.5.6',
            'name': 'Disable identifiers after defined period of inactivity',
            'description': 'Disable identifiers after a defined period of inactivity.',
            'domain': 'IA',
            'status': 'implemented'
        },
        {
            'id': 'IA.L2-3.5.7',
            'name': 'Enforce minimum password complexity',
            'description': 'Enforce a minimum password complexity and change of characters when new passwords are created.',
            'domain': 'IA',
            'status': 'implemented'
        },
        {
            'id': 'IA.L2-3.5.8',
            'name': 'Prohibit password reuse',
            'description': 'Prohibit password reuse for a specified number of generations.',
            'domain': 'IA',
            'status': 'partial'
        },
        {
            'id': 'IA.L2-3.5.9',
            'name': 'Allow temporary password use for system logons',
            'description': 'Allow temporary password use for system logons with an immediate change to a permanent password.',
            'domain': 'IA',
            'status': 'implemented'
        },
        {
            'id': 'IA.L2-3.5.10',
            'name': 'Store and transmit only cryptographically-protected passwords',
            'description': 'Store and transmit only cryptographically-protected passwords.',
            'domain': 'IA',
            'status': 'implemented'
        },
        {
            'id': 'IA.L2-3.5.11',
            'name': 'Obscure feedback of authentication information',
            'description': 'Obscure feedback of authentication information.',
            'domain': 'IA',
            'status': 'implemented'
        },
        # Incident Response (IR)
        {
            'id': 'IR.L2-3.6.1',
            'name': 'Establish operational incident response capability',
            'description': 'Establish an operational incident response capability for organizational information systems.',
            'domain': 'IR',
            'status': 'partial'
        },
        {
            'id': 'IR.L2-3.6.2',
            'name': 'Detect and report incidents',
            'description': 'Detect, report, and respond to incidents.',
            'domain': 'IR',
            'status': 'not-implemented'
        },
        {
            'id': 'IR.L2-3.6.3',
            'name': 'Test incident response capability',
            'description': 'Test the organizational incident response capability.',
            'domain': 'IR',
            'status': 'not-implemented'
        },
        # Maintenance (MA)
        {
            'id': 'MA.L2-3.7.1',
            'name': 'Perform system maintenance',
            'description': 'Perform maintenance on organizational information systems.',
            'domain': 'MA',
            'status': 'implemented'
        },
        {
            'id': 'MA.L2-3.7.2',
            'name': 'Control nonlocal maintenance',
            'description': 'Provide controls on the tools, techniques, mechanisms, and personnel used to conduct information system maintenance.',
            'domain': 'MA',
            'status': 'partial'
        },
        {
            'id': 'MA.L2-3.7.3',
            'name': 'Require multifactor authentication for nonlocal maintenance',
            'description': 'Require multifactor authentication to establish nonlocal maintenance sessions via external network connections.',
            'domain': 'MA',
            'status': 'not-implemented'
        },
        {
            'id': 'MA.L2-3.7.4',
            'name': 'Supervise maintenance personnel',
            'description': 'Supervise the maintenance activities of maintenance personnel without required access authorization.',
            'domain': 'MA',
            'status': 'implemented'
        },
        {
            'id': 'MA.L2-3.7.5',
            'name': 'Sanitize equipment removed for off-site maintenance',
            'description': 'Sanitize equipment removed from organizational facilities for off-site maintenance or repairs.',
            'domain': 'MA',
            'status': 'partial'
        },
        {
            'id': 'MA.L2-3.7.6',
            'name': 'Check media containing diagnostic and test programs',
            'description': 'Check media containing diagnostic and test programs for malicious code before the media are used in organizational information systems.',
            'domain': 'MA',
            'status': 'not-implemented'
        },
        # Media Protection (MP)
        {
            'id': 'MP.L2-3.8.1',
            'name': 'Protect system media',
            'description': 'Protect (i.e., physically control and securely store) information system media containing CUI.',
            'domain': 'MP',
            'status': 'implemented'
        },
        {
            'id': 'MP.L2-3.8.2',
            'name': 'Limit access to CUI on system media',
            'description': 'Limit access to CUI on information system media to authorized users.',
            'domain': 'MP',
            'status': 'partial'
        },
        {
            'id': 'MP.L2-3.8.3',
            'name': 'Sanitize or destroy media',
            'description': 'Sanitize or destroy information system media containing CUI before disposal or release for reuse.',
            'domain': 'MP',
            'status': 'implemented'
        },
        {
            'id': 'MP.L2-3.8.4',
            'name': 'Mark media with necessary CUI markings',
            'description': 'Mark media with necessary CUI markings and distribution limitations.',
            'domain': 'MP',
            'status': 'partial'
        },
        {
            'id': 'MP.L2-3.8.5',
            'name': 'Control access to media during transport',
            'description': 'Control access to media during transport outside of controlled areas.',
            'domain': 'MP',
            'status': 'not-implemented'
        },
        {
            'id': 'MP.L2-3.8.6',
            'name': 'Implement cryptographic mechanisms',
            'description': 'Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport.',
            'domain': 'MP',
            'status': 'partial'
        },
        {
            'id': 'MP.L2-3.8.7',
            'name': 'Control use of removable media',
            'description': 'Control the use of removable media on information system components.',
            'domain': 'MP',
            'status': 'implemented'
        },
        {
            'id': 'MP.L2-3.8.8',
            'name': 'Prohibit use of portable storage devices',
            'description': 'Prohibit the use of portable storage devices when such devices have no identifiable owner.',
            'domain': 'MP',
            'status': 'implemented'
        },
        {
            'id': 'MP.L2-3.8.9',
            'name': 'Protect backup CUI at storage locations',
            'description': 'Protect the confidentiality of backup CUI at storage locations.',
            'domain': 'MP',
            'status': 'partial'
        },
        # Physical Protection (PE)
        {
            'id': 'PE.L2-3.10.1',
            'name': 'Limit physical access to organizational information systems',
            'description': 'Limit physical access to organizational information systems, equipment, and the respective operating environments.',
            'domain': 'PE',
            'status': 'implemented'
        },
        {
            'id': 'PE.L2-3.10.2',
            'name': 'Protect and monitor physical access',
            'description': 'Protect and monitor the physical facility and support infrastructure for organizational information systems.',
            'domain': 'PE',
            'status': 'implemented'
        },
        {
            'id': 'PE.L2-3.10.3',
            'name': 'Escort visitors and monitor visitor activity',
            'description': 'Escort visitors and monitor visitor activity; maintain audit logs of physical access; and control and manage physical access devices.',
            'domain': 'PE',
            'status': 'partial'
        },
        {
            'id': 'PE.L2-3.10.4',
            'name': 'Control physical access to output from output devices',
            'description': 'Control physical access to output from output devices.',
            'domain': 'PE',
            'status': 'implemented'
        },
        {
            'id': 'PE.L2-3.10.5',
            'name': 'Control physical access to information system media',
            'description': 'Control physical access to information system media.',
            'domain': 'PE',
            'status': 'implemented'
        },
        {
            'id': 'PE.L2-3.10.6',
            'name': 'Enforce safeguarding measures for CUI at alternate work sites',
            'description': 'Enforce safeguarding measures for CUI at alternate work sites.',
            'domain': 'PE',
            'status': 'partial'
        },
        # Personnel Security (PS)
        {
            'id': 'PS.L2-3.11.1',
            'name': 'Screen individuals prior to authorizing access',
            'description': 'Screen individuals prior to authorizing access to organizational information systems containing CUI.',
            'domain': 'PS',
            'status': 'implemented'
        },
        {
            'id': 'PS.L2-3.11.2',
            'name': 'Ensure CUI and information system processing are protected',
            'description': 'Ensure that organizational information and information systems are protected during and after personnel actions.',
            'domain': 'PS',
            'status': 'partial'
        },
        # Risk Assessment (RA)
        {
            'id': 'RA.L2-3.12.1',
            'name': 'Periodically assess risk to organizational operations',
            'description': 'Periodically assess the risk to organizational operations and assets, and individuals, resulting from the operation of organizational information systems.',
            'domain': 'RA',
            'status': 'partial'
        },
        {
            'id': 'RA.L2-3.12.2',
            'name': 'Scan for vulnerabilities in organizational information systems',
            'description': 'Scan for vulnerabilities in organizational information systems and hosted applications monthly or more frequently.',
            'domain': 'RA',
            'status': 'not-implemented'
        },
        {
            'id': 'RA.L2-3.12.3',
            'name': 'Remediate vulnerabilities in accordance with risk assessments',
            'description': 'Remediate vulnerabilities in accordance with risk assessments.',
            'domain': 'RA',
            'status': 'partial'
        },
        # System and Services Acquisition (SA)
        {
            'id': 'SA.L2-3.13.1',
            'name': 'Allocate resources to protect CUI',
            'description': 'Allocate sufficient resources to protect CUI.',
            'domain': 'SA',
            'status': 'implemented'
        },
        {
            'id': 'SA.L2-3.13.2',
            'name': 'Employ system development life cycle process',
            'description': 'Employ a system development life cycle process that incorporates information security considerations.',
            'domain': 'SA',
            'status': 'partial'
        },
        {
            'id': 'SA.L2-3.13.3',
            'name': 'Acquire and use information technology products',
            'description': 'Acquire and use information technology products with security-relevant configuration settings.',
            'domain': 'SA',
            'status': 'implemented'
        },
        {
            'id': 'SA.L2-3.13.4',
            'name': 'Require developer to implement security configuration settings',
            'description': 'Require the developer of the information system, system component, or information system service to provide configuration settings documentation.',
            'domain': 'SA',
            'status': 'partial'
        },
        # System and Communications Protection (SC)
        {
            'id': 'SC.L2-3.13.1',
            'name': 'Monitor and control communications at system boundaries',
            'description': 'Monitor, control, and protect organizational communications (i.e., information transmitted or received by organizational information systems) at the external boundaries and key internal boundaries of the information systems.',
            'domain': 'SC',
            'status': 'not-implemented'
        },
        {
            'id': 'SC.L2-3.13.2',
            'name': 'Employ architectural designs and implementation techniques',
            'description': 'Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security.',
            'domain': 'SC',
            'status': 'partial'
        },
        {
            'id': 'SC.L2-3.13.3',
            'name': 'Separate user functionality from system management functionality',
            'description': 'Separate user functionality from information system management functionality.',
            'domain': 'SC',
            'status': 'implemented'
        },
        {
            'id': 'SC.L2-3.13.4',
            'name': 'Prevent unauthorized connections',
            'description': 'Prevent unauthorized and unintended information transfer via shared system resources.',
            'domain': 'SC',
            'status': 'partial'
        },
        {
            'id': 'SC.L2-3.13.5',
            'name': 'Implement subnetworks for publicly accessible components',
            'description': 'Implement subnetworks for publicly accessible system components that are physically or logically separated from internal organizational networks.',
            'domain': 'SC',
            'status': 'not-implemented'
        },
        {
            'id': 'SC.L2-3.13.6',
            'name': 'Deny communications traffic by default',
            'description': 'Deny network communications traffic by default and allow network communications traffic by exception.',
            'domain': 'SC',
            'status': 'partial'
        },
        {
            'id': 'SC.L2-3.13.7',
            'name': 'Prevent remote devices from simultaneously connecting',
            'description': 'Prevent remote devices from simultaneously establishing non-remote connections with organizational information systems.',
            'domain': 'SC',
            'status': 'not-implemented'
        },
        {
            'id': 'SC.L2-3.13.8',
            'name': 'Implement cryptographic mechanisms',
            'description': 'Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission.',
            'domain': 'SC',
            'status': 'implemented'
        },
        {
            'id': 'SC.L2-3.13.9',
            'name': 'Terminate network connections at end of sessions',
            'description': 'Terminate network connections associated with communications sessions at the end of the sessions.',
            'domain': 'SC',
            'status': 'implemented'
        },
        {
            'id': 'SC.L2-3.13.10',
            'name': 'Establish and manage cryptographic keys',
            'description': 'Establish and manage cryptographic keys for cryptographic mechanisms employed in organizational information systems.',
            'domain': 'SC',
            'status': 'partial'
        },
        {
            'id': 'SC.L2-3.13.11',
            'name': 'Employ FIPS-validated cryptography',
            'description': 'Employ FIPS-validated cryptographic mechanisms when used to protect the confidentiality of CUI.',
            'domain': 'SC',
            'status': 'not-implemented'
        },
        {
            'id': 'SC.L2-3.13.12',
            'name': 'Prohibit remote activation of collaborative computing devices',
            'description': 'Prohibit remote activation of collaborative computing devices excluding those devices necessary for physical access control.',
            'domain': 'SC',
            'status': 'implemented'
        },
        {
            'id': 'SC.L2-3.13.13',
            'name': 'Control and monitor use of mobile code',
            'description': 'Control and monitor the use of mobile code.',
            'domain': 'SC',
            'status': 'partial'
        },
        {
            'id': 'SC.L2-3.13.14',
            'name': 'Control and monitor use of Voice over Internet Protocol technologies',
            'description': 'Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.',
            'domain': 'SC',
            'status': 'not-implemented'
        },
        {
            'id': 'SC.L2-3.13.15',
            'name': 'Protect authenticity of communications sessions',
            'description': 'Protect the authenticity of communications sessions.',
            'domain': 'SC',
            'status': 'partial'
        },
        {
            'id': 'SC.L2-3.13.16',
            'name': 'Protect confidentiality of CUI at rest',
            'description': 'Protect the confidentiality of CUI at rest.',
            'domain': 'SC',
            'status': 'implemented'
        },
        # System and Information Integrity (SI)
        {
            'id': 'SI.L2-3.14.1',
            'name': 'Identify and correct information system flaws',
            'description': 'Identify, report, and correct information and information system flaws in a timely manner.',
            'domain': 'SI',
            'status': 'partial'
        },
        {
            'id': 'SI.L2-3.14.2',
            'name': 'Provide protection from malicious code',
            'description': 'Provide protection from malicious code at appropriate locations within organizational information systems.',
            'domain': 'SI',
            'status': 'implemented'
        },
        {
            'id': 'SI.L2-3.14.3',
            'name': 'Monitor information system security alerts',
            'description': 'Monitor information system security alerts and advisories and take appropriate actions in response.',
            'domain': 'SI',
            'status': 'partial'
        },
        {
            'id': 'SI.L2-3.14.4',
            'name': 'Update malicious code protection mechanisms',
            'description': 'Update malicious code protection mechanisms when new releases are available.',
            'domain': 'SI',
            'status': 'implemented'
        },
        {
            'id': 'SI.L2-3.14.5',
            'name': 'Perform periodic scans of the information system',
            'description': 'Perform periodic scans of the information system and real-time scans of files from external sources.',
            'domain': 'SI',
            'status': 'partial'
        },
        {
            'id': 'SI.L2-3.14.6',
            'name': 'Monitor organizational information systems',
            'description': 'Monitor organizational information systems, including inbound and outbound communications traffic.',
            'domain': 'SI',
            'status': 'not-implemented'
        },
        {
            'id': 'SI.L2-3.14.7',
            'name': 'Identify unauthorized use of organizational information systems',
            'description': 'Identify unauthorized use of organizational information systems.',
            'domain': 'SI',
            'status': 'partial'
        }
        ]
        
        # Add realistic objectives for each control
        objectives_map = {
            'AC.L2-3.1.1': [
                {'objective': 'Implement user access controls', 'notes': ''},
                {'objective': 'Configure role-based access', 'notes': ''},
                {'objective': 'Review access permissions quarterly', 'notes': ''}
            ],
            'AC.L2-3.1.2': [
                {'objective': 'Define authorized transaction types', 'notes': ''},
                {'objective': 'Implement transaction monitoring', 'notes': ''},
                {'objective': 'Document function restrictions', 'notes': ''}
            ],
            'AU.L2-3.3.1': [
                {'objective': 'Configure audit logging systems', 'notes': ''},
                {'objective': 'Establish log retention policies', 'notes': ''},
                {'objective': 'Implement log monitoring and analysis', 'notes': ''}
            ],
            'IA.L2-3.5.1': [
                {'objective': 'Establish user identification procedures', 'notes': ''},
                {'objective': 'Implement unique user identifiers', 'notes': ''},
                {'objective': 'Maintain user identity records', 'notes': ''}
            ],
            'IA.L2-3.5.2': [
                {'objective': 'Deploy multi-factor authentication', 'notes': ''},
                {'objective': 'Configure authentication policies', 'notes': ''},
                {'objective': 'Test authentication mechanisms', 'notes': ''}
            ],
            'SC.L2-3.13.1': [
                {'objective': 'Monitor external communications', 'notes': ''},
                {'objective': 'Protect internal network boundaries', 'notes': ''},
                {'objective': 'Implement communication controls', 'notes': ''}
            ]
        }
        
        for control in controls:
            control['objectives'] = objectives_map.get(control['id'], [
                {'objective': f'Define implementation approach for {control["id"]}', 'notes': ''},
                {'objective': f'Execute {control["id"]} requirements', 'notes': ''},
                {'objective': f'Validate {control["id"]} effectiveness', 'notes': ''}
            ])

        # Save initial controls to database
        for control in controls:
            save_control(control)
        return jsonify(controls)
    else:
        return jsonify(db_controls)

@app.route('/api/controls/<control_id>', methods=['PUT'])
def update_control(control_id):
    data = request.get_json()
    # Update control in database
    save_control(data)
    return jsonify({'status': 'success'})

@app.route('/api/controls/<control_id>/notes', methods=['PUT'])
def update_control_notes(control_id):
    """Update notes for a specific control's objectives"""
    data = request.get_json()
    
    # Get the current control from database
    db_controls = db_get_controls()
    control = next((c for c in db_controls if c['id'] == control_id), None)
    
    if not control:
        return jsonify({'error': 'Control not found'}), 404
    
    # Update the notes for the specific objective
    objective_index = data.get('objective_index')
    new_notes = data.get('notes', '')
    
    if objective_index is not None and 0 <= objective_index < len(control['objectives']):
        control['objectives'][objective_index]['notes'] = new_notes
        save_control(control)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Invalid objective index'}), 400

@app.route('/api/poams')
def get_poams():
    return jsonify(db_get_poams())

@app.route('/api/poams', methods=['POST'])
def create_poam():
    data = request.get_json()
    poam_id = save_poam(data)
    return jsonify({'id': poam_id, 'status': 'created'})

@app.route('/api/poams/<int:poam_id>', methods=['PUT'])
def update_poam_api(poam_id):
    data = request.get_json()
    update_poam(poam_id, data)
    return jsonify({'status': 'updated'})

@app.route('/api/poams/<int:poam_id>', methods=['DELETE'])
def delete_poam_api(poam_id):
    delete_poam(poam_id)
    return jsonify({'status': 'deleted'})

@app.route('/api/export/poams')
def export_poams():
    poams = db_get_poams()
    return jsonify(poams)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)
