import os
from twilio.rest import Client

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

NEXFIELD_NUMBER = os.getenv("NEXFIELD_NUMBER")

# ТЕСТОВЫЙ НОМЕР (можешь поменять)
lead_phone = "+19165716526"

print("START TEST CALL")

try:
    call = client.calls.create(
        to=NEXFIELD_NUMBER,
        from_=lead_phone,
        twiml="""
        <Response>
            <Say>This is a test call. Check caller ID.</Say>
        </Response>
        """
    )

    print("CALL SENT")
    print("CALL SID:", call.sid)
    print("SENT FROM:", lead_phone)

except Exception as e:
    print("ERROR:")
    print(e)
