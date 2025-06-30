import smtplib
import ssl
from email.message import EmailMessage

# ==== Configuration ====
sender_email = "buzztroll@gmail.com"
app_password = "sslm qdso ghyt wncn"
receiver_email = "buzztroll@gmail.com"

image_path = "temperature_plot.png"
temperature = 72.5  # Example: read this dynamically from a sensor

# ==== Create the email ====
msg = EmailMessage()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Pool Pi Temperature Report"

msg.set_content(f"The current temperature is {temperature:.1f} °F.\nAttached is the image.")

# Attach the image
with open(image_path, "rb") as f:
    img_data = f.read()
    msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename="picture.jpg")

# ==== Send the email ====
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)

print("Email sent!")
