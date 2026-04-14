#!/usr/bin/env python3
"""
FREE FIRE WISHLIST MANAGER API - ALL IN ONE
Developer: Riduanul Islam
Telegram: @RiduanOfficialBD
YouTube: @riduan0
"""

import json
import requests
import time
import base64
import urllib3
import jwt
from urllib.parse import urlparse, parse_qs
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# গেম ভার্শন ফাইল থেকে ডেটা ইমপোর্ট করা হচ্ছে
from game_version import (
    CLIENT_VERSION, 
    CLIENT_VERSION_CODE, 
    UNITY_VERSION, 
    RELEASE_VERSION,
    USER_AGENT_MODEL,
    ANDROID_OS_VERSION
)

# SSL Warnings বন্ধ করা হচ্ছে
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# JSON এর কি-গুলোর সিরিয়াল বা ক্রম ঠিক রাখার জন্য কনফিগারেশন
app.config['JSON_SORT_KEYS'] = False
if hasattr(app, 'json'):
    app.json.sort_keys = False

_sym_db = _symbol_database.Default()

# --- Protobuf Descriptors ---
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MajorLoginReq_pb2', _globals)

MajorLogin = _globals['MajorLogin']
GameSecurity = _globals['GameSecurity']

DESCRIPTOR2 = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"|\n\rMajorLoginRes\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0b\n\x03key\x18\x16 \x01(\x0c\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3')

_globals2 = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR2, _globals2)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR2, 'MajorLoginRes_pb2', _globals2)

MajorLoginRes = _globals2['MajorLoginRes']

# =========================================================
# ENCRYPTION KEYS & DEFAULTS
# =========================================================
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

DEFAULT_WISHLIST_ITEMS = [
    101000001, 102000014, 101000005, 101000006, 101000011, 101000016, 101000027,
    102000021, 102000025, 102000030, 102000046, 102000055, 103000004, 103000003,
    203000001, 203000055, 203000074, 203000075, 203000076, 203000077, 203000078,
    203000150, 203000151, 203000156, 203000089, 203000084, 203000177, 203000182,
    203000202, 203000207, 203000245, 203000348, 203000349, 203000350, 203000351,
    203000352, 203000490, 1803400001, 1803400002, 1310000271, 1309000074, 1309000081,
    1309000091, 1309000083, 1309000084, 1309000101, 1309000102, 1309000103, 1309000104,
    1309000114, 1309000142, 1309000173, 1309000212, 928005203, 929005202, 929005203
]

# =========================================================
# PROTOBUF & ENCRYPTION UTILS
# =========================================================
def encode_varint(num):
    result = bytearray()
    while num > 0x7F:
        result.append((num & 0x7F) | 0x80)
        num >>= 7
    result.append(num & 0x7F)
    return bytes(result)

def make_varint_field(field_num, value):
    header = encode_varint((field_num << 3) | 0)
    data = encode_varint(value)
    return header + data

def make_bytes_field(field_num, value):
    header = encode_varint((field_num << 3) | 2)
    length = encode_varint(len(value))
    return header + length + value

def make_string_field(field_num, value):
    return make_bytes_field(field_num, value.encode())

def build_wishlist_request(item_id):
    packet = b''
    packet += make_varint_field(1, item_id)
    packet += make_bytes_field(2, b'')
    packet += make_string_field(3, "MallV2")
    return packet

def encrypt_aes(data_bytes):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data_bytes, AES.block_size))

def decrypt_response(encrypted_bytes):
    try:
        if not encrypted_bytes or len(encrypted_bytes) == 0:
            return None
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        decrypted = cipher.decrypt(encrypted_bytes)
        try:
            padding_len = decrypted[-1]
            if padding_len <= 16 and padding_len > 0:
                if all(b == padding_len for b in decrypted[-padding_len:]):
                    return decrypted[:-padding_len]
            return decrypted
        except:
            return decrypted
    except:
        return None

# =========================================================
# API LOGIC (AUTH & EAT)
# =========================================================
def get_access_token_from_eat(eat_token):
    try:
        url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
        response = requests.get(url, allow_redirects=True, timeout=30, verify=False)
        
        if 'help.garena.com' in response.url:
            parsed = urlparse(response.url)
            params = parse_qs(parsed.query)
            if 'access_token' in params:
                return params['access_token'][0]
    except Exception:
        pass
    return None

def build_major_login(open_id, access_token, platform_type):
    major = MajorLogin()
    major.event_time = "2025-03-23 12:00:00"
    major.game_name = "free fire"
    major.platform_id = 1
    major.client_version = CLIENT_VERSION
    major.system_software = f"{ANDROID_OS_VERSION} / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major.system_hardware = "Handheld"
    major.telecom_operator = "Verizon"
    major.network_type = "WIFI"
    major.screen_width = 1920
    major.screen_height = 1080
    major.screen_dpi = "280"
    major.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major.memory = 3003
    major.gpu_renderer = "Adreno (TM) 640"
    major.gpu_version = "OpenGL ES 3.1 v1.46"
    major.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major.client_ip = "223.191.51.89"
    major.language = "en"
    major.open_id = open_id
    major.open_id_type = "4"
    major.device_type = "Handheld"
    major.memory_available.version = 55
    major.memory_available.hidden_value = 81
    major.access_token = access_token
    major.platform_sdk_id = 1
    major.network_operator_a = "Verizon"
    major.network_type_a = "WIFI"
    major.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major.external_storage_total = 36235
    major.external_storage_available = 31335
    major.internal_storage_total = 2519
    major.internal_storage_available = 703
    major.game_disk_storage_available = 25010
    major.game_disk_storage_total = 26628
    major.external_sdcard_avail_storage = 32992
    major.external_sdcard_total_storage = 36235
    major.login_by = 3
    major.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major.reg_avatar = 1
    major.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major.channel_type = 3
    major.cpu_type = 2
    major.cpu_architecture = "64"
    major.client_version_code = CLIENT_VERSION_CODE
    major.graphics_api = "OpenGLES2"
    major.supported_astc_bitset = 16383
    major.login_open_id_type = 4
    major.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major.loading_time = 13564
    major.release_channel = "android"
    major.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major.android_engine_init_flag = 110009
    major.if_push = 1
    major.is_vpn = 1
    major.origin_platform_type = str(platform_type)
    major.primary_platform_type = str(platform_type)
    return major.SerializeToString()

def get_jwt_from_access_token(access_token):
    inspect_url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
    try:
        insp_resp = requests.get(inspect_url, timeout=10, verify=False)
        if insp_resp.status_code != 200:
            return None
        insp_data = insp_resp.json()
        open_id = insp_data.get('open_id')
        if not open_id:
            return None
    except:
        return None
    
    platform_types = [2, 3, 4, 6, 8]
    for pt in platform_types:
        try:
            payload = build_major_login(open_id, access_token, pt)
            encrypted_payload = encrypt_aes(payload)
            url = "https://loginbp.ggblueshark.com/MajorLogin"
            headers = {
                "User-Agent": f"Dalvik/2.1.0 (Linux; U; {ANDROID_OS_VERSION}; {USER_AGENT_MODEL} Build/PI)",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Unity-Version": UNITY_VERSION,
                "X-GA": "v1 1",
                "ReleaseVersion": RELEASE_VERSION
            }
            resp = requests.post(url, data=encrypted_payload, headers=headers, timeout=10, verify=False)
            if resp.status_code == 200:
                major_res = MajorLoginRes()
                major_res.ParseFromString(resp.content)
                if major_res.token:
                    return major_res.token
        except:
            continue
    return None

def extract_info_from_jwt(jwt_token):
    try:
        decoded = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])
        uid = decoded.get('account_id', decoded.get('uid', 'Not Found'))
        region = decoded.get('lock_region', 'Unknown')
        return str(uid), region
    except Exception:
        return 'Unknown UID', 'Unknown Region'

def add_to_wishlist_single(jwt_token, item_id):
    try:
        proto_bytes = build_wishlist_request(item_id)
        encrypted = encrypt_aes(proto_bytes)
        headers = {
            'User-Agent': f"UnityPlayer/{UNITY_VERSION} (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            'Authorization': f"Bearer {jwt_token}",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASE_VERSION,
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Unity-Version': UNITY_VERSION
        }
        url = "https://clientbp.ggblueshark.com/ChangeWishListItem"
        response = requests.post(url, data=encrypted, headers=headers, timeout=5, verify=False)
        if response.status_code == 200:
            return {'item_id': item_id, 'status': 200, 'success': True}
        else:
            return {'item_id': item_id, 'status': response.status_code, 'success': False}
    except Exception as e:
        return {'item_id': item_id, 'status': 'Error', 'success': False, 'error': str(e)[:50]}

def process_wishlist_batch(jwt_token, item_ids, max_workers=50):
    results = {'success_items': [], 'failed_items': []}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(add_to_wishlist_single, jwt_token, item_id): item_id for item_id in item_ids}
        for future in as_completed(future_to_item):
            result = future.result()
            if result.get('success'):
                results['success_items'].append(result)
            else:
                results['failed_items'].append(result)
    return results

def get_account_from_guest(uid, password):
    try:
        url = f"https://rizerxguestaccountacceee.vercel.app/rizer?uid={uid}&password={password}"
        response = requests.get(url, timeout=15, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and data.get('jwt_token'):
                return data
        return None
    except:
        return None

# =========================================================
# FLASK ROUTES
# =========================================================

@app.route('/', methods=['GET'])
def root_route():
    return jsonify({
        "Developer": "Riduanul Islam",
        "TelegramBot": "https://t.me/RiduanFFBot",
        "TelegramChannel": "https://t.me/RiduanOfficialBD",
        "Project": "Free Fire Wishlist Manager",
        "Message": "Welcome to Free Fire Wishlist Manager API"
    })

@app.route('/api/wishlist', methods=['GET', 'POST'])
def wishlist_manager():
    # ডিফল্ট এরর রেসপন্সের জন্যও সিরিয়াল ঠিক রাখা হলো
    error_response = {
        "Developer": "Riduanul Islam",
        "TelegramBot": "https://t.me/RiduanFFBot",
        "TelegramChannel": "https://t.me/RiduanOfficialBD"
    }
    
    jwt_token = request.args.get('jwt_token')
    eat_token = request.args.get('eat_token')
    access_token = request.args.get('access_token')
    uid = request.args.get('uid')
    password = request.args.get('password')
    items_param = request.args.get('items') or request.args.get('item_id')
    
    target_items = []
    if items_param:
        target_items = [int(x.strip()) for x in items_param.split(',') if x.strip().isdigit()]
        if not target_items:
            error_response["error"] = "Invalid items provided."
            return jsonify(error_response), 400
    else:
        target_items = DEFAULT_WISHLIST_ITEMS

    active_jwt = None
    
    if jwt_token:
        active_jwt = jwt_token
        
    elif eat_token:
        extracted_access_token = get_access_token_from_eat(eat_token)
        if not extracted_access_token:
            error_response["error"] = "Failed to extract access_token. Invalid EAT token."
            return jsonify(error_response), 401
        active_jwt = get_jwt_from_access_token(extracted_access_token)
            
    elif access_token:
        active_jwt = get_jwt_from_access_token(access_token)
            
    elif uid and password:
        acc_data = get_account_from_guest(uid, password)
        if acc_data and acc_data.get('jwt_token'):
            active_jwt = acc_data.get('jwt_token')
    else:
        error_response["error"] = "Missing authentication parameters."
        return jsonify(error_response), 400

    if not active_jwt:
        error_response["error"] = "Failed to authenticate or generate token. Server might be busy."
        return jsonify(error_response), 401

    # JWT থেকে অ্যাকাউন্টের তথ্য বের করা
    game_uid, region = extract_info_from_jwt(active_jwt)

    start_time = time.time()
    
    # উইশলিস্টে আইটেম অ্যাড করা
    if len(target_items) == 1:
        result = add_to_wishlist_single(active_jwt, target_items[0])
        success_count = 1 if result['success'] else 0
        failed_count = 0 if result['success'] else 1
        details = [result]
    else:
        results = process_wishlist_batch(active_jwt, target_items)
        success_count = len(results['success_items'])
        failed_count = len(results['failed_items'])
        # Details এ শুধু আইটেমগুলোর লিস্ট দেওয়া হচ্ছে
        details = results['success_items'] + results['failed_items']

    elapsed_time = time.time() - start_time

    # একদম আপনার চাওয়া অনুযায়ী সিরিয়াল মেইনটেইন করে ফাইনাল রেসপন্স তৈরি
    final_response = {
        "Developer": "Riduanul Islam",
        "TelegramBot": "https://t.me/RiduanFFBot",
        "TelegramChannel": "https://t.me/RiduanOfficialBD",
        "Account_Info": {
            "Game_UID": game_uid,
            "Region": region
        },
        "Details": details,
        "Task_Summary": {
            "Status": "Success",
            "Total_Items_Requested": len(target_items),
            "Successfully_Added": success_count,
            "Failed_To_Add": failed_count,
            "Total_Time_Taken": f"{round(elapsed_time, 2)} seconds"
        }
    }
        
    return jsonify(final_response)

if __name__ == '__main__':
    print("="*50)
    print("🚀 Wishlist API Server Started")
    print(f"📦 Active Game Version: {CLIENT_VERSION}")
    print("="*50)
    app.run(host='0.0.0.0', port=8000, debug=False)
