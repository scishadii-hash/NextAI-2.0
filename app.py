import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai

APP_DIR = Path(__file__).resolve().parent
INDEX_FILE = APP_DIR / "index.html"
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

app = FastAPI(title="NextAI", version="2.0.1")


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok", "app": "NextAI", "version": "2.0.1"}


@app.get("/", response_class=HTMLResponse)
def home():
    if not INDEX_FILE.is_file():
        raise HTTPException(status_code=500, detail="ملف الواجهة index.html غير موجود.")
    return INDEX_FILE.read_text(encoding="utf-8")


@app.post("/api/chat")
def chat(req: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="مفتاح Gemini غير مضبوط. أضفه في Environment Variables باسم GEMINI_API_KEY.",
        )

    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="اكتب رسالة أولاً.")

    try:
        client = genai.Client(api_key=api_key)
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
        print(f"Provider error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="حصل خطأ أثناء الاتصال بالنموذج. راجع سجلات الخدمة في Render.",
        )
