import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

APP_DIR = Path(__file__).parent
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="NextAI", version="2.0.0")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok", "app": "NextAI", "version": "2.0.0"}

@app.get("/", response_class=HTMLResponse)
def home():
    return (APP_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.post("/api/chat")
def chat(req: ChatRequest):
    if not API_KEY:
        raise HTTPException(status_code=503, detail="مفتاح Gemini غير مضبوط. أضفه في Environment Variables باسم GEMINI_API_KEY.")
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="اكتب رسالة أولاً.")
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "أنت NextAI، مساعد ذكي يتحدث باللهجة المصرية عند مخاطبة المستخدم بالعربية. "
                "كن عملياً ومختصراً، ولا تدّع تنفيذ أي إجراء لم تنفذه فعلاً.\n\n"
                f"رسالة المستخدم: {message}"
            ),
        )
        return {"reply": response.text or "لم يصل رد نصي من النموذج."}
    except Exception as exc:
        # Keep secrets and raw provider errors out of the browser.
        print(f"Provider error: {type(exc).__name__}: {exc}")
        raise HTTPException(status_code=502, detail="حصل خطأ أثناء الاتصال بالنموذج. راجع سجلات الخدمة في Render.")
