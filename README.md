
## Dental Clinic CRM

**Dental Clinic CRM** is a lightweight, modular system designed to help dental clinics manage patient leads, appointments, treatments, and payments in one integrated platform.

### 🚀 Features

* **Leads Management**
  Track potential patients (leads) — add, edit, delete — with status and source metadata.

* **Patient Profiles**
  Store patient data (contact info, history, notes) and link them to appointments and payments.

* **Appointments / Scheduling**
  Schedule appointments by date, time, service, and doctor. Mark visits as completed, view daily calendar.

* **Treatment Records & Receipts**
  After a completed appointment, record the procedures and generate a receipt for the patient.

* **Payments Module**
  Log payments (cash, card, online), track income and balances, filter by patient or date.

* **Dashboard & Statistics**
  A summary of clinic metrics: number of patients, today’s appointments, income, new leads.

* **Role-based Access & Authentication**
  Admins / staff have full access, doctors have restricted access (e.g. only their appointments).

* **Clean Architecture Using Django + DRF**
  Backend built with Django and Django REST Framework, serving JSON APIs for frontend.

* **Frontend-ready UI structure**
  Designed to pair with your existing HTML + TailwindCSS frontend for seamless integration.

### 🧱 Project Structure (Highlights)

The repository includes these main Django apps:

* `leads`
* `patients`
* `appointments`
* `receipts`
* `payments`
* `dashboard`

You’ll also find settings, routing, and templating infrastructure under `dentalcrm`, and a basic SQLite database for development.

### 🛠 Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Rashidov21/dental-clinic-crm.git
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv  
   source venv/bin/activate  
   pip install -r requirements.txt
   ```

3. Apply migrations and run the server:

   ```bash
   python manage.py migrate  
   python manage.py runserver
   ```

4. Access the API endpoints (e.g., `/api/leads/`, `/api/patients/`) and integrate with your frontend.

### 🌟 Why Use This?

* Saves development time by providing ready-to-use backend logic for common clinic workflows.
* Easily customizable — you can extend models, endpoints, or access rules.
* Designed for integration with clean, responsive frontend (HTML + TailwindCSS).

---


