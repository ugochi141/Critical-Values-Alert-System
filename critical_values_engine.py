#!/usr/bin/env python3
"""
Enhanced Critical Values Alert System
Real-time monitoring and alerting for laboratory critical values
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CriticalValuesEngine:
    """Core engine for critical value detection and alerting"""

    def __init__(self):
        self.critical_ranges = self.load_critical_ranges()
        self.alert_history = []
        self.escalation_matrix = self.setup_escalation_matrix()

    def load_critical_ranges(self) -> Dict:
        """Load critical value ranges for different tests"""
        return {
            # Chemistry Panel
            "glucose": {"low": 40, "high": 500, "unit": "mg/dL", "panic": {"low": 30, "high": 600}},
            "sodium": {"low": 120, "high": 160, "unit": "mEq/L", "panic": {"low": 115, "high": 165}},
            "potassium": {"low": 2.5, "high": 6.5, "unit": "mEq/L", "panic": {"low": 2.0, "high": 7.0}},
            "calcium": {"low": 6.0, "high": 13.0, "unit": "mg/dL", "panic": {"low": 5.0, "high": 14.0}},
            "creatinine": {"low": None, "high": 7.0, "unit": "mg/dL", "panic": {"low": None, "high": 10.0}},

            # Hematology
            "hemoglobin": {"low": 7.0, "high": 20.0, "unit": "g/dL", "panic": {"low": 5.0, "high": 22.0}},
            "wbc": {"low": 2.0, "high": 30.0, "unit": "K/μL", "panic": {"low": 1.0, "high": 50.0}},
            "platelets": {"low": 50, "high": 1000, "unit": "K/μL", "panic": {"low": 20, "high": 1500}},
            "inr": {"low": None, "high": 4.5, "unit": "", "panic": {"low": None, "high": 6.0}},

            # Blood Gases
            "ph": {"low": 7.20, "high": 7.60, "unit": "", "panic": {"low": 7.10, "high": 7.70}},
            "pco2": {"low": 20, "high": 60, "unit": "mmHg", "panic": {"low": 15, "high": 70}},
            "po2": {"low": 50, "high": None, "unit": "mmHg", "panic": {"low": 40, "high": None}},

            # Cardiac Markers
            "troponin": {"low": None, "high": 0.04, "unit": "ng/mL", "panic": {"low": None, "high": 0.1}},
            "bnp": {"low": None, "high": 900, "unit": "pg/mL", "panic": {"low": None, "high": 2000}},

            # Microbiology
            "positive_blood_culture": {"alert": True, "priority": "CRITICAL"},
            "csf_positive": {"alert": True, "priority": "CRITICAL"},
        }

    def setup_escalation_matrix(self) -> Dict:
        """Define escalation paths for different severity levels"""
        return {
            "CRITICAL": {
                "primary": ["attending_physician", "charge_nurse"],
                "escalation_time": 5,  # minutes
                "secondary": ["medical_director", "nursing_supervisor"],
                "final": ["chief_medical_officer"]
            },
            "HIGH": {
                "primary": ["attending_physician"],
                "escalation_time": 15,
                "secondary": ["charge_nurse", "on_call_physician"],
                "final": ["medical_director"]
            },
            "MODERATE": {
                "primary": ["primary_nurse"],
                "escalation_time": 30,
                "secondary": ["attending_physician"],
                "final": ["charge_nurse"]
            }
        }

    def check_critical_value(self, test_name: str, value: float, patient_id: str) -> Optional[Dict]:
        """Check if a test result is critical"""
        if test_name not in self.critical_ranges:
            return None

        ranges = self.critical_ranges[test_name]

        # Skip if not a numeric test
        if isinstance(ranges.get("alert"), bool):
            return {"severity": ranges.get("priority", "HIGH"), "test": test_name}

        alert = None
        severity = None

        # Check panic values first
        panic = ranges.get("panic", {})
        if panic.get("low") and value < panic["low"]:
            severity = "CRITICAL"
            alert = f"PANIC LOW: {test_name} = {value} {ranges['unit']} (< {panic['low']})"
        elif panic.get("high") and value > panic["high"]:
            severity = "CRITICAL"
            alert = f"PANIC HIGH: {test_name} = {value} {ranges['unit']} (> {panic['high']})"

        # Check critical values
        elif ranges.get("low") and value < ranges["low"]:
            severity = "HIGH"
            alert = f"CRITICAL LOW: {test_name} = {value} {ranges['unit']} (< {ranges['low']})"
        elif ranges.get("high") and value > ranges["high"]:
            severity = "HIGH"
            alert = f"CRITICAL HIGH: {test_name} = {value} {ranges['unit']} (> {ranges['high']})"

        if alert:
            return {
                "patient_id": patient_id,
                "test": test_name,
                "value": value,
                "unit": ranges.get("unit", ""),
                "severity": severity,
                "message": alert,
                "timestamp": datetime.now().isoformat()
            }

        return None

    def send_alert(self, alert: Dict) -> bool:
        """Send alert through multiple channels"""
        try:
            # Log the alert
            logging.critical(f"CRITICAL VALUE ALERT: {alert['message']}")
            self.alert_history.append(alert)

            # Get escalation path
            escalation = self.escalation_matrix.get(alert["severity"])

            # Send to primary contacts
            for contact_role in escalation["primary"]:
                self.notify_contact(contact_role, alert)

            # Schedule escalation if needed
            self.schedule_escalation(alert, escalation)

            return True

        except Exception as e:
            logging.error(f"Failed to send alert: {e}")
            return False

    def notify_contact(self, role: str, alert: Dict):
        """Send notification to specific contact role"""
        # This would integrate with actual notification systems
        # For now, we'll simulate it
        logging.info(f"Notifying {role}: {alert['message']}")

        # In production, this would:
        # - Send SMS via Twilio
        # - Send email
        # - Send pager alert
        # - Update dashboard
        # - Log to audit trail

    def schedule_escalation(self, alert: Dict, escalation: Dict):
        """Schedule automatic escalation if not acknowledged"""
        # In production, this would use a task queue like Celery
        logging.info(f"Escalation scheduled in {escalation['escalation_time']} minutes if not acknowledged")

    def generate_alert_summary(self) -> pd.DataFrame:
        """Generate summary of all alerts"""
        if not self.alert_history:
            return pd.DataFrame()

        df = pd.DataFrame(self.alert_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Add response time calculation
        df['acknowledged'] = False  # Would be updated by acknowledgment system
        df['response_time_minutes'] = None

        return df

    def calculate_metrics(self) -> Dict:
        """Calculate performance metrics for critical value management"""
        if not self.alert_history:
            return {}

        df = self.generate_alert_summary()

        metrics = {
            "total_alerts": len(df),
            "critical_alerts": len(df[df['severity'] == 'CRITICAL']),
            "high_alerts": len(df[df['severity'] == 'HIGH']),
            "average_response_time": df['response_time_minutes'].mean() if 'response_time_minutes' in df else None,
            "acknowledgment_rate": (df['acknowledged'].sum() / len(df) * 100) if len(df) > 0 else 0
        }

        return metrics


class CriticalValueMonitor:
    """Real-time monitoring system for critical values"""

    def __init__(self, engine: CriticalValuesEngine):
        self.engine = engine
        self.active_monitors = {}

    def start_monitoring(self, data_source: str):
        """Start monitoring a data source for critical values"""
        logging.info(f"Starting critical value monitoring for {data_source}")

        # In production, this would connect to LIS/EMR systems
        # For demonstration, we'll simulate data
        self.simulate_lab_results()

    def simulate_lab_results(self):
        """Simulate incoming lab results for testing"""
        # Generate some test data with critical values
        test_results = [
            {"patient_id": "P001", "test": "potassium", "value": 6.8},  # Critical high
            {"patient_id": "P002", "test": "glucose", "value": 35},      # Panic low
            {"patient_id": "P003", "test": "hemoglobin", "value": 6.5},  # Critical low
            {"patient_id": "P004", "test": "troponin", "value": 0.08},   # Panic high
            {"patient_id": "P005", "test": "ph", "value": 7.15},         # Panic low
        ]

        for result in test_results:
            alert = self.engine.check_critical_value(
                result["test"],
                result["value"],
                result["patient_id"]
            )

            if alert:
                self.engine.send_alert(alert)

    def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display"""
        return {
            "alerts": self.engine.alert_history,
            "metrics": self.engine.calculate_metrics(),
            "last_update": datetime.now().isoformat()
        }


# Integration with notification systems
class NotificationManager:
    """Manage multi-channel notifications"""

    def __init__(self):
        self.channels = self.setup_channels()

    def setup_channels(self):
        """Setup notification channels"""
        return {
            "email": self.send_email,
            "sms": self.send_sms,
            "teams": self.send_teams,
            "pager": self.send_pager
        }

    def send_email(self, recipient: str, alert: Dict):
        """Send email notification"""
        # Email implementation
        pass

    def send_sms(self, phone: str, alert: Dict):
        """Send SMS notification via Twilio"""
        # SMS implementation
        pass

    def send_teams(self, channel: str, alert: Dict):
        """Send Microsoft Teams notification"""
        # Teams webhook implementation
        pass

    def send_pager(self, pager_id: str, alert: Dict):
        """Send pager alert"""
        # Pager system integration
        pass


if __name__ == "__main__":
    # Initialize the critical values engine
    engine = CriticalValuesEngine()

    # Start monitoring
    monitor = CriticalValueMonitor(engine)
    monitor.start_monitoring("LIS_PROD")

    # Display metrics
    metrics = engine.calculate_metrics()
    print("\n📊 Critical Value Alert Metrics:")
    print(json.dumps(metrics, indent=2))

    # Display alert summary
    summary = engine.generate_alert_summary()
    if not summary.empty:
        print("\n🚨 Alert Summary:")
        print(summary.to_string())