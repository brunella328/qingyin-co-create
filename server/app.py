#!/usr/bin/env python3
"""
LINE OA Webhook + Waitlist Server for 青銀共創
Railway-ready version
"""
import os, csv, json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, Response

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "ce101f5d1f1a86a45fcb18890fdfc9f3")
LINE_CHANNEL_TOKEN  = os.environ.get("LINE_CHANNEL_TOKEN", "")
FORM_URL = os.environ.get("FORM_URL", "https://your-app.railway.app/form")
PDF_URL  = os.environ.get("PDF_URL", "https://drive.google.com/PLACEHOLDER")
WAITLIST_CSV = os.environ.get("WAITLIST_CSV", "/data/waitlist_signups.csv")
os.makedirs(os.path.dirname(WAITLIST_CSV), exist_ok=True)

WELCOME_MSG = f"""歡迎加入青銀共創！🎉

您已獲得《新鮮人職場生存大禮包》試閱版！

📥 向上管理話術表（試閱版 PDF）
→ {PDF_URL}

📌 完整版 Early Bird 搶先登記 NT$149（原價 NT$399）
→ {FORM_URL}"""

ABOUT_MSG = "青銀共創連結壯世代高管與職場新鮮人，透過 30 年實戰智慧傳承幫助你縮短職場摸索期。\n\n有任何問題，直接傳訊息給我們！"

FORM_HTML = """<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>青銀共創｜Early Bird 搶先登記</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,'PingFang TC',sans-serif;background:#f5f7fa;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:white;border-radius:16px;max-width:520px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.10);overflow:hidden}
.header{background:#1B3A6B;padding:32px 28px 24px;text-align:center}
.header .brand{color:#F5A623;font-size:13px;font-weight:600;letter-spacing:2px;margin-bottom:8px}
.header h1{color:white;font-size:22px;font-weight:700;line-height:1.4}
.badge{display:inline-block;background:#F5A623;color:#1B3A6B;font-weight:700;font-size:13px;border-radius:20px;padding:4px 14px;margin-top:12px}
.body{padding:28px}
.price-box{background:#EEF2F8;border-radius:10px;padding:14px 18px;margin-bottom:22px;display:flex;align-items:center;gap:12px}
.price-now{font-size:28px;font-weight:800;color:#1B3A6B}
.price-orig{font-size:13px;color:#999;text-decoration:line-through}
.features{margin-bottom:24px}
.feature{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid #f0f0f0;font-size:14px;color:#333}
.feature:last-child{border-bottom:none}
.check{color:#38A169;font-weight:700;flex-shrink:0}
form{display:flex;flex-direction:column;gap:14px}
label{font-size:13px;font-weight:600;color:#444;margin-bottom:4px;display:block}
input,select{width:100%;padding:11px 14px;border:1.5px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit;outline:none}
input:focus,select:focus{border-color:#1B3A6B}
.submit-btn{background:#F5A623;color:#1B3A6B;font-weight:800;font-size:17px;border:none;border-radius:10px;padding:15px;cursor:pointer}
.footer-note{font-size:12px;color:#999;text-align:center;margin-top:10px}
.success-box{display:none;text-align:center;padding:20px 0}
.success-box .icon{font-size:52px;margin-bottom:12px}
.success-box h2{color:#1B3A6B;font-size:20px;margin-bottom:8px}
.success-box p{color:#666;font-size:14px;line-height:1.6}
</style></head>
<body><div class="card">
<div class="header">
  <div class="brand">青 銀 共 創</div>
  <h1>新鮮人職場生存大禮包<br>搶先登記</h1>
  <div class="badge">Early Bird 特惠</div>
</div>
<div class="body">
  <div class="price-box">
    <div><div class="price-now">NT$149</div><div class="price-orig">原價 NT$399</div></div>
    <div style="font-size:12px;color:#666">登記後享 Early Bird 特惠<br>正式開賣前 48 小時 Email 通知</div>
  </div>
  <div class="features">
    <div class="feature"><span class="check">✓</span>非公開升遷指標（高管評分真實標準）</div>
    <div class="feature"><span class="check">✓</span>向上管理話術表（15 個情境標準話術）</div>
    <div class="feature"><span class="check">✓</span>高管視角面試指南（破解面試邏輯）</div>
  </div>
  <form id="f">
    <div><label>姓名 *</label><input name="name" placeholder="你的名字" required></div>
    <div><label>Email *</label><input type="email" name="email" placeholder="your@email.com" required></div>
    <div><label>目前職場狀態 *</label>
      <select name="status" required><option value="">請選擇</option>
        <option>求職中</option><option>入職0-1年</option><option>入職1-3年</option><option>其他</option>
      </select></div>
    <div><label>最大職場困擾（選填）</label>
      <select name="pain"><option value="">請選擇</option>
        <option>不知道怎麼和主管溝通</option><option>擔心試用期表現不達標</option>
        <option>不懂職場升遷邏輯</option><option>跨部門協作卡關</option>
      </select></div>
    <button type="submit" class="submit-btn">立即搶先登記 →</button>
    <div class="footer-note">填寫即代表同意接收開賣通知，不會發送垃圾郵件</div>
  </form>
  <div class="success-box" id="s">
    <div class="icon">🎉</div>
    <h2>登記成功！</h2>
    <p>感謝你的支持！你已獲得 Early Bird 資格（NT$149）。<br><br>我們將在正式開賣前 48 小時以 Email 通知你。<br><br>— 青銀共創團隊</p>
  </div>
</div></div>
<script>
document.getElementById('f').addEventListener('submit',async function(e){
  e.preventDefault();
  const btn=this.querySelector('.submit-btn');
  btn.textContent='送出中...';btn.disabled=true;
  const fd=new FormData(this);
  const data={};fd.forEach((v,k)=>data[k]=v);
  try{
    const r=await fetch('/waitlist',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});
    if(r.ok){document.getElementById('f').style.display='none';document.getElementById('s').style.display='block';}
    else{btn.textContent='送出失敗，請重試';btn.disabled=false;}
  }catch{btn.textContent='網路錯誤，請重試';btn.disabled=false;}
});
</script></body></html>"""

app = Flask(__name__)

def line_reply(reply_token, text):
    import urllib.request
    data = json.dumps({"replyToken": reply_token, "messages": [{"type":"text","text":text}]}).encode()
    req = urllib.request.Request("https://api.line.me/v2/bot/message/reply", data=data,
        headers={"Content-Type":"application/json","Authorization":f"Bearer {LINE_CHANNEL_TOKEN}"})
    try: urllib.request.urlopen(req, timeout=5)
    except Exception as e: app.logger.error(f"Reply: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json(silent=True) or {}
    for event in body.get("events", []):
        rt = event.get("replyToken","")
        if event.get("type") == "follow":
            line_reply(rt, WELCOME_MSG)
        elif event.get("type") == "message":
            text = event.get("message",{}).get("text","").strip()
            if "領取大禮包" in text or "大禮包" in text:
                line_reply(rt, f"【職場大禮包 PDF 試閱版】\n\n立即下載：\n{PDF_URL}\n\n完整版 Early Bird 登記：\n{FORM_URL}")
            elif "關於我們" in text or "關於" in text:
                line_reply(rt, ABOUT_MSG)
            elif "登記" in text or "預約" in text:
                line_reply(rt, f"【Early Bird 搶先登記】\n\nNT$149 特惠（正式上線 NT$399）\n\n立即登記：\n{FORM_URL}")
    return "OK", 200

@app.route("/form")
def form():
    return Response(FORM_HTML, mimetype="text/html")

@app.route("/waitlist", methods=["POST","OPTIONS"])
def waitlist():
    if request.method == "OPTIONS":
        r = app.make_default_options_response()
        r.headers.update({"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"Content-Type","Access-Control-Allow-Methods":"POST"})
        return r
    data = request.get_json(silent=True) or {}
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_header = not os.path.exists(WAITLIST_CSV)
    with open(WAITLIST_CSV,"a",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header: w.writerow(["timestamp","name","email","status","pain"])
        w.writerow([ts, data.get("name",""), data.get("email",""), data.get("status",""), data.get("pain","")])
    r = jsonify({"ok":True})
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route("/health")
def health():
    count = 0
    if os.path.exists(WAITLIST_CSV):
        with open(WAITLIST_CSV) as f: count = sum(1 for _ in f) - 1
    return jsonify({"status":"ok","oa":"@666duqqu","waitlist_count":max(0,count)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=False)
