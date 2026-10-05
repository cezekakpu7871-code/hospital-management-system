import hashlib
import json
import os
from base64 import b64encode, b64decode

class SecurityManager:
    """Handles data encryption, decryption, and password hashing."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes passwords securely using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def Simple_encrypt(data: str, key: int = 7) -> str:
        """Encrypts sensitive patient data using a basic transposition cipher."""
        encrypted_chars = [chr(ord(char) ^ key) for char in data]
        return b64encode("".join(encrypted_chars).encode()).decode()

    @staticmethod
    def simple_decrypt(encoded_data: str, key: int = 7) -> str:
        """Decrypts encrypted patient data."""
        decoded_data = b64decode(encoded_data.encode()).decode()
        return "".join([chr(ord(char) ^ key) for char in decoded_data])


class User:
    """Base class for all system users."""
    def __init__(self, user_id: str, name: str, role: str, password_hash: str):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.password_hash = password_hash


class Patient:
    """Represents a patient record within the healthcare system."""
    def __init__(self, patient_id: str, name: str, age: int, medical_history: str):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        # Encrypt sensitive medical history at rest
        self.encrypted_history = SecurityManager.simple_encrypt(medical_history)

    def get_medical_history(self) -> str:
        """Decrypts and returns the patient's medical history."""
        return SecurityManager.simple_decrypt(self.encrypted_history)

    def to_dict(self) -> dict:
        """Serializes patient data for storage."""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "encrypted_history": self.encrypted_history
        }


class HospitalManagementSystem:
    """Core administrative system for managing patient records and appointments."""
    
    def __init__(self):
        self.patients = {}
        self.appointments = []

    def register_patient(self, patient_id: str, name: str, age: int, medical_history: str):
        """Registers a new patient and encrypts their records."""
        if patient_id in self.patients:
            raise ValueError(f"Patient ID {patient_id} already exists.")
        
        patient = Patient(patient_id, name, age, medical_history)
        self.patients[patient_id] = patient
        print(f"[SUCCESS] Patient {name} (ID: {patient_id}) registered successfully.")

    def schedule_appointment(self, patient_id: str, doctor_name: str, date_time: str):
        """Schedules a clinical appointment for a registered patient."""
        if patient_id not in self.patients:
            raise KeyError(f"Patient ID {patient_id} not found.")
        
        appointment = {
            "patient_id": patient_id,
            "patient_name": self.patients[patient_id].name,
            "doctor_name": doctor_name,
            "date_time": date_time
        }
        self.appointments.append(appointment)
        print(f"[SUCCESS] Appointment scheduled for {self.patients[patient_id].name} with Dr. {doctor_name} on {date_time}.")

    def view_patient_record(self, patient_id: str, requester_role: str):
        """Retrieves patient information based on access permissions."""
        if patient_id not in self.patients:
            print(f"[ERROR] Patient ID {patient_id} not found.")
            return

        patient = self.patients[patient_id]
        print(f"\n--- Patient File: {patient.name} ---")
        print(f"ID: {patient.patient_id}")
        print(f"Age: {patient.age}")
        
        # Role-based security check
        if requester_role in ["Doctor", "Administrator"]:
            print(f"Medical History: {patient.get_medical_history()}")
        else:
            print("Medical History: [RESTRICTED ACCESS - Doctor/Admin privileges required]")


# --- Demonstration Run ---
if __name__ == "__main__":
    print("==================================================")
    print(" HOSPITAL MANAGEMENT SYSTEM (DEMO RUN)")
    print("==================================================\n")

    hms = HospitalManagementSystem()

    # 1. Register Patients
    hms.register_patient("PAT-001", "Amara Okeke", 34, "Hypertension diagnosed in 2022. Allergic to Penicillin.")
    hms.register_patient("PAT-002", "Ibrahim Musa", 45, "Type 2 Diabetes. Daily Insulin treatment.")

    # 2. Schedule Appointments
    print()
    hms.schedule_appointment("PAT-001", "Dr. Adeleke", "2026-10-12 10:00 AM")
    hms.schedule_appointment("PAT-002", "Dr. Chidubem", "2026-10-12 11:30 AM")

    # 3. Access Patient Records (Role-Based Access Control)
    print("\n--- Access Attempt 1: Receptionist Role ---")
    hms.view_patient_record("PAT-001", requester_role="Receptionist")

    print("\n--- Access Attempt 2: Doctor Role ---")
    hms.view_patient_record("PAT-001", requester_role="Doctor")
