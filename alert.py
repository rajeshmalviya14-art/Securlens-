from twilio.rest import Client
import os

TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_NUMBER = "+19788384566"
OWNER_NUMBER = "+919829442727"

client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_call_alert(camera_name, confidence):
    call = client.calls.create(
        twiml=f'<Response><Say voice="alice">Alert! SecurLens has detected suspicious activity on {camera_name} with {confidence} percent confidence. Please check immediately.</Say></Response>',
        to=OWNER_NUMBER,
        from_=TWILIO_NUMBER
    )
    return call.sid

def send_whatsapp_clip(camera_name, clip_url):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'SecurLens ALERT! {camera_name} pe suspicious activity detect hui! Evidence clip attached.',
        media_url=[clip_url],
        to=f'whatsapp:{OWNER_NUMBER}'
    )
    return message.sid

print("SecurLens Alert System Ready!")
