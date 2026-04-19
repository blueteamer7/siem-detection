import os
import requests
import zipfile
import io
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = os.environ.get('QRADAR_HOST')
QRADAR_TOKEN = os.environ.get('QRADAR_SEC_TOKEN')

HEADERS = {
    'SEC': QRADAR_TOKEN,
    'Accept': 'application/json',
    'Version': '17.0'
}

def create_extension_zip():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        rule_folder = 'detections/qradar/'
        files = [f for f in os.listdir(rule_folder) if f.endswith('.json')]
        
        if not files: return None
            
        # 🎫 ƏN RƏSMİ MANİFEST FORMATI
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<extension name="ZakhraSOCRules" version="1.0">\n'
        xml_content += '    <description>SOC Detection Rules</description>\n'
        xml_content += '</extension>'
        
        # Məcburi: extension.xml mütləq ZIP-in kökündə olmalıdır
        zip_file.writestr('extension.xml', xml_content)
        
        for file_name in files:
            file_path = os.path.join(rule_folder, file_name)
            zip_file.write(file_path, arcname=file_name)
            
    return zip_buffer.getvalue()

def upload_to_qradar():
    zip_data = create_extension_zip()
    if not zip_data: return

    url = f"https://{QRADAR_HOST}/api/config/extension_management/extensions"
    files = {'file': ('ZakhraSOC.zip', zip_data, 'application/zip')}
    
    # timeout əlavə edirik ki, asılıb qalmasın
    response = requests.post(url, headers=HEADERS, files=files, verify=False, timeout=30)

    if response.status_code in [200, 201, 202]:
        print("✅ NƏHAYƏT! QRadar paketi qəbul etdi.")
    else:
        print(f"❌ Xəta: {response.status_code} - {response.text}")

if __name__ == "__main__":
    upload_to_qradar()
