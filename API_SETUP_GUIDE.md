# Getting Your LLM API Keys

You need at least ONE of these two working; both is better (for the
fallback feature to actually be demonstrable).

## 1. Google Gemini API key (free tier available — do this first)

1. Go to **https://aistudio.google.com/app/apikey** in your browser.
2. Sign in with a Google account.
3. Click **"Create API key"**.
4. Choose "Create API key in new project" if you don't have a Google
   Cloud project yet (one is created automatically for you).
5. Copy the key that appears (starts with `AIza...`).
6. Paste it into your `.env` file as:
   ```
   GEMINI_API_KEY=AIzaSy...your_key...
   ```

**Free tier**: Gemini 1.5 Flash has a generous free tier (requests per
minute/day) that is more than enough for a demo and interview. No
credit card is required to get started at AI Studio.

**Note**: This is different from a full Google Cloud project with
billing enabled. For tonight, the AI Studio key is the fastest path.
If later you want to call Gemini through Vertex AI (with a Google
Cloud project + billing), that's a separate, more involved setup — not
needed for this project.

## 2. OpenAI API key (used as the fallback provider)

1. Go to **https://platform.openai.com/api-keys**.
2. Sign in or create an account.
3. Click **"Create new secret key"**, give it a name (e.g.
   `cloud-rag-assistant`), and copy it immediately — you can't view it
   again after closing the dialog (starts with `sk-...`).
4. Paste it into your `.env` file as:
   ```
   OPENAI_API_KEY=sk-...your_key...
   ```

**Billing note**: unlike Gemini's AI Studio free tier, OpenAI generally
requires adding a small amount of prepaid credit
(**https://platform.openai.com/settings/organization/billing**) before
API calls work, even a few dollars is enough for a demo. If you don't
want to add billing tonight, run the project with Gemini only — the
router already handles having just one provider configured.

## 3. Put both keys in `.env`

```bash
cp .env.example .env
```
Then open `.env` and fill in:
```
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-...
```
Never commit `.env` to GitHub — it's already in `.gitignore`.

## 4. Quick sanity check (optional but recommended)

Test each key works before wiring it into the full app:

```python
# test_gemini.py
import google.generativeai as genai
genai.configure(api_key="YOUR_GEMINI_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
print(model.generate_content("Say hello in one sentence.").text)
```

```python
# test_openai.py
from openai import OpenAI
client = OpenAI(api_key="YOUR_OPENAI_KEY")
r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print(r.choices[0].message.content)
```

If either prints a response, that key is working and ready to use in
the project.

## If you only get one key working tonight

That's fine — the app is designed to work with just one provider. Get
Gemini working first (it's free and faster to set up); add OpenAI
later if there's time. In the interview, you can honestly say: "I
built it with a provider abstraction so adding a second or third LLM
is a few lines of code — here's the interface," and show
`app/llm/base.py`.
