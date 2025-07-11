import os
import smtplib
import ssl
from email.message import EmailMessage

import pool


sender_email = "buzztroll@gmail.com"
app_password = os.getenv('SHIRK_POOL_EMAIL_PW')
receiver_email = "buzztroll@gmail.com, cindyconnelly@hotmail.com, wrshirk@yahoo.com, justinconnelly@hotmail.com"
receiver_email = "buzztroll@gmail.com"

image_path = "temperature_plot.png"
temperature = pool.get_pool_temp(reading_count=1)

msg = EmailMessage()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Shirk Pool Daily Temperature"

msg.set_content(f"The current temperature is {temperature:.1f} °F.\nAttached is the image.")

# Attach the image
with open(image_path, "rb") as f:
    img_data = f.read()
    msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename="temperature_plot.png")

# ==== Send the email ====
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)

print("Email sent!")
