from flask import Flask, request, jsonify, render_template, redirect
import json
import requests
import numpy as np
from pymongo import MongoClient
import pickle
import os
import requests
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib import font_manager as fm
from datetime import datetime
from fuzzywuzzy import process, fuzz




    # โหลดโมเดลที่ใช้ทำนายโรคสมอง
with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\model_stroke_risk.pkl", 'rb') as model_file:
    Staggers_classifier = pickle.load(model_file)
    
    # โหลดโมเดลที่ใช้ทำนายโรคเบาหวาน
with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\model_blood_fat.pkl", 'rb') as model_file:
    Blood_fat_classifier = pickle.load(model_file)

    # โหลดโมเดลที่ใช้ทำนายโรคไขมันในเลือด
with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\model_dm_risk.pkl", 'rb') as model_file:
    Diabetes_classifier = pickle.load(model_file)

# การเชื่อมต่อ MongoDB 
MONGO_URI = "mongodb://localhost:27017/"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["health"]  # ฐานข้อมูลสำหรับเก็บข้อมูลโรค
Staggers_collection = db["Staggers"]            # สำหรับเก็บข้อมูลโรคสมอง
Diabetes_collection = db["Diabetes"]            # สำหรับเก็บข้อมูลโรคเบาหวาน
blood_fat_collection = db["blood-fat"]          # สำหรับเก็บข้อมูลโรคไขมันในเลือด
Disease_collection = db["Disease-status"]       # สำหรับเก็บข้อมูลความมเสี่ยงของโรค
user_profiles = db['user_profiles']             # สำหรับเก็บข้อมูลผู้ใช้


LINE_API_URL = "https://api.line.me/v2/bot/message/push"
#myhealth
# LINE_ACCESS_TOKEN = "1x3tE+qWFFWfG2wxF3B8iemgo4N9PSNxQ9pkXc66w+cq00iPoCgxq1XdHOVZHl+sgeWzO5TtQvYp8z/LgvUlwHrVWBCC9zp+FJrJGHeT9NoMJ9OQvpGDXAsYOuEYMRA/53Q0qkOCkRuiMa4VTENihAdB04t89/1O/w1cDnyilFU="
#sipsinse
LINE_ACCESS_TOKEN = "NeXMAZt6QoDOwz7ryhruPZ0xrkfHbWPhQVvA9mLII8Y0CAeOTB7zXUGhzs8Q6JhT8ntAKAilCJQKjE/6rTfonbVRFTLkg7WL8rtzfHisWYBLbOCc6jkx6iePMA1VNJuqN/0B05f3+jq8d2nOeFnGQgdB04t89/1O/w1cDnyilFU="
#myhealth2
# LINE_ACCESS_TOKEN = "+mxXTWUhft/lds9sjCQLThOE7hSpYYa3Qc9Ex8f+/7NNB6075OpjZ0jIC/83ABlncS0BObm5K+8oDnHck6sKcILblYZv9AUU8TllWdaHWHWIE8Cp9Z1ybS0jfzi5iF6hDwggWQurGYX93oAOwwr9CQdB04t89/1O/w1cDnyilFU="
# LINE_ACCESS_TOKEN = "dlmMJIDuAnFTOrIxt1IjvGRihrCyyINAXB2QaTDGEUaikjefh2dZ7CFOk3hpBGSXNqCClqCGkeMULxN3tfC4DAYl/5c15dL1rTEhZ9AwyF7XSx2A7Cs4/pJhlQQWISwT2bWsyzxc9lxK8vDbAj8YnAdB04t89/1O/w1cDnyilFU="

ngrok = "https://a69c-223-205-176-129.ngrok-free.app"

#การเปรียบเทียบ
def calculate_average(data_list):
    averages = {}
    count = len(data_list)

    for data in data_list:
        for key, value in data.items():
            if isinstance(value, (int, float)):  # เฉพาะค่าตัวเลข
                if key not in averages:
                    averages[key] = 0
                averages[key] += value

    for key in averages:
        averages[key] /= count

    return averages

def translate_keys(data, key_mapping):
    translated_data = {}
    for key, value in data.items():
        translated_key = key_mapping.get(key, key)
        translated_data[translated_key] = value
    return translated_data

def send_line_message(user, text):
    """ ฟังก์ชันส่งข้อความแจ้งเตือนกลับไปที่ LINE """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    message = {
        "to": user,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }
    requests.post(LINE_API_URL, headers=headers, data=json.dumps(message))

#การเปรียบเทียบโรคเบาหวาน
def compare_and_visualize_diabetes_data():
    req = request.get_json(silent=True, force=True)

    # ตรวจสอบว่า req มีข้อมูลและมี userId หรือไม่
    try:
        user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    except (KeyError, TypeError):
        print("❌ ไม่สามารถดึง userId จาก request ได้")
        return None, None, None, None

    # ดึงข้อมูลจาก MongoDB ตาม user_id
    latest_data = Diabetes_collection.find_one({"userId": user}, sort=[("timestamp", -1)])

    if not latest_data:
        print(f"❌ ไม่พบข้อมูลล่าสุดของ user: {user}")
        send_line_message(user, "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ")
        return None, None, None, None

    previous_data = list(Diabetes_collection.find(
        {"userId": user, "timestamp": {"$lt": latest_data['timestamp']}},
        sort=[("timestamp", -1)]
    ))

    print(f"✅ ข้อมูลล่าสุด: {latest_data}")
    print(f"📌 ข้อมูลเก่า: {previous_data}")

    if not previous_data:
        print(f"⚠ ไม่มีข้อมูลก่อนหน้าเพื่อเปรียบเทียบสำหรับ user: {user}")
        send_line_message(user, "ไม่มีข้อมูลเก่าเพื่อใช้ในการเปรียบเทียบ")
        return None, None, None, None


    # คำนวณค่าเฉลี่ย
    previous_avg = calculate_average(previous_data)
    latest_avg = {key: value for key, value in latest_data.items() if isinstance(value, (int, float))}

    # แผนที่การแปลคีย์
    key_mapping = {
        "age": "อายุ",
        "bmi": "ดัชนีมวลกาย",
        "visceral": "ไขมันในช่องท้อง",
        "wc": "รอบเอว",
        "ht": "ความสูง",
        "sbp": "ความดันตัวบน",
        "dbp": "ความดันตัวล่าง",
        "fbs": "น้ำตาลในเลือด",
        "HbAlc": "ฮีโมโกลบิน A1c",
        "family_his": "ประวัติครอบครัว"
    }

    # แปลคีย์ในข้อมูล
    latest_avg = translate_keys(latest_avg, key_mapping)
    previous_avg = translate_keys(previous_avg, key_mapping)

    # ระบุเส้นทางไปยังไฟล์ฟอนต์ที่รองรับภาษาไทย
    font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"

    # โหลดฟอนต์ที่ระบุ
    prop = fm.FontProperties(fname=font_path)
    prop.set_size(20)

    # สร้างกราฟ
    labels = [key for key in latest_avg.keys() if key != "อายุ"]
    latest_values = [latest_avg[key] for key in labels]
    previous_values = [previous_avg[key] for key in labels]

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
    plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
    plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right', fontsize=20)
    plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=30, fontproperties=prop)
    plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=30, fontproperties=prop)
    plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
    plt.legend(prop=prop)
    plt.tight_layout()

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d.%H-%M-%S")
    user_dir = os.path.join(f"static/{user}")
    os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
    graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
    plt.savefig(graph_path)
    plt.close()

    print(formatted_time)
    image_url = f"{ngrok}/{graph_path}"

    return user, latest_avg, previous_avg, image_url

#การเปรียบเทียบโรคไขมันในเลือด
def compare_and_visualize_blood_fat_data():
    req = request.get_json(silent=True, force=True)
    # ตรวจสอบว่า req มีข้อมูลและมี userId หรือไม่
    try:
        user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    except (KeyError, TypeError):
        print("❌ ไม่สามารถดึง userId จาก request ได้")
        return None, None, None, None

    # ดึงข้อมูลจาก MongoDB ตาม user_id
    latest_data = blood_fat_collection.find_one({"userId": user}, sort=[("timestamp", -1)])

    if not latest_data:
        print(f"❌ ไม่พบข้อมูลล่าสุดของ user: {user}")
        send_line_message(user, "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ")
        return None, None, None, None

    previous_data = list(blood_fat_collection.find(
        {"userId": user, "timestamp": {"$lt": latest_data['timestamp']}},
        sort=[("timestamp", -1)]
    ))

    print(f"✅ ข้อมูลล่าสุด: {latest_data}")
    print(f"📌 ข้อมูลเก่า: {previous_data}")

    if not previous_data:
        print(f"⚠ ไม่มีข้อมูลก่อนหน้าเพื่อเปรียบเทียบสำหรับ user: {user}")
        send_line_message(user, "ไม่มีข้อมูลเก่าเพื่อใช้ในการเปรียบเทียบ")
        return None, None, None, None

    # คำนวณค่าเฉลี่ย
    previous_avg = calculate_average(previous_data)
    latest_avg = {key: value for key, value in latest_data.items() if isinstance(value, (int, float))}

    # แผนที่การแปลคีย์
    key_mapping = {
        "Gender": "เพศ",
        "Weight": "น้ำหนัก",
        "Height": "ส่วนสูง",
        "Cholesterol": "คอเลสเตอรอล",
        "Triglycerider": "ไตรกลีเซอไรด์",
        "Hdl": "เอชดีแอล",
        "Ldl": "แอลดีแอล"
    }

    # แปลคีย์ในข้อมูล
    latest_avg = translate_keys(latest_avg, key_mapping)
    previous_avg = translate_keys(previous_avg, key_mapping)

    # ระบุเส้นทางไปยังไฟล์ฟอนต์ที่รองรับภาษาไทย
    font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"  # แก้ไขเส้นทางไปยังฟอนต์ไทยที่คุณใช้งาน

    # โหลดฟอนต์ที่ระบุ
    prop = fm.FontProperties(fname=font_path)
    prop.set_size(20)  # ตั้งค่าขนาดตัวอักษร

    # สร้างกราฟ
    labels = [key for key in latest_avg.keys() if key != "อายุ"]
    latest_values = [latest_avg[key] for key in labels]
    previous_values = [previous_avg[key] for key in labels]

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
    plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
    plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right', fontsize=20)
    plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=30, fontproperties=prop)
    plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=30, fontproperties=prop)
    plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
    plt.legend(prop=prop)
    plt.tight_layout()
    now = datetime.now()
    # แสดงวันที่และเวลาในรูปแบบที่ต้องการ
    formatted_time = now.strftime("%Y-%m-%d.%H-%M-%S")
    user_dir = os.path.join(f"static/{user}")
    os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
    graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
    plt.savefig(graph_path)
    plt.close()

    image_url = f"{ngrok}/{graph_path}"

    return user, latest_avg, previous_avg, image_url

#การเปรียบเทียบโรคสมอง
def compare_and_visualize_staggers_data():
    req = request.get_json(silent=True, force=True)
    # ตรวจสอบว่า req มีข้อมูลและมี userId หรือไม่
    try:
        user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    except (KeyError, TypeError):
        print("❌ ไม่สามารถดึง userId จาก request ได้")
        return None, None, None, None

    # ดึงข้อมูลจาก MongoDB ตาม user_id
    latest_data = Staggers_collection.find_one({"userId": user}, sort=[("timestamp", -1)])

    if not latest_data:
        print(f"❌ ไม่พบข้อมูลล่าสุดของ user: {user}")
        send_line_message(user, "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ")
        return None, None, None, None

    previous_data = list(Staggers_collection.find(
        {"userId": user, "timestamp": {"$lt": latest_data['timestamp']}},
        sort=[("timestamp", -1)]
    ))

    print(f"✅ ข้อมูลล่าสุด: {latest_data}")
    print(f"📌 ข้อมูลเก่า: {previous_data}")

    if not previous_data:
        print(f"⚠ ไม่มีข้อมูลก่อนหน้าเพื่อเปรียบเทียบสำหรับ user: {user}")
        send_line_message(user, "ไม่มีข้อมูลเก่าเพื่อใช้ในการเปรียบเทียบ")
        return None, None, None, None

    # คำนวณค่าเฉลี่ย
    previous_avg = calculate_average(previous_data)
    latest_avg = {key: value for key, value in latest_data.items() if isinstance(value, (int, float))}

    # แผนที่การแปลคีย์
    key_mapping = {
        "sbp": "ความดันตัวบน",
        "dbp": "ความดันตัวล่าง",
        "his": "ประวัติการรักษา",
        "smoke": "การสูบบุหรี่",
        "fbs": "น้ำตาลในเลือด",
        "HbAlc": "ฮีโมโกลบิน A1c",
        "total_Cholesterol": "คอเลสเตอรอลรวม",
        "Exe": "การออกกำลังกาย",
        "bmi": "ดัชนีมวลกาย",
        "family_his": "ประวัติครอบครัว"
    }

    # แปลคีย์ในข้อมูล
    latest_avg = translate_keys(latest_avg, key_mapping)
    previous_avg = translate_keys(previous_avg, key_mapping)

    # ระบุเส้นทางไปยังไฟล์ฟอนต์ที่รองรับภาษาไทย
    font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"  # แก้ไขเส้นทางไปยังฟอนต์ไทยที่คุณใช้งาน

    # โหลดฟอนต์ที่ระบุ
    prop = fm.FontProperties(fname=font_path)
    prop.set_size(20)  # ตั้งค่าขนาดตัวอักษร

    # สร้างกราฟ
    labels = [key for key in latest_avg.keys()]
    latest_values = [latest_avg[key] for key in labels]
    previous_values = [previous_avg[key] for key in labels]

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
    plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
    plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right', fontsize=20)
    plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=30, fontproperties=prop)
    plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=30, fontproperties=prop)
    plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
    plt.legend(prop=prop)
    plt.tight_layout()
    now = datetime.now()
    # แสดงวันที่และเวลาในรูปแบบที่ต้องการ
    formatted_time = now.strftime("%Y-%m-%d.%H-%M-%S")
    user_dir = os.path.join(f"static/{user}")
    os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
    graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
    plt.savefig(graph_path)
    plt.close()

    image_url = f"{ngrok}/{graph_path}"

    return user, latest_avg, previous_avg, image_url



#เช็คโรคไขมันในเลือด
def Checkup_blood_fat():
    req = request.get_json(silent=True, force=True)
    intent = req['queryResult']['intent']['displayName']
    # user_id = req['queryResult']['parameters'].get('user_id')
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    print("Intent:", intent)
    # print("User ID:", user_id)
    print("User:", user)
    
    # ดึงข้อมูลจาก MongoDB ตาม user_id
    user_data_blood_fat = blood_fat_collection.find_one({"userId": user},sort=[("timestamp", -1)]) # timestamp 1=เรียงจากน้อยไปมาก, timestamp -1=เรียงจากมากไปน้อย
    print("User data:", user_data_blood_fat)
    # ตรวจสอบว่าพบข้อมูลหรือไม่
    if not user_data_blood_fat:
        send_line_message(user, "ไม่พบข้อมูลโรคไขมันในเลือดของคุณในระบบ กรุณาเพิ่มข้อมูลโรคไขมันในเลือดก่อนครับ")
        return None, None, None, None, None, None, None, None, None

    Gender = user_data_blood_fat.get("gender_str", 0)
    Weight = user_data_blood_fat.get("Weight", 0)
    Height = user_data_blood_fat.get("Height", 0)
    Cholesterol = user_data_blood_fat.get("Cholesterol", 0)
    Triglycerides = user_data_blood_fat.get("Triglycerides", 0)
    Hdl = user_data_blood_fat.get("Hdl", 0)
    Ldl = user_data_blood_fat.get("Ldl", 0)

    input_data = [[Gender, Weight, Height, Cholesterol, Triglycerides, Hdl, Ldl]]
    # print("Input data:", input_data)

    prediction = Blood_fat_classifier.predict(input_data)

    if prediction[0] == 0:
        reply_text = "ไม่มีความเสี่ยง"
    else:
        reply_text = "มีความเสี่ยง"
        
    #แปลงตัวเลขเป็น ข้อความ 
    if Gender == 0:
        Gender_status = "ชาย"
    else:
        Gender_status = "หญิง"

    # send_blood_fat(user, reply_text, Gender_status, Weight, Height, Cholesterol, Triglycerides, Hdl, Ldl)
    return user, reply_text, Gender_status, Weight, Height, Cholesterol, Triglycerides, Hdl, Ldl

#เช็คโรคเบาหวาน
def Checkup_diabetes():
    req = request.get_json(silent=True, force=True)
    intent = req['queryResult']['intent']['displayName']
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    print("Intent:", intent)
    print("User:", user)
    
    # ดึงข้อมูลจาก MongoDB ตาม user_id
    user_data_diabetes = Diabetes_collection.find_one({"userId": user}, sort=[("timestamp", -1)])
    print("User data:", user_data_diabetes)
    
    if not user_data_diabetes:
        send_line_message(user, "ไม่พบข้อมูลโรคเบาหวานของคุณในระบบ กรุณาเพิ่มข้อมูลโรคเบาหวานก่อนครับ")
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None

    age = user_data_diabetes.get("age", 0)
    bmi = user_data_diabetes.get("bmi", 0)
    visceral = user_data_diabetes.get("visceral", 0)
    wc = user_data_diabetes.get("wc", 0)
    ht = user_data_diabetes.get("ht", 0)
    sbp = user_data_diabetes.get("sbp", 0)
    dbp = user_data_diabetes.get("dbp", 0)
    fbs = user_data_diabetes.get("fbs", 0)
    HbAlc = user_data_diabetes.get("HbAlc", 0)
    family_his = user_data_diabetes.get("family_his", 0)

    

    input_data = [[age, bmi, visceral, wc, ht, sbp, dbp, fbs, HbAlc, family_his]]
    print("Input data:", input_data)

    prediction = Diabetes_classifier.predict(input_data)

    if prediction[0] == 0:
        reply_text = "ความเสี่ยงต่ำ"
    elif prediction[0] == 1:
        reply_text = "ความเสี่ยงปานกลาง"
    else:
        reply_text = "ความเสี่ยงสูง"


            
    if ht == 1:
        ht_str = "มี"
    else:
        ht_str = "ไม่มี"

    if family_his == 1:
        family_his_str = "มี"
    else:
        family_his_str = "ไม่มี"

    return user, reply_text, age, bmi, visceral, wc, ht, ht_str, sbp, dbp, fbs, HbAlc, family_his, family_his_str

#เช็คโรคสมอง
def Checkup_Staggers():
    req = request.get_json(silent=True, force=True)
    intent = req['queryResult']['intent']['displayName']
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    print("Intent:", intent)
    print("User:", user)
    
    # ดึงข้อมูลจาก MongoDB ตาม user_id
    user_data_staggers = Staggers_collection.find_one({"userId": user}, sort=[("timestamp", -1)])
    print("User data:", user_data_staggers)
    
    if not user_data_staggers:
        send_line_message(user, "ไม่พบข้อมูลโรคสมองของคุณในระบบ กรุณาเพิ่มข้อมูลโรคสมองก่อนครับ")
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

    sbp = user_data_staggers.get("sbp", 0)
    dbp = user_data_staggers.get("dbp", 0)
    his = user_data_staggers.get("his", 0)
    smoke = user_data_staggers.get("smoke", 0)
    fbs = user_data_staggers.get("fbs", 0)
    HbAlc = user_data_staggers.get("HbAlc", 0)
    total_Cholesterol = user_data_staggers.get("total_Cholesterol", 0)
    Exe = user_data_staggers.get("Exe", 0)
    bmi = user_data_staggers.get("bmi", 0)
    family_his = user_data_staggers.get("family_his", 0)

    

    input_data = [[sbp, dbp, his, smoke, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his]]
    print("Input data:", input_data)

    prediction = Staggers_classifier.predict(input_data)

    if prediction[0] == 0:
        reply_text = "ความเสี่ยงต่ำ"
    elif prediction[0] == 1:
        reply_text = "ความเสี่ยงปานกลาง"
    else:
        reply_text = "ความเสี่ยงสูง"


            
    if his == 1:
        his_str = "มี"
    else:
        his_str = "ไม่มี"

    if smoke == 0:
        smoke_str = "ไม่เคย"
    elif smoke == 1:
        smoke_str = "หยุดสูบ"
    else:
        smoke_str = "สูบอยู่"

    if Exe == 0:
        Exe_str = "0"
    elif Exe == 1:
        Exe_str = "150-200"
    else:
        Exe_str = "> 200"

    if family_his == 1:
        family_his_str = "มี"
    else:
        family_his_str = "ไม่มี"

    return user, reply_text, sbp, dbp, his, his_str, smoke, smoke_str, fbs, HbAlc, total_Cholesterol, Exe, Exe_str, bmi, family_his, family_his_str


life = "https://liff.line.me/2003057525-1L9EGXEO"
#เพิ่มข้อมูล
def insertData():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    URL_add_user_form = f"{life}/getUser"
    URL_add_diabetes_form = f"{life}/diabetes"
    URL_add_blood_fat_form = f"{life}/blood_fat"
    URL_add_staggers_form = f"{life}/staggers"
    return user, URL_add_user_form, URL_add_diabetes_form, URL_add_blood_fat_form, URL_add_staggers_form

#ดึงข้อมูลผู้ใช้
def getUser():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    user_data = user_profiles.find_one({"userId": user})
    print("User data:", user_data)
    if not user_data:
        return "ไม่พบข้อมูลผู้ใช้ในระบบ"
        # แปลง ObjectId เป็นสตริง
    user_data['_id'] = str(user_data['_id'])
    name = user_data.get("name", "")
    age = user_data.get("age", "")
    a = f"ชื่อ: {name} อายุ: {age}"
    return a






# โหลดโมเดลและข้อมูล
try:

    with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\questions__answers.pkl", "rb") as f:
        data = pickle.load(f)
        questions = data["questions"]
        answers = data["answers"]
except FileNotFoundError as e:
    print(f"เกิดข้อผิดพลาด: {e}")
    exit()

# ฟังก์ชัน การตอบคำถาม
def find_best_match_with_fuzzy(question, threshold=50):
    best_match = process.extractOne(question, questions, scorer=fuzz.partial_ratio)

    if best_match is None or best_match[1] < threshold:
        return "ขอโทษค่ะ ฉันไม่เข้าใจคำถาม กรุณาถามใหม่อีกครั้ง"

    best_answer = answers[questions.index(best_match[0])]

    # รับค่าปัจจุบันของวัน/เวลา
    now = datetime.now()
    today_date = now.strftime("%d/%m/%Y")
    today_name = now.strftime("%A")
    current_time = now.strftime("%H:%M:%S")

    days_th = {
        "Monday": "วันจันทร์",
        "Tuesday": "วันอังคาร",
        "Wednesday": "วันพุธ",
        "Thursday": "วันพฤหัสบดี",
        "Friday": "วันศุกร์",
        "Saturday": "วันเสาร์",
        "Sunday": "วันอาทิตย์"
    }

    # แทนค่าตัวแปรในข้อความ
    best_answer = best_answer.replace("{date}", today_date)
    best_answer = best_answer.replace("{day}", days_th.get(today_name, today_name))
    best_answer = best_answer.replace("{time}", current_time)

    return best_answer
