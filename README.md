# Critical Values Alert System

## Description
The Critical Values Alert System is an automated tool designed to monitor laboratory test results and immediately notify healthcare providers when critical values are detected. This system enhances patient safety by ensuring rapid communication of potentially life-threatening test results, reducing the risk of delayed treatment and improving overall clinical outcomes.

## Features
- Real-time monitoring of laboratory results
- Automated alerts for critical values
- Customizable alert thresholds for different tests
- Seamless integration with existing Laboratory Information Systems (LIS)
- Secure, HIPAA-compliant messaging to healthcare providers
- Multi-channel notifications (email, SMS, in-app alerts)
- Audit trail for all alerts and acknowledgments
- User-friendly dashboard for result tracking and system management
- Scalable architecture to handle high volumes of test results

## Installation
1. Clone the repository:
   git clone https://github.com/ugochi141/Critical-Values-Alert-System.git
2. Navigate to the project directory:
   cd Critical-Values-Alert-System
3. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
4. Install required dependencies:
   pip install -r requirements.txt

Markdown
copy
Open in Browser
4. Set up the configuration file (see Configuration section below)

## Usage
1. Start the alert system:
python main.py

Markdown
copy
Open in Browser
2. Access the web dashboard at `http://localhost:5000`
3. Log in with your credentials
4. Monitor alerts and manage settings through the dashboard

## Configuration
1. Copy `config_example.json` to `config.json`
2. Edit `config.json` to set up:
- LIS connection details
- Alert thresholds for different tests
- Notification preferences
- User authentication settings

For detailed configuration instructions, see the [Configuration Guide](docs/configuration.md).

## Dependencies
- Python 3.8+
- PostgreSQL 12+
- Flask 2.0+
- SQLAlchemy 1.4+
- Twilio API (for SMS alerts)
- See `requirements.txt` for a full list of Python package dependencies

## Contributing
We welcome contributions to the Critical Values Alert System. Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact
Ugochi Ndubuisi - u.l.ndubuisi@gmail.com
Project Link: https://github.com/ugochi141/Critical-Values-Alert-System
