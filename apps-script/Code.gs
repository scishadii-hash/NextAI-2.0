function doGet() {
  return HtmlService.createHtmlOutputFromFile("index")
    .setTitle("NextAI 2.0")
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}

function getReply(message) {
  message = String(message || "").trim();
  if (!message) throw new Error("اكتب رسالة الأول.");

  const key = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
  if (!key) throw new Error("أضف GEMINI_API_KEY في Project Settings ثم Script Properties.");

  const model = PropertiesService.getScriptProperties().getProperty("GEMINI_MODEL") || "gemini-2.5-flash";
  const url = "https://generativelanguage.googleapis.com/v1beta/models/" +
    encodeURIComponent(model) + ":generateContent?key=" + encodeURIComponent(key);

  const payload = {
    contents: [{
      parts: [{
        text: "أنت NextAI، مساعد ذكي يتحدث باللهجة المصرية عند مخاطبة المستخدم بالعربية. كن عملياً ومختصراً، ولا تدّع تنفيذ أي إجراء لم تنفذه فعلاً.\n\nرسالة المستخدم: " + message
      }]
    }]
  };

  const response = UrlFetchApp.fetch(url, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const status = response.getResponseCode();
  const data = JSON.parse(response.getContentText() || "{}");
  if (status < 200 || status >= 300) {
    const detail = data.error && data.error.message ? data.error.message : "تعذر الاتصال بالنموذج.";
    throw new Error(detail);
  }

  return data.candidates && data.candidates[0] &&
    data.candidates[0].content && data.candidates[0].content.parts
    ? data.candidates[0].content.parts.map(function(p) { return p.text || ""; }).join("\n").trim()
    : "لم يصل رد نصي من النموذج.";
}
