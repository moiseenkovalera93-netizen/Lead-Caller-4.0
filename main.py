import re
import json
import time
import os
import logging
import threading
import redis

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from twilio.rest import Client

# =========================
# LOGGING
# =========================
logging.basicConfig(level=logging.INFO)

# =========================
# REDIS
# =========================
r = redis.Redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)

QUEUE_KEY = "queue:calls"
DEDUP_PREFIX = "dedup:"
LEAD_PREFIX = "lead:"

# =========================
# TWILIO
# =========================
twilio = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")
NEXFIELD_NUMBER = os.getenv("NEXFIELD_NUMBER")

CALL_DELAY = 120
MAX_ATTEMPTS = 3


# =========================
# PHONE PARSER (MASTER FIX)
# =========================
def extract_phone(text: str):
    match = re.search(r'(\+1[\s\-]?\d{10}|\b\d{10}\b)', text)
    if not match:
        return None

    digits = re.sub(r"[^\d]", "", match.group())

    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"

    return None


# =========================
# LEAD STORAGE
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

    lead_phone = extract_phone(text)

    if not lead_phone:
        return

    # dedup
    dedup_key = f"{DEDUP_PREFIX}{lead_phone}"
    if r.get(dedup_key):
        return

    r.setex(dedup_key, 300, "1")

    lead_key = f"{LEAD_PREFIX}{lead_phone}"

    lead = get_lead(lead_key)
    if not lead:
        lead = {
            "lead_id": str(int(time.time())),
            "lead_phone": lead_phone,
            "status": "NEW",
            "attempts": 0,
            "created_at": time.time(),
            "last_error": None
        }

    lead["status"] = "QUEUED"
    save_lead(lead_key, lead)

    # IMPORTANT: queue only lead_phone (MASTER FIELD)
    r.rpush(QUEUE_KEY, json.dumps({
        "lead_phone": lead_phone,
        "lead_key": lead_key
    }))

    await update.message.reply_text(f"📞 Lead queued: {lead_phone}")


# =========================
# CALL PROCESSOR
# =========================
def process_call(task):
    lead_phone = task["lead_phone"]
    lead_key = task["lead_key"]

    lead = get_lead(lead_key)
    if not lead:
        return

    try:
        lead["status"] = "CALLING"
        save_lead(lead_key, lead)

        time.sleep(CALL_DELAY)

        # TWILIO CALL (ONLY lead_phone)
        call = twilio.calls.create(
            to=lead_phone,
            from_=TWILIO_FROM,
            twiml=f"<Response><Say>Please hold</Say><Dial>{NEXFIELD_NUMBER}</Dial></Response>"
        )

        lead["status"] = "CALLED"
        lead["attempts"] += 1
        lead["last_error"] = None
        lead["twilio_call_sid"] = call.sid

        save_lead(lead_key, lead)

        logging.info(f"CALLED {lead_phone}")

    except Exception as e:
        lead["attempts"] += 1
        lead["last_error"] = str(e)

        if lead["attempts"] >= MAX_ATTEMPTS:
            lead["status"] = "FAILED"
        else:
            lead["status"] = "RETRYING"
            r.rpush(QUEUE_KEY, json.dumps(task))

        save_lead(lead_key, lead)
        logging.error(f"ERROR {lead_phone}: {e}")


# =========================
# WORKER
# =========================
def worker_loop():
    print("Worker started")

    while True:
        _, data = r.blpop(QUEUE_KEY)
        task = json.loads(data)
        process_call(task)


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    threading.Thread(target=worker_loop, daemon=True).start()

    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started")

    app.run_polling()
CALL_DELAY = 120


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

    lead = {
        "phone": phone,
        "status": "QUEUED",
        "created_at": time.time()
    }

    save_lead(lead_key, lead)

    r.rpush(QUEUE_KEY, json.dumps({
        "phone": phone,
        "lead_key": lead_key
    }))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Queued: {phone}"
    )


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

        call = twilio.calls.create(
            to=phone,
            from_=TWILIO_FROM,
            machine_detection="Enable",   # 🔥 AMD включён
            twiml=f"""
<Response>
    <Say voice="alice">Please hold while we connect you.</Say>
    <Dial>{NEXFIELD_NUMBER}</Dial>
</Response>
"""
        )

        lead["status"] = "CALLED"
        lead["twilio_sid"] = call.sid
        save_lead(lead_key, lead)

        logging.info(f"CALL SENT {phone} SID={call.sid}")

    except Exception as e:
        lead["status"] = "FAILED"
        lead["error"] = str(e)
        save_lead(lead_key, lead)

        logging.error(f"CALL ERROR {phone}: {e}")


# =========================
# WORKER
# =========================
def worker():
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

    threading.Thread(target=worker, daemon=True).start()

    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started")

    app.run_polling()
CALL_DELAY = 120


# =========================
# PHONE
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
# LEAD STORAGE
# =========================
def save_lead(key, lead):
    r.set(key, json.dumps(lead))


def get_lead(key):
    data = r.get(key)
    return json.loads(data) if data else None


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

    lead = {
        "lead_phone": phone,
        "status": "QUEUED",
        "created_at": time.time(),
        "source": "telegram"
    }

    save_lead(lead_key, lead)

    r.rpush(QUEUE_KEY, json.dumps({
        "lead_phone": phone,
        "lead_key": lead_key
    }))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Queued lead: {phone}"
    )


# =========================
# CALL WORKER
# =========================
def process_call(task):
    lead_phone = task["lead_phone"]
    lead_key = task["lead_key"]

    lead = get_lead(lead_key)
    if not lead:
        return

    try:
        lead["status"] = "CALLING"
        save_lead(lead_key, lead)

        time.sleep(CALL_DELAY)

        # IMPORTANT: ONLY lead_phone goes to "to"
        twilio.calls.create(
            to=lead_phone,
            from_=TWILIO_FROM,
            twiml=f"<Response><Say>Please hold</Say><Dial>{NEXFIELD_NUMBER}</Dial></Response>"
        )

        lead["status"] = "CALLED"
        save_lead(lead_key, lead)

        logging.info(f"CALL OK lead={lead_phone}")

    except Exception as e:
        lead["status"] = "FAILED"
        lead["error"] = str(e)
        save_lead(lead_key, lead)

        logging.error(f"CALL ERROR lead={lead_phone} err={e}")


# =========================
# WORKER
# =========================
def worker():
    print("Worker started")

    while True:
        try:
            _, data = r.blpop(QUEUE_KEY)
            task = json.loads(data)
            process_call(task)
        except Exception as e:
            logging.error(f"Worker crash: {e}")
            time.sleep(2)


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    threading.Thread(target=worker, daemon=True).start()

    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started")

    app.run_polling()
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

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Queued: {phone}"
    )


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
# WORKER
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
