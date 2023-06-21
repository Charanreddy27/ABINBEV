import selenium
import html
import smtplib
import time
from selenium import webdriver
import openpyxl


def login_to_linkedin(username, password):
    """Log in to LinkedIn with the specified username and password."""
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/")
    username_input = driver.find_element_by_id("username")
    username_input.send_keys(username)
    password_input = driver.find_element_by_id("password")
    password_input.send_keys(password)
    login_button = driver.find_element_by_id("login-submit")
    login_button.click()
    return driver

def get_unread_messages_and_notifications(driver):
    """Get the number of unread messages and notifications from the LinkedIn profile."""
    unread_messages = driver.find_element_by_id("msgCount").text
    unread_notifications = driver.find_element_by_id("notifCount").text
    return unread_messages, unread_notifications

def send_email_notification(driver, recipient, unread_messages, unread_notifications):
    """Send an email notification to the specified recipient with the number of unread messages and notifications."""
    email_body = html.unescape("""
    <html>
    <head>
    <title>LinkedIn Notification</title>
    </head>
    <body>
    <h1>LinkedIn Notification</h1>
    <p>You have <b>{{ unread_messages }}</b> unread messages and <b>{{ unread_notifications }}</b> unread notifications.</p>
    <p>Here is a comparison between the current data and the previous occurrence data:</p>
    <table>
    <tr>
    <th>Data</th>
    <th>Current</th>
    <th>Previous</th>
    </tr>
    <tr>
    <td>Unread messages</td>
    <td>{{ unread_messages }}</td>
    <td>{{ previous_unread_messages }}</td>
    </tr>
    <tr>
    <td>Unread notifications</td>
    <td>{{ unread_notifications }}</td>
    <td>{{ previous_unread_notifications }}</td>
    </tr>
    </table>
    </body>
    </html>
    """).format(
        unread_messages=unread_messages,
        unread_notifications=unread_notifications,
        previous_unread_messages=unread_messages,
        previous_unread_notifications=unread_notifications,
    )
    server = smtplib.SMTP("charanbapireddy@gmail.com", 587)
    server.starttls()

    #give your email address and password
    server.login("username", "password")


    #give the email address
    server.sendmail("email", recipient, email_body)
    server.quit()

def main():
    """Main function."""

    #Give your email address and password
    driver = login_to_linkedin("username", "password")
    unread_messages, unread_notifications = get_unread_messages_and_notifications(driver)
    send_email_notification(driver, "recipient@gmail.com", unread_messages, unread_notifications)

if __name__ == "__main__":
    main()


# Create a new Excel sheet.
wb = openpyxl.Workbook()

# Create a header row with the relevant columns.
sheet = wb.active
sheet.append(['Timestamp', 'Unread messages', 'Unread notifications'])

# Fill in the columns with the data.
timestamp = time.time()
unread_messages = unread_messages
unread_notifications = unread_notifications
sheet.append([timestamp, unread_messages, unread_notifications])

# Save the Excel sheet.
wb.save('notifications.xlsx')



