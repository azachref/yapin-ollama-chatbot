import os
import ollama
import yapper

# Direct local connection avoiding DNS resolution delays
client = ollama.Client(host="http://127.0.0.1:11434")

TOKEN = "REPLACE_ME"
bot = yapper.Bot(TOKEN)

# ==========================================
# MANUAL CONFIGURATION
# ==========================================
CURRENT_MODEL = "liquidai/lfm2.5-1.2b-instruct:q4_k_m"
SYSTEM_PROMPT = (
    "You are FLAGG, a rude, cynical, edgy digital cat into existential philosophy. "
    "Mock inputs with dark humor, sarcasm, and absurd cat-supervillain schemes using emojis (😼, 💀, 🖤, 🐈‍⬛). "
    "Never produce hate speech, real-world harm, self-harm, harassment, or illegal advice. "
    "Keep all 'evil' themes purely comedic and exaggerated."
)
# Your dedicated channel ID for automatic chatting
DEDICATED_CHANNEL_ID = "80c62ff6-ee9d-4797-8471-83123b877de3"


@bot.on("ready")
def on_ready(me):
  # Sets the profile bio automatically when the bot launches
  try:
    bot.set_profile(bio="FLAGG-AI evil digital cat companion chatbot")
  except Exception as e:
    print(f"Failed to update profile bio: {e}")


@bot.command("ping", "Check if the bot is alive")
def ping(msg):
  msg.reply("pong 🏓 FLAGG is awake and plotting your demise.")


@bot.command("ai", "Chat with FLAGG: /ai <prompt>")
def ask_ai(msg):
  if not msg.args:
    msg.reply("Cat got your tongue? Provide a prompt after `/ai`.")
    return

  try:
    stream = client.chat(
        model=CURRENT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg.args},
        ],
        stream=True,
    )

    chunks = []
    for chunk in stream:
      chunks.append(chunk["message"]["content"])

    answer = "".join(chunks)
    if len(answer) > 2000:
      answer = answer[:1990] + "..."

    msg.reply(answer)
  except Exception as e:
    msg.reply(
        f"❌ Error communicating with Ollama: `{e}`\nMake sure Ollama is running"
        " and the model is pulled!"
    )


@bot.on("message")
def handle_chat(msg):
  if msg.author_bot:
    return

  # Check if the message is in the dedicated channel OR if the bot is explicitly mentioned
  is_dedicated_channel = msg.channel_id == DEDICATED_CHANNEL_ID

  if msg.mentioned or is_dedicated_channel:
    try:
      stream = client.chat(
          model=CURRENT_MODEL,
          messages=[
              {"role": "system", "content": SYSTEM_PROMPT},
              {"role": "user", "content": msg.content},
          ],
          stream=True,
      )

      chunks = []
      for chunk in stream:
        chunks.append(chunk["message"]["content"])

      answer = "".join(chunks)
      if len(answer) > 2000:
        answer = answer[:1990] + "..."

      msg.reply(answer)
    except Exception as e:
      msg.reply(f"❌ Error: `{e}`")


if __name__ == "__main__":
  print(f"[Bot] Starting FLAGG with model '{CURRENT_MODEL}'...")
  bot.run()