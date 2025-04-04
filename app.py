import os
import streamlit as st
from utils import create_draft_with_attachments, get_contact_list
from model import chain,chain2, extract_resume_text
from scheduler import authenticate_google_calendar, create_calendar_event
from datetime import datetime, timedelta
import base64
from constant import HTML_TEMPLATES
# Initialize session state for steps and other variables
if "step" not in st.session_state:
    st.session_state.step = 1
if "attachments" not in st.session_state:
    st.session_state.attachments = []
if "email_body" not in st.session_state:
    st.session_state.email_body = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "contact_list" not in st.session_state:
    st.session_state.contact_list = []
if "to_emails" not in st.session_state:
    st.session_state.to_emails = []

def step_1():
    st.title("Step 1: Upload Resume 📄")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    if resume_file:
        with open(resume_file.name, "wb") as f:
            f.write(resume_file.getvalue())
        st.session_state.resume_text = extract_resume_text(resume_file.name)
        os.remove(resume_file.name)
        # Embed PDF using iframe
        base64_pdf = base64.b64encode(resume_file.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500"></iframe>'
        
        st.markdown(pdf_display, unsafe_allow_html=True)
        st.success("Resume uploaded successfully!")

    if st.button("Next"):
        st.session_state.step += 1

def step_2():
    st.title("Step 2: Select Recipients 📧")

    # Initialize session state variables if not already set
    if "uploaded_contacts" not in st.session_state:
        st.session_state.uploaded_contacts = False
    if "contact_list" not in st.session_state:
        st.session_state.contact_list = []
    if "to_emails" not in st.session_state:
        st.session_state.to_emails = []

    multi_mails = st.file_uploader("Upload txt file (containing email IDs)", type=["txt"], key="contact_file_uploader")

    # Only process file upload if a file is uploaded and contacts haven't been processed yet
    if multi_mails is not None and not st.session_state.uploaded_contacts:
        contact_list = get_contact_list(multi_mails)
        st.session_state.contact_list = contact_list
        st.session_state.uploaded_contacts = True
        st.rerun()  # Force a rerun to update the contact list

    # Only show multiselect if contacts are available
    if st.session_state.contact_list:
        to_emails = st.multiselect(
            "Select Recipients",
            options=st.session_state.contact_list,
            default=st.session_state.to_emails,  # Preserve previous selections
            help="You can select multiple recipients"
        )
    else:
        to_emails = []

    custom_email = st.text_input("Add Custom Email (optional)")
    
    # Add custom email if provided and not already in the list
    if custom_email and custom_email not in to_emails:
        to_emails.append(custom_email)

    # Update session state
    st.session_state.to_emails = to_emails

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            st.session_state.step -= 1
    with col2:
        # Only enable Next button if recipients are selected
        if to_emails:
            if st.button("Next"):
                st.session_state.uploaded_contacts = False  # Reset flag
                st.session_state.step += 1
        else:
            st.warning("Please select at least one recipient")
# import streamlit as st

def step_3():
    st.title("Step 3: Compose Email ✍️")

    # Initialize session state variables
    if "subject" not in st.session_state:
        st.session_state.subject = ""
    if "email_body" not in st.session_state:
        st.session_state.email_body = ""
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""
    if "show_options" not in st.session_state:
        st.session_state.show_options = False
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    # Subject input with preservation
    subject = st.text_input(
        "Email Subject",
        value=st.session_state.subject,
        key="email_subject_input"
    )
    st.session_state.subject = subject

    # Email body generation method
    option = st.selectbox(
        "How would you like to generate the Email Body?",
        ("Generate", "Write", "Template"),
        key="email_body_method"
    )

    if option == "Generate":
        user_input = st.text_area(
            "Enter a brief idea for the email:",
            height=100,
            key="generation_input"
        )

        if st.button("Generate", key="generate_email_btn"):
            if user_input.strip():
                query = user_input
                resume_text = st.session_state.get("resume_text", "")  # Ensure resume_text is retrieved safely
                try:
                    generated_text = chain.invoke({"query": query, "resume_text": resume_text})
                    st.session_state.generated_text = generated_text
                    st.session_state.show_options = True
                    st.session_state.edit_mode = False
                except Exception as e:
                    st.error(f"Error generating email: {e}")
            else:
                st.warning("Please enter a brief idea for email generation")

        if st.session_state.show_options:
            st.markdown("### Generated Email Body:")
            st.markdown(st.session_state.generated_text, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Edit", key="edit_generated_btn"):
                    st.session_state.edit_mode = True

            with col2:
                if st.button("OK", key="confirm_generated_btn"):
                    st.success("Email confirmed!")
                    st.session_state.email_body = st.session_state.generated_text

        if st.session_state.edit_mode:
            edited_text = st.text_area(
                "Edit Email Body:",
                value=st.session_state.generated_text,
                height=200,
                key="edit_generated_input"
            )
            if st.button("Save Changes", key="save_edited_btn"):
                st.session_state.generated_text = edited_text
                st.session_state.email_body = edited_text
                st.session_state.edit_mode = False

    elif option == "Write":
        body = st.text_area(
            "Write an Email Body:",
            value=st.session_state.email_body,
            height=200,
            key="manual_email_body_input"
        )
        st.session_state.email_body = body

    elif option == "Template":
        template_category = st.selectbox(
            "Select Template Category",
            list(HTML_TEMPLATES.keys()),
            key="template_category"
        )

        selected_template = st.selectbox(
            "Choose a Template",
            list(HTML_TEMPLATES[template_category].keys()),
            key="selected_template"
        )

        template_content = HTML_TEMPLATES[template_category][selected_template]

        st.markdown("### Customize Template")
        custom_fields = {
            "[COMPANY_NAME]": st.text_input("Company Name", key="company_name"),
            "[YOUR_NAME]": st.text_input("Your Name", value="Amar Choudhary", key="your_name"),
            "[UNIVERSITY_NAME]": st.text_input("University Name (if applicable)", key="university_name"),
            "[INDUSTRY/FIELD]": st.text_input("Industry/Field", key="industry_field")
        }

        for placeholder, value in custom_fields.items():
            if value:
                template_content = template_content.replace(placeholder, value)

        resume_text = st.session_state.get("resume_text", "")
        try:
            refined_text = chain2.invoke({"template_content": template_content, "resume_text": resume_text})
        except Exception as e:
            st.error(f"Error generating email from template: {e}")
            refined_text = template_content

        st.code(refined_text, language="html")

        edited_template = st.text_area(
            "Edit Template",
            value=refined_text,
            height=300,
            key="template_edit_input"
        )

        if st.button("Use This Template", key="use_template_btn"):
            st.session_state.email_body = edited_template
            st.success(f"Template '{selected_template}' selected!")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous", key="previous_step"):
            st.session_state.step -= 1
    with col2:
        if subject.strip() and st.session_state.email_body.strip():
            if st.button("Next", key="next_step"):
                st.session_state.step += 1
        else:
            st.warning("Please enter a subject and email body before proceeding")
def step_4():
    st.title("Step 4: Attach Files and Schedule 📎")
    uploaded_files = st.file_uploader(
        "Attach Files",
        accept_multiple_files=True,
        help="You can upload multiple files"
    )

    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.attachments:
                st.session_state.attachments.append(file.name)
                with open(file.name, "wb") as f:
                    f.write(file.getvalue())

    if st.session_state.attachments:
        st.write("Current Attachments:")
        for attachment in st.session_state.attachments:
            st.write(attachment)
            if st.button(f"Remove {attachment}"):
                st.session_state.attachments.remove(attachment)
                os.remove(attachment)

    schedule_date = st.date_input("Schedule Date")
    schedule_time = st.time_input("Schedule Time", value=None)

    if st.button("Create Draft"):
            body = st.session_state.email_body
            to_emails = st.session_state.get("to_emails", [])

            # Convert string to list if necessary
            if isinstance(to_emails, str):
                to_emails = [to_emails.strip()]

            from_email = "amarc8399@gmail.com"

            if not to_emails or to_emails == [""]:
                st.error("Please select at least one recipient")
                st.stop()

            if not st.session_state.subject:
                st.error("Please enter an email subject")
                st.stop()

            if not body:
                st.error("Please enter an email body")
                st.stop()

            st.write("Debugging: to_emails ->", to_emails)  # Debugging output

            try:
                drafts = []
                for email in to_emails:
                    draft = create_draft_with_attachments(
                        from_email,
                        [email],  # Pass a single email as a list
                        st.session_state.subject,
                        st.session_state.email_body,
                        st.session_state.attachments
                    )
                    if draft:
                        drafts.append(draft)
                
                if drafts:
                    st.success("Drafts created successfully!")
                    st.session_state.attachments = []

                    service = authenticate_google_calendar()
                    start_time = datetime.combine(schedule_date, schedule_time)
                    end_time = start_time + timedelta(minutes=30)
                    event = create_calendar_event(service, st.session_state.subject, start_time, end_time)
                    st.success(f"Email scheduled successfully! Event ID: {event['id']}")
                else:
                    st.error("Failed to create drafts")
            except Exception as e:
                st.error(f"An error occurred: {e}")


    if st.button("Previous"):
        st.session_state.step -= 1

def main():
    # st.title("Gmail Draft Automation with Scheduler")
    # st.title("MailMagic AI ✨")
    # Sidebar Content
    # st.sidebar.title("MailMagic AI ✨",)

    # Custom CSS for sidebar title with hover effect

    # Custom CSS for styling with hover effects
    st.markdown(
        """
        <style>
        .main-title, .sidebar-title {
            font-size: 32px; /* Bigger size for main title */
            font-weight: bold;
            color: #FDCB58; /* Default color */
            text-align: center;
            margin-bottom: 20px;
            transition: color 0.3s ease-in-out, transform 0.2s;
        }
        .main-title:hover, .sidebar-title:hover {
            color: #FF9F1C; /* Hover color */
            transform: scale(1.1); /* Slight zoom effect */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display main title with custom class
    st.markdown('<div class="main-title">MailMagic AI ✨</div>', unsafe_allow_html=True)

    # Display sidebar title with custom class
    st.sidebar.markdown('<div class="sidebar-title">MailMagic AI ✨</div>', unsafe_allow_html=True)

    # st.sidebar.write("""
    # MailMagic AI makes emailing effortless! 🚀 Draft smart, personalized emails and schedule them to unlimited recipients with a single click. Let AI handle the writing while you focus on what truly matters! 💡 
                      
    # - **Step 1** : Upload Resume
    # - **Step 2** : Select Recipients
    # - **Step 3** : Compose Email
    # - **Step 4** : Attach Files and Schedule
    # Explore the features and request a demo today!  
    # """)


    # Custom CSS for floating animation
    # Custom CSS for floating animation + red hover effect
    st.markdown(
        """
        <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-5px); } /* Move up */
            100% { transform: translateY(0px); } /* Back to normal */
        }

        .floating-step {
            display: block;
            font-size: 16px;
            font-weight: bold;
            margin: 8px 0;
            padding: 5px;
            border-radius: 5px;
            transition: color 0.3s ease, background-color 0.3s ease;
            animation: float 2s ease-in-out infinite;
        }

        /* Hover effect: Text turns white, background turns red */
        .floating-step:hover {
            color: white;
            background-color: red;
            cursor: pointer;
        }

        /* Delays for smooth staggered animation */
        .step1 { animation-delay: 0s; }
        .step2 { animation-delay: 0.2s; }
        .step3 { animation-delay: 0.4s; }
        .step4 { animation-delay: 0.6s; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar content with animated steps and emojis
    st.sidebar.markdown(
    """
    <i>
    <b>MailMagic AI</b> makes emailing effortless! 🚀 Draft smart, personalized emails and schedule them to unlimited recipients with a single click.  
    Let AI handle the writing while you focus on what truly matters! 💡 
    </i>
    """,
    unsafe_allow_html=True
)


    st.sidebar.markdown('<div class="floating-step step1"><i>Step 1: Upload Resume 📄</i></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="floating-step step2"><i>Step 2: Select Recipients 📧</i></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="floating-step step3"><i>Step 3: Compose Email ✍️</i></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="floating-step step4"><i>Step 4: Attach Files & Schedule 📎</i></div>', unsafe_allow_html=True)



    st.sidebar.markdown("<i>Explore the features and request a demo today!</i>",unsafe_allow_html=True)


    if st.session_state.step == 1:
        step_1()
    elif st.session_state.step == 2:
        step_2()
    elif st.session_state.step == 3:
        step_3()
    elif st.session_state.step == 4:
        step_4()

if __name__ == "__main__":
    main()
