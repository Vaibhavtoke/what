import streamlit as st
import pywhatkit
import time
import pyautogui
import os
from datetime import datetime

# Function to send WhatsApp messages
def send_whatsapp_message(phone_no, message, wait_time=20):
    try:
        st.write(f"Sending message to {phone_no}...")
        pywhatkit.sendwhatmsg_instantly(phone_no=phone_no, message=message, wait_time=wait_time)
        time.sleep(15)  # Wait to ensure the message is sent
        pyautogui.hotkey('ctrl', 'w')  # Close the tab
        pyautogui.press('enter')  # Confirm closing
        pyautogui.hotkey('ctrl', 'r')  # Refresh
        st.success(f"Message sent to {phone_no}")
    except Exception as e:
        st.error(f"Error sending message to {phone_no}: {e}")

# Fix for headless environments (Xvfb)
if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':1')

# Sidebar with logo and title
st.sidebar.image('company_logo.png', use_column_width=True)
st.sidebar.markdown("<marquee> Automate WhatsApp Messenger </marquee>", unsafe_allow_html=True)

# Web app title
st.markdown(
    "<div style='background-color:#000000;padding:12px'><h1 style='color:white;text-align:center;'>WhatsApp Web App</h1></div>",
    unsafe_allow_html=True
)

# Main function
def main():
    col1, col2 = st.columns(2)

    # Phone numbers input
    to_phones = col1.text_area(
        'Enter phone numbers (comma-separated)',
        help='Enter multiple phone numbers separated by commas',
        placeholder='+919876543210, +918765432109'
    )

    # Repeat message count
    repeat_msg_count = col2.number_input(
        'How many times to repeat the message?', 
        min_value=1, 
        step=1
    )

    # Message input
    text_msg = st.text_area(
        'Enter message to send', 
        value="We’re excited to invite you to our upcoming AI Club Event!",
        placeholder='Enter message to send'
    )

    # Tabs for sending messages
    tab1, tab2 = st.tabs(['Send Now', 'Schedule to Send Later'])

    # Immediate sending
    with tab1:
        if st.checkbox('Send Message'):
            text_msg_all = '\n'.join([text_msg] * repeat_msg_count)
            phone_numbers = [num.strip() for num in to_phones.split(',') if num.strip()]
            for phone_no in phone_numbers:
                send_whatsapp_message(phone_no, text_msg_all)

    # Scheduled message sending
    with tab2:
        col1, col2 = st.columns(2)
        send_date = col1.date_input("Select the date to send messages")
        send_time = col2.time_input("Select the time to send messages")

        if col1.checkbox('Send Scheduled Messages'):
            text_msg_all = '\n'.join([text_msg] * repeat_msg_count)
            phone_numbers = [num.strip() for num in to_phones.split(',') if num.strip()]

            target_datetime = datetime.combine(send_date, send_time)
            current_time = datetime.now()

            if target_datetime <= current_time:
                st.error("Selected date and time must be in the future!")
            else:
                time_diff = (target_datetime - current_time).total_seconds()
                st.write(f"Scheduled to send on {send_date} at {send_time}. Waiting for {time_diff:.2f} seconds.")
                time.sleep(time_diff)
                for phone_no in phone_numbers:
                    send_whatsapp_message(phone_no, text_msg_all)

# Run the app
if __name__ == '__main__':
    main()

