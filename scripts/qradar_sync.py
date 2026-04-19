import os
import requests
import zipfile
import io
import urllib3

# SSL xəbərdarlıqlarını söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = os.environ.get('QRADAR_HOST')
QRADAR_TOKEN = os.environ.get('QRADAR_SEC_TOKEN')

HEADERS = {
    'SEC': QRADAR_TOKEN,
    'Accept': 'application/json',
    'Version': '17.0'
}

def create_extension_zip():
    """Bütün JSON qaydalarını bir ZIP paketində toplayır"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        rule_folder = 'detections/qradar/'
        files = [f for f in os.listdir(rule_folder) if f.endswith('.json')]
        
        if not files:
            print("❌ Heç bir JSON faylı tapılmadı!")
            return None
            
        for file_name in files:
            file_path = os.path.join(rule_folder, file_name)
            zip_file.write(file_path, arcname=file_name)
            print(f"📦 Paketə əlavə edildi: {file_name}")
            
    return zip_buffer.getvalue()

def upload_to_qradar():
    zip_data = create_extension_zip()
    if not zip_data: return

    # QRadar Extension Management Endpoint
    url = f"https://{QRADAR_HOST}/api/config/extension_management/extensions"
    
    print(f"🚀 Paket QRadar-a göndərilir: {url}")
    
    files = {'file': ('rules_pack.zip', zip_data, 'application/zip')}
    
    response = requests.post(url, headers=HEADERS, files=files, verify=False)

    if response.status_code in [200, 201, 202]:
        print("✅ UĞURLU! Qaydalar Extension kimi yükləndi.")
        print("💡 İndi QRadar panelində 'Admin -> Extension Management' hissəsinə bax.")
    else:
        print(f"❌ Xəta: {response.status_code}")
        print(f"Mesaj: {response.text}")

if __name__ == "__main__":
    upload_to_qradar()
