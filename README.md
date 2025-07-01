# CMMC Level 2 Compliance Tracker

## ✅ **COMPLETE IMPLEMENTATION** ✅
**112 Controls | 251 Assessment Objectives | Individual Note-Taking**

A comprehensive web-based application for tracking CMMC (Cybersecurity Maturity Model Certification) Level 2 compliance with all controls and assessment objectives, including individual note-taking capabilities for detailed compliance documentation.
![image](https://github.com/user-attachments/assets/2e3cb054-d0c9-4a11-912d-f02b5607ebe6)

## Features

- **Visual Dashboard**: Overview of compliance status with charts and metrics
- **Controls Management**: Track implementation status of all CMMC Level 2 controls
- **POA&M Management**: Create, manage, and track Plans of Action and Milestones
- **Artifact Storage**: Upload and manage compliance documentation and evidence
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Navigate to the project directory:
   ```bash
   cd /Users/brandon/Desktop/cmmc-compliance-tracker
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask development server:
   ```bash
   python app/main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Dashboard
- View overall compliance percentage
- See active POA&Ms count
- Track controls implementation progress
- Monitor high-priority issues
- View compliance by domain charts

### Controls Management
- Filter controls by domain (AC, AT, AU, CM, etc.)
- Filter by implementation status
- View detailed control descriptions
- Track implementation progress

### POA&M Management
- Create new POA&Ms with priority levels
- Assign due dates and responsible parties
- Link POA&Ms to specific controls
- Track progress and updates

### Artifact Management
- Upload compliance documents
- Drag-and-drop file upload
- View uploaded artifacts
- Organize documentation by control area

## File Structure

```
cmmc-compliance-tracker/
├── app/
│   ├── main.py              # Flask application
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Application styles
│   │   ├── js/
│   │   │   └── app.js       # Frontend JavaScript
│   │   └── uploads/         # Uploaded files storage
│   └── templates/
│       └── index.html       # Main HTML template
├── data/                    # Data storage (future expansion)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Next Steps for Production

1. **Database Integration**: Replace in-memory data with a proper database (SQLite, PostgreSQL, etc.)
2. **Authentication**: Add user authentication and role-based access control
3. **API Development**: Create REST API endpoints for data management
4. **Data Persistence**: Implement proper data storage for controls, POA&Ms, and artifacts
5. **Reporting**: Add PDF report generation capabilities
6. **Integration**: Connect with existing security tools and CMMC assessment platforms
7. **Backup**: Implement regular data backup procedures
8. **Security**: Add input validation, CSRF protection, and other security measures

## CMMC Level 2 Control Domains

The application tracks controls across these domains:
- **AC**: Access Control
- **AT**: Awareness and Training
- **AU**: Audit and Accountability
- **CM**: Configuration Management
- **IA**: Identification and Authentication
- **IR**: Incident Response
- **MA**: Maintenance
- **MP**: Media Protection
- **PE**: Physical Protection
- **PS**: Personnel Security
- **RA**: Risk Assessment
- **SA**: System and Services Acquisition
- **SC**: System and Communications Protection
- **SI**: System and Information Integrity

## Support

This is a prototype application designed to demonstrate CMMC compliance tracking capabilities. For production use, additional development and security hardening would be required.
