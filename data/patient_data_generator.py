"""
Comprehensive EHR Lab Data Generator
Generates realistic patient demographics, lab orders, and results for healthcare informatics systems
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from faker import Faker
import json

fake = Faker()

class LabDataGenerator:
    def __init__(self):
        self.test_panels = {
            'CBC': {
                'name': 'Complete Blood Count',
                'components': {
                    'WBC': {'unit': 'K/uL', 'normal': (4.5, 11.0), 'critical_low': 2.0, 'critical_high': 50.0},
                    'RBC': {'unit': 'M/uL', 'normal': (4.5, 5.5), 'critical_low': 2.0, 'critical_high': 7.0},
                    'Hemoglobin': {'unit': 'g/dL', 'normal': (12.0, 16.0), 'critical_low': 7.0, 'critical_high': 20.0},
                    'Hematocrit': {'unit': '%', 'normal': (36, 48), 'critical_low': 20, 'critical_high': 60},
                    'Platelets': {'unit': 'K/uL', 'normal': (150, 450), 'critical_low': 50, 'critical_high': 1000}
                },
                'department': 'Hematology',
                'tat_hours': (2, 6)
            },
            'BMP': {
                'name': 'Basic Metabolic Panel',
                'components': {
                    'Glucose': {'unit': 'mg/dL', 'normal': (70, 100), 'critical_low': 40, 'critical_high': 400},
                    'BUN': {'unit': 'mg/dL', 'normal': (7, 20), 'critical_low': 2, 'critical_high': 100},
                    'Creatinine': {'unit': 'mg/dL', 'normal': (0.6, 1.2), 'critical_low': 0.2, 'critical_high': 10.0},
                    'Sodium': {'unit': 'mEq/L', 'normal': (136, 145), 'critical_low': 120, 'critical_high': 160},
                    'Potassium': {'unit': 'mEq/L', 'normal': (3.5, 5.0), 'critical_low': 2.5, 'critical_high': 6.0},
                    'Chloride': {'unit': 'mEq/L', 'normal': (98, 107), 'critical_low': 80, 'critical_high': 120},
                    'CO2': {'unit': 'mEq/L', 'normal': (22, 28), 'critical_low': 10, 'critical_high': 40}
                },
                'department': 'Chemistry',
                'tat_hours': (1, 4)
            },
            'CMP': {
                'name': 'Comprehensive Metabolic Panel',
                'components': {
                    'Glucose': {'unit': 'mg/dL', 'normal': (70, 100), 'critical_low': 40, 'critical_high': 400},
                    'BUN': {'unit': 'mg/dL', 'normal': (7, 20), 'critical_low': 2, 'critical_high': 100},
                    'Creatinine': {'unit': 'mg/dL', 'normal': (0.6, 1.2), 'critical_low': 0.2, 'critical_high': 10.0},
                    'Sodium': {'unit': 'mEq/L', 'normal': (136, 145), 'critical_low': 120, 'critical_high': 160},
                    'Potassium': {'unit': 'mEq/L', 'normal': (3.5, 5.0), 'critical_low': 2.5, 'critical_high': 6.0},
                    'Chloride': {'unit': 'mEq/L', 'normal': (98, 107), 'critical_low': 80, 'critical_high': 120},
                    'CO2': {'unit': 'mEq/L', 'normal': (22, 28), 'critical_low': 10, 'critical_high': 40},
                    'Total_Protein': {'unit': 'g/dL', 'normal': (6.0, 8.3), 'critical_low': 3.0, 'critical_high': 12.0},
                    'Albumin': {'unit': 'g/dL', 'normal': (3.5, 5.0), 'critical_low': 1.5, 'critical_high': 6.0},
                    'Total_Bilirubin': {'unit': 'mg/dL', 'normal': (0.2, 1.2), 'critical_low': None, 'critical_high': 15.0},
                    'AST': {'unit': 'U/L', 'normal': (10, 40), 'critical_low': None, 'critical_high': 1000},
                    'ALT': {'unit': 'U/L', 'normal': (7, 35), 'critical_low': None, 'critical_high': 1000},
                    'Alkaline_Phosphatase': {'unit': 'U/L', 'normal': (44, 147), 'critical_low': None, 'critical_high': 500}
                },
                'department': 'Chemistry',
                'tat_hours': (2, 6)
            },
            'Lipid_Panel': {
                'name': 'Lipid Panel',
                'components': {
                    'Total_Cholesterol': {'unit': 'mg/dL', 'normal': (100, 200), 'critical_low': None, 'critical_high': 400},
                    'HDL_Cholesterol': {'unit': 'mg/dL', 'normal': (40, 100), 'critical_low': 20, 'critical_high': None},
                    'LDL_Cholesterol': {'unit': 'mg/dL', 'normal': (70, 130), 'critical_low': None, 'critical_high': 300},
                    'Triglycerides': {'unit': 'mg/dL', 'normal': (50, 150), 'critical_low': None, 'critical_high': 1000}
                },
                'department': 'Chemistry',
                'tat_hours': (4, 8)
            },
            'Thyroid_Panel': {
                'name': 'Thyroid Function Panel',
                'components': {
                    'TSH': {'unit': 'mIU/L', 'normal': (0.4, 4.0), 'critical_low': 0.01, 'critical_high': 100.0},
                    'Free_T4': {'unit': 'ng/dL', 'normal': (0.8, 1.8), 'critical_low': 0.2, 'critical_high': 5.0},
                    'Free_T3': {'unit': 'pg/mL', 'normal': (2.3, 4.2), 'critical_low': 1.0, 'critical_high': 10.0}
                },
                'department': 'Endocrinology',
                'tat_hours': (6, 24)
            },
            'Cardiac_Markers': {
                'name': 'Cardiac Markers',
                'components': {
                    'Troponin_I': {'unit': 'ng/mL', 'normal': (0.0, 0.04), 'critical_low': None, 'critical_high': 0.1},
                    'CK_MB': {'unit': 'ng/mL', 'normal': (0.0, 6.0), 'critical_low': None, 'critical_high': 25.0},
                    'BNP': {'unit': 'pg/mL', 'normal': (0, 100), 'critical_low': None, 'critical_high': 2000}
                },
                'department': 'Chemistry',
                'tat_hours': (1, 2)
            },
            'Coagulation': {
                'name': 'Coagulation Studies',
                'components': {
                    'PT': {'unit': 'sec', 'normal': (11.0, 14.0), 'critical_low': None, 'critical_high': 30.0},
                    'INR': {'unit': '', 'normal': (0.8, 1.2), 'critical_low': None, 'critical_high': 5.0},
                    'PTT': {'unit': 'sec', 'normal': (25, 35), 'critical_low': None, 'critical_high': 80.0}
                },
                'department': 'Hematology',
                'tat_hours': (1, 3)
            },
            'Urinalysis': {
                'name': 'Urinalysis',
                'components': {
                    'Specific_Gravity': {'unit': '', 'normal': (1.003, 1.030), 'critical_low': 1.000, 'critical_high': 1.040},
                    'Protein': {'unit': 'mg/dL', 'normal': (0, 20), 'critical_low': None, 'critical_high': 500},
                    'Glucose': {'unit': 'mg/dL', 'normal': (0, 15), 'critical_low': None, 'critical_high': 1000},
                    'WBC_Urine': {'unit': '/hpf', 'normal': (0, 5), 'critical_low': None, 'critical_high': 50},
                    'RBC_Urine': {'unit': '/hpf', 'normal': (0, 2), 'critical_low': None, 'critical_high': 20}
                },
                'department': 'Chemistry',
                'tat_hours': (1, 4)
            }
        }
        
        self.departments = [
            'Emergency Department', 'ICU', 'Medical Ward', 'Surgical Ward', 
            'Cardiology', 'Oncology', 'Pediatrics', 'Obstetrics', 'Outpatient Clinic'
        ]
        
        self.physicians = [
            'Dr. Sarah Johnson', 'Dr. Michael Smith', 'Dr. Emily Davis', 'Dr. David Wilson',
            'Dr. Jennifer Brown', 'Dr. Robert Miller', 'Dr. Lisa Anderson', 'Dr. Christopher Taylor',
            'Dr. Michelle Garcia', 'Dr. Andrew Martinez', 'Dr. Jessica Rodriguez', 'Dr. Matthew Thomas',
            'Dr. Amanda Jackson', 'Dr. Kevin White', 'Dr. Nicole Harris', 'Dr. Daniel Martin',
            'Dr. Stephanie Thompson', 'Dr. Brandon Lee', 'Dr. Melissa Walker', 'Dr. James Hall'
        ]
        
        self.facilities = [
            'Main Hospital', 'North Campus', 'South Campus', 'Outpatient Center',
            'Emergency Center', 'Cardiac Center', 'Cancer Center', 'Pediatric Hospital'
        ]
    
    def generate_patients(self, n_patients=1000):
        """Generate realistic patient demographics"""
        patients = []
        
        for i in range(n_patients):
            gender = random.choice(['M', 'F'])
            age = np.random.beta(2, 5) * 90 + 10  # Skewed towards younger ages
            age = int(age)
            
            # Generate realistic names based on gender
            if gender == 'M':
                first_name = fake.first_name_male()
            else:
                first_name = fake.first_name_female()
            
            patient = {
                'Patient_ID': f"PAT{str(i+1).zfill(6)}",
                'MRN': f"MRN{str(i+100001).zfill(6)}",
                'First_Name': first_name,
                'Last_Name': fake.last_name(),
                'Full_Name': f"{first_name} {fake.last_name()}",
                'DOB': fake.date_of_birth(minimum_age=age, maximum_age=age),
                'Age': age,
                'Gender': gender,
                'Race': np.random.choice([
                    'White', 'Black/African American', 'Hispanic/Latino', 
                    'Asian', 'Native American', 'Other', 'Unknown'
                ], p=[0.6, 0.13, 0.18, 0.06, 0.01, 0.01, 0.01]),
                'Address': fake.address().replace('\n', ', '),
                'Phone': fake.phone_number(),
                'Email': fake.email(),
                'Insurance': random.choice([
                    'Medicare', 'Medicaid', 'Blue Cross Blue Shield', 'Aetna', 
                    'Cigna', 'UnitedHealth', 'Private', 'Self-Pay'
                ]),
                'Primary_Physician': random.choice(self.physicians),
                'Emergency_Contact': fake.name(),
                'Emergency_Phone': fake.phone_number(),
                'Allergies': random.choice([
                    'NKDA', 'Penicillin', 'Sulfa', 'Latex', 'Shellfish', 
                    'Nuts', 'Contrast Dye', 'Multiple'
                ]),
                'Registration_Date': fake.date_between(start_date='-2y', end_date='today')
            }
            patients.append(patient)
        
        return pd.DataFrame(patients)
    
    def generate_lab_orders(self, patients_df, n_orders=2000):
        """Generate realistic lab orders"""
        orders = []
        current_time = datetime.now()
        
        for i in range(n_orders):
            patient = patients_df.sample(1).iloc[0]
            
            # Order details
            order_date = fake.date_time_between(start_date='-30d', end_date='now')
            test_panel = random.choice(list(self.test_panels.keys()))
            panel_info = self.test_panels[test_panel]
            
            # Priority based on department and test type
            if random.random() < 0.15:  # 15% STAT orders
                priority = 'STAT'
                tat_multiplier = 0.5
            elif random.random() < 0.25:  # 25% Urgent
                priority = 'Urgent'
                tat_multiplier = 0.75
            else:
                priority = 'Routine'
                tat_multiplier = 1.0
            
            # Calculate expected TAT
            base_tat = random.uniform(*panel_info['tat_hours'])
            expected_tat = base_tat * tat_multiplier
            
            # Status progression
            status_weights = [0.05, 0.10, 0.15, 0.60, 0.10]  # Received, In Progress, Completed, Reported, Cancelled
            status = np.random.choice(
                ['Received', 'In Progress', 'Completed', 'Reported', 'Cancelled'],
                p=status_weights
            )
            
            order = {
                'Order_ID': f"ORD{str(i+1).zfill(8)}",
                'Patient_ID': patient['Patient_ID'],
                'MRN': patient['MRN'],
                'Patient_Name': patient['Full_Name'],
                'Age': patient['Age'],
                'Gender': patient['Gender'],
                'Test_Panel': test_panel,
                'Test_Name': panel_info['name'],
                'Department': panel_info['department'],
                'Priority': priority,
                'Status': status,
                'Order_Date': order_date,
                'Expected_TAT_Hours': round(expected_tat, 1),
                'Ordering_Physician': random.choice(self.physicians),
                'Location': random.choice(self.departments),
                'Facility': random.choice(self.facilities),
                'Specimen_Type': random.choice(['Blood', 'Serum', 'Plasma', 'Urine', 'CSF']),
                'Collection_Date': order_date + timedelta(minutes=random.randint(5, 120)),
                'Received_Date': order_date + timedelta(minutes=random.randint(10, 180)),
                'Clinical_Indication': random.choice([
                    'Routine screening', 'Follow-up', 'Diagnostic workup', 
                    'Pre-operative', 'Monitoring therapy', 'Chest pain', 
                    'Shortness of breath', 'Fatigue', 'Abnormal vital signs'
                ])
            }
            
            # Add completion dates for completed orders
            if status in ['Completed', 'Reported']:
                completion_time = order['Received_Date'] + timedelta(hours=expected_tat)
                order['Completion_Date'] = completion_time
                order['Actual_TAT_Hours'] = round(
                    (completion_time - order['Received_Date']).total_seconds() / 3600, 1
                )
            
            orders.append(order)
        
        return pd.DataFrame(orders)
    
    def generate_lab_results(self, orders_df, n_results=5000):
        """Generate realistic lab results with critical values"""
        results = []
        
        for _, order in orders_df.iterrows():
            if order['Status'] not in ['Completed', 'Reported']:
                continue
                
            panel_info = self.test_panels.get(order['Test_Panel'])
            if not panel_info:
                continue
            
            for component_name, component_info in panel_info['components'].items():
                # Determine if result should be critical
                prob = random.random()
                
                if prob < 0.02:  # 2% panic values
                    if component_info['critical_high']:
                        value = random.uniform(
                            component_info['critical_high'],
                            component_info['critical_high'] * 1.5
                        )
                    else:
                        value = random.uniform(*component_info['normal'])
                    result_flag = 'PANIC'
                elif prob < 0.08:  # 6% critical values
                    if component_info['critical_low'] and component_info['critical_high']:
                        if random.choice([True, False]):
                            value = random.uniform(
                                component_info['critical_low'],
                                component_info['normal'][0]
                            )
                        else:
                            value = random.uniform(
                                component_info['normal'][1],
                                component_info['critical_high']
                            )
                    elif component_info['critical_high']:
                        value = random.uniform(
                            component_info['normal'][1],
                            component_info['critical_high']
                        )
                    else:
                        value = random.uniform(*component_info['normal'])
                    result_flag = 'CRITICAL'
                elif prob < 0.25:  # 17% abnormal values
                    if random.choice([True, False]):
                        value = random.uniform(
                            component_info['normal'][0] * 0.7,
                            component_info['normal'][0]
                        )
                    else:
                        value = random.uniform(
                            component_info['normal'][1],
                            component_info['normal'][1] * 1.3
                        )
                    result_flag = 'ABNORMAL'
                else:  # Normal values
                    value = random.uniform(*component_info['normal'])
                    result_flag = 'NORMAL'
                
                # Round appropriately
                if component_name in ['WBC_Urine', 'RBC_Urine']:
                    value = int(value)
                elif 'Count' in component_name or component_name in ['Glucose', 'BUN', 'Sodium', 'Potassium']:
                    value = round(value, 1)
                else:
                    value = round(value, 2)
                
                result = {
                    'Result_ID': f"RES{len(results)+1:08d}",
                    'Order_ID': order['Order_ID'],
                    'Patient_ID': order['Patient_ID'],
                    'MRN': order['MRN'],
                    'Patient_Name': order['Patient_Name'],
                    'Test_Panel': order['Test_Panel'],
                    'Component_Name': component_name,
                    'Result_Value': value,
                    'Unit': component_info['unit'],
                    'Reference_Range': f"{component_info['normal'][0]}-{component_info['normal'][1]}",
                    'Result_Flag': result_flag,
                    'Department': order['Department'],
                    'Result_Date': order.get('Completion_Date', datetime.now()),
                    'Reviewing_Pathologist': random.choice(self.physicians),
                    'Method': random.choice(['Automated', 'Manual', 'POCT', 'Send-out']),
                    'Instrument': random.choice([
                        'Sysmex XN-1000', 'Abbott Architect', 'Roche Cobas', 
                        'Beckman AU680', 'Siemens Atellica', 'Ortho Vision'
                    ]),
                    'Critical_Called': result_flag in ['CRITICAL', 'PANIC'],
                    'Call_Time': datetime.now() if result_flag in ['CRITICAL', 'PANIC'] else None,
                    'Called_To': order['Ordering_Physician'] if result_flag in ['CRITICAL', 'PANIC'] else None
                }
                
                results.append(result)
        
        return pd.DataFrame(results)
    
    def generate_complete_dataset(self, n_patients=500, n_orders=1000, n_results=3000):
        """Generate complete EHR lab dataset"""
        print("Generating patients...")
        patients = self.generate_patients(n_patients)
        
        print("Generating lab orders...")
        orders = self.generate_lab_orders(patients, n_orders)
        
        print("Generating lab results...")
        results = self.generate_lab_results(orders, n_results)
        
        return {
            'patients': patients,
            'orders': orders,
            'results': results
        }
    
    def save_datasets(self, datasets, output_dir='./data'):
        """Save datasets to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, df in datasets.items():
            filepath = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(filepath, index=False)
            print(f"Saved {name} dataset: {len(df)} records -> {filepath}")
    
    def get_test_catalog(self):
        """Return the complete test catalog"""
        catalog = []
        for panel_code, panel_info in self.test_panels.items():
            for component, details in panel_info['components'].items():
                catalog.append({
                    'Panel_Code': panel_code,
                    'Panel_Name': panel_info['name'],
                    'Component_Name': component,
                    'Unit': details['unit'],
                    'Normal_Low': details['normal'][0],
                    'Normal_High': details['normal'][1],
                    'Critical_Low': details.get('critical_low'),
                    'Critical_High': details.get('critical_high'),
                    'Department': panel_info['department'],
                    'TAT_Hours_Min': panel_info['tat_hours'][0],
                    'TAT_Hours_Max': panel_info['tat_hours'][1]
                })
        return pd.DataFrame(catalog)

# Example usage
if __name__ == "__main__":
    generator = LabDataGenerator()
    
    # Generate complete dataset
    datasets = generator.generate_complete_dataset(
        n_patients=1000,
        n_orders=2000,
        n_results=5000
    )
    
    # Save to CSV files
    generator.save_datasets(datasets)
    
    # Save test catalog
    catalog = generator.get_test_catalog()
    catalog.to_csv('./data/test_catalog.csv', index=False)
    
    print("\nDataset Generation Complete!")
    print(f"Patients: {len(datasets['patients'])}")
    print(f"Orders: {len(datasets['orders'])}")
    print(f"Results: {len(datasets['results'])}")
    print(f"Test Catalog: {len(catalog)} test components")