import os, socket, threading, asyncio, requests
from flask import Flask, request, jsonify, render_template_string
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
app = Flask(__name__)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
def CODEX_BRAIN(text, user_name="User"):
    l=text.lower()
    if "domain" in l:
        n="".join(c for c in l.split()[-1] if c.isalnum())[:15] or "codex"
        res=""
        for tld in [".com",".ai",".io",".pk"]:
            d=f"{n}{tld}"
            try: socket.gethostbyname(d); res+=f"❌ {d} Booked\n"
            except: res+=f"✅ {d} AVAILABLE\n"
        return res
    return f"CODEX Ready ✅\nLikho: domain check codexstore"
HTML='<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-black text-white p-4"><h1>CODEX_OMNI LIVE</h1><div id="chat" class="bg-zinc-900 p-3 rounded mt-3 h-96 overflow-y-auto"></div><div class="flex gap-2 mt-3"><input id="m" class="flex-1 p-3 rounded bg-zinc-800"><button onclick="send()" class="bg-blue-600 px-6 rounded">Send</button></div><script>async function send(){let v=m.value;chat.innerHTML+=`You: ${v}<br>`;m.value="";let r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:v})});let d=await r.json();chat.innerHTML+=`Bot: ${d.reply}<br>`}</script></body></html>'
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/api/chat', methods=['POST'])
def api(): return jsonify({"reply": CODEX_BRAIN(request.json.get('message',''))})
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CODEX_BRAIN(update.message.text))
def run_tele():
    if not TOKEN: return
    loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop)
    a=ApplicationBuilder().token(TOKEN).build()
    a.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    loop.run_until_complete(a.run_polling())
if __name__=='__main__':
    threading.Thread(target=run_tele, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",8080)))
