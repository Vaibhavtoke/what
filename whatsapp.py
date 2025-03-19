import pywhatkit
import streamlit as st
import time, pyautogui
from datetime import datetime

def send_whatsapp_message(phone_no, message, wait_time=20):
    pywhatkit.sendwhatmsg_instantly(phone_no=phone_no, message=message, wait_time=wait_time)
    time.sleep(15)
    pyautogui.hotkey('ctrl', 'w')
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'r')

# Sidebar with company logo and title
st.sidebar.image('company_logo.png', use_container_width=True)
st.sidebar.markdown("<marquee> Automate Whatsapp Messenger </marquee>", unsafe_allow_html=True)

# Web app title section
user_color = "#000000"
title_webapp = "Whatsapp Web App"
html_temp = f"""
<div style="background-color:{user_color};padding:12px">
<h1 style="color:white;text-align:center;">{title_webapp}

</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

def main():
    col1, col2 = st.columns(2)
    
    # Multiple phone numbers input (comma-separated)
    to_phones = col1.text_area(
        'Enter phone numbers (comma-separated)',
        help='Enter multiple phone numbers separated by commas',
        placeholder='+919876543210, +918765432109'
    )
    
    # Number of times to repeat the message
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
    
    # Tabs for immediate or scheduled sending
    tab1, tab2 = st.tabs(['Send Now', 'Schedule to send later'])
    
    # Immediate message sending
    with tab1:
        flag_open = st.checkbox('Send Message', value=False)
        if flag_open:
            text_msg_all = '\n'.join([text_msg] * repeat_msg_count)
            phone_numbers = [num.strip() for num in to_phones.split(',') if num.strip()]
            for phone_no in phone_numbers:
                send_whatsapp_message(phone_no, text_msg_all)

    # Scheduled message sending
    with tab2:
        col1, col2 = st.columns(2)
        
        send_date = col1.date_input("Select the date to send messages")
        send_time = col2.time_input("Select the time to send messages")
        
        flag_open = col1.checkbox('Send Scheduled Messages', value=False)

        if flag_open:
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

if __name__ == '__main__':
    main()
