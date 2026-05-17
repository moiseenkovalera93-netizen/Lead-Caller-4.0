

accomplished-reverence

production



Agent


Lead-Caller-4.0
Deployments
Variables
Metrics
Settings
Unexposed service
3.13.13python@3.13.13
US West
1 Replica

HISTORY
Hide Skipped
Lead-Caller-4.0
/
4d8dcb0f
Crashed

May 17, 2026 at 12:54 AM PDT
Get Help
Details
Build Logs
Deploy Logs
Network Flow Logs
Filter and search logs

You reached the start of the range
May 17, 2026 at 12:54 AM
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
Starting Container
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
  File "/app/main.py", line 18
    3.13.13python@3.13.13
          ^
SyntaxError: invalid decimal literal
You reached the end of the range
May 17, 2026 at 12:54 AM


500May 17, 2026 at 12:51 AM
Starting Container
Worker started
Bot started
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getMe "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/deleteWebhook "HTTP/1.1 200 OK"
INFO:telegram.ext.Application:Application started
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<19 lines>...
ERROR:telegram.ext.Application:No error handlers are registered, logging exception.
    )
Traceback (most recent call last):
    ^
  File "/app/.venv/lib/python3.13/site-packages/telegram/ext/_application.py", line 1335, in process_update
    await coroutine
  File "/app/.venv/lib/python3.13/site-packages/telegram/ext/_handlers/basehandler.py", line 158, in handle_update
  File "/app/.venv/lib/python3.13/site-packages/telegram/ext/_extbot.py", line 2909, in send_message
    return await self.callback(update, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/telegram/_message.py", line 1762, in reply_text
    return await super().send_message(
  File "/app/main.py", line 111, in handle_message
    await update.message.reply_text(f"Queued: {phone}")
    return await self.get_bot().send_message(
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getUpdates "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/sendMessage "HTTP/1.1 400 Bad Request"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
  File "/app/.venv/lib/python3.13/site-packages/telegram/ext/_extbot.py", line 355, in _do_post
    ^
  File "/app/.venv/lib/python3.13/site-packages/telegram/ext/_extbot.py", line 610, in _send_message
    result = await super()._send_message(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<20 lines>...
    )
    ^
    ...<20 lines>...
  File "/app/.venv/lib/python3.13/site-packages/telegram/_bot.py", line 745, in _send_message
    )
    result = await self._post(
    ^
             ^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.13/site-packages/telegram/_bot.py", line 1029, in send_message
    ...<7 lines>...
    return await self._send_message(
    )
           ^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<18 lines>...
    ^
  File "/app/.venv/lib/python3.13/site-packages/telegram/_bot.py", line 623, in _post
    return await self._do_post(
           ^^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
    )
    ^
    return await super()._do_post(
           ^^^^^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
    )
    ^
  File "/app/.venv/lib/python3.13/site-packages/telegram/_bot.py", line 652, in _do_post
    result = await request.post(
             ^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
    )
    ^
  File "/app/.venv/lib/python3.13/site-packages/telegram/request/_baserequest.py", line 201, in post
    result = await self._request_wrapper(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<7 lines>...
    )
    ^
  File "/app/.venv/lib/python3.13/site-packages/telegram/request/_baserequest.py", line 382, in _request_wrapper
    raise BadRequest(message)
telegram.error.BadRequest: Message to be replied not found
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getUpdates "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getUpdates "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getUpdates "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getUpdates "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8900911631:AAEQy1sEyLTrMW8g27tIit3-SW2-_ANkLbg/getUpdates "HTTP/1.1 200 OK"


500
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")
NEXFIELD_NUMBER = os.getenv("NEXFIELD_NUMBER")

CALL_DELAY = 120
MAX_ATTEMPTS = 3


# =========================
# PHONE PARSER
# =========================
def extract_phone(text: str):
    match = re.search(r'(\+1[\s\-]?\d{10}|\b\d{10}\b)', text)
    if not match:
        return None

    digits = re.sub(r'[^\d]', '', match.group())

    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"

    return None


# =========================
# LEADS
# =========================
def get_lead(key):
    data = r.get(key)
    return json.loads(data) if data else None


def save_lead(key, lead):
    r.set(key, json.dumps(lead))


# =========================
# TELEGRAM HANDLER
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    phone = extract_phone(text)

    if not phone:
        return

    dedup_key = f"{DEDUP_PREFIX}{phone}"
    if r.get(dedup_key):
        return

    r.setex(dedup_key, 300, "1")

    lead_key = f"{LEAD_PREFIX}{phone}"

    lead = get_lead(lead_key)
    if not lead:
        lead = {
            "phone": phone,
            "status": "NEW",
            "attempts": 0,
            "created_at": time.time(),
            "last_error": None
        }

    lead["status"] = "QUEUED"
    save_lead(lead_key, lead)

    r.rpush(QUEUE_KEY, json.dumps({
        "phone": phone,
        "lead_key": lead_key
    }))

    await update.message.reply_text(f"Queued: {phone}")


# =========================
# CALL PROCESS
# =========================
def process_call(task):
    phone = task["phone"]
    lead_key = task["lead_key"]

    lead = get_lead(lead_key)
    if not lead:
        return

    try:
        lead["status"] = "CALLING"
        save_lead(lead_key, lead)

        time.sleep(CALL_DELAY)

        twilio.calls.create(
            to=phone,
            from_=TWILIO_FROM,
            twiml=f"<Response><Say>Please hold</Say><Dial>{NEXFIELD_NUMBER}</Dial></Response>"
        )

        lead["status"] = "CALLED"
        lead["attempts"] += 1
        lead["last_error"] = None
        save_lead(lead_key, lead)

        logging.info(f"CALLED {phone}")

    except Exception as e:
        lead["attempts"] += 1
        lead["last_error"] = str(e)

        if lead["attempts"] >= MAX_ATTEMPTS:
            lead["status"] = "FAILED"
        else:
            lead["status"] = "RETRYING"
            time.sleep(5)
            r.rpush(QUEUE_KEY, json.dumps(task))

        save_lead(lead_key, lead)
        logging.error(f"ERROR {phone}: {e}")


# =========================
# WORKER THREAD
# =========================
def worker_loop():
    print("Worker started")

    while True:
        try:
            _, data = r.blpop(QUEUE_KEY)
            task = json.loads(data)
            process_call(task)
        except Exception as e:
            logging.error(f"Worker error: {e}")
            time.sleep(2)


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    threading.Thread(target=worker_loop, daemon=True).start()

    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started")

    app.run_polling()
