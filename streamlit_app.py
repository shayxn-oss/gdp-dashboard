import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

# Initialize temporary data
if "patients" not in st.session_state:
    st.session_state.patients = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

st.title("🏥 Hospital Management System")
st.write("Manage patients and appointments.")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Register Patient", "Book Appointment", "View Records"]
)

# Dashboard
if menu == "Dashboard":
    st.header("Hospital Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Patients", len(st.session_state.patients))

    with col2:
        st.metric(
            "Total Appointments",
            len(st.session_state.appointments)
        )

    st.info("Use the sidebar to manage hospital records.")

# Patient registration
elif menu == "Register Patient":
    st.header("Register a New Patient")

    with st.form("patient_form"):
        name = st.text_input("Patient Name")
        age = st.number_input(
            "Age", min_value=0, max_value=120, value=18
        )
        gender = st.selectbox(
            "Gender", ["Female", "Male", "Other"]
        )
        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button("Register Patient")

    if submitted:
        if not name.strip():
            st.error("Please enter the patient's name.")
        else:
            patient_id = f"P{len(st.session_state.patients) + 1:03d}"

            st.session_state.patients.append({
                "Patient ID": patient_id,
                "Name": name.strip(),
                "Age": int(age),
                "Gender": gender,
                "Phone": phone.strip()
            })

            st.success(f"Patient registered successfully! ID: {patient_id}")

# Appointment booking
elif menu == "Book Appointment":
    st.header("Book an Appointment")

    if not st.session_state.patients:
        st.warning("Register a patient before booking an appointment.")
    else:
        patient_options = {
            f"{p['Patient ID']} - {p['Name']}": p["Patient ID"]
            for p in st.session_state.patients
        }

        with st.form("appointment_form"):
            selected_patient = st.selectbox(
                "Select Patient", list(patient_options.keys())
            )

            doctor = st.selectbox(
                "Select Doctor",
                ["Dr. Ahmed", "Dr. Fatima", "Dr. Ali"]
            )

            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")

            submitted = st.form_submit_button("Book Appointment")

        if submitted:
            patient_id = patient_options[selected_patient]

            # Prevent double-booking the same doctor and time
            conflict = any(
                a["Doctor"] == doctor
                and a["Date"] == str(appointment_date)
                and a["Time"] == appointment_time.strftime("%H:%M")
                for a in st.session_state.appointments
            )

            if conflict:
                st.error("This doctor already has an appointment at that time.")
            else:
                st.session_state.appointments.append({
                    "Patient ID": patient_id,
                    "Patient": selected_patient,
                    "Doctor": doctor,
                    "Date": str(appointment_date),
                    "Time": appointment_time.strftime("%H:%M")
                })

                st.success("Appointment booked successfully!")

# View records
elif menu == "View Records":
    st.header("Hospital Records")

    st.subheader("Patient Records")

    patients_df = pd.DataFrame(st.session_state.patients)

    if not patients_df.empty:
        search = st.text_input("Search patients by name or ID")

        filtered = patients_df[
            patients_df["Name"].str.contains(search, case=False, na=False)
            | patients_df["Patient ID"].str.contains(
                search, case=False, na=False
            )
        ]

        st.dataframe(filtered, use_container_width=True)
    else:
        st.info("No patients registered yet.")

    st.subheader("Appointment Records")

    appointments_df = pd.DataFrame(st.session_state.appointments)

    if not appointments_df.empty:
        st.dataframe(appointments_df, use_container_width=True)
    else:
        st.info("No appointments booked yet.")