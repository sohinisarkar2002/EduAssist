import httpx, os
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"
async def send_email_async(to: str, subject: str, html: str):
    payload = {
        "personalizations":[{"to":[{"email":to}],"subject":subject}],
        "from":{"email":EMAIL_SENDER},
        "content":[{"type":"text/html","value":html}]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(SENDGRID_URL, json=payload, headers={"Authorization": f"Bearer {SENDGRID_API_KEY}"})
        return resp.status_code
