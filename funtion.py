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
from flask_cors import CORS
from matplotlib import font_manager as fm
from datetime import datetime  # Import the datetime class

app = Flask(__name__)
CORS(app)


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
Staggers_collection = db["Staggers"]       # สำหรับเก็บข้อมูลโรคไขมันในเลือด
Diabetes_collection = db["Diabetes"]       # สำหรับเก็บข้อมูลโรคไขมันในเลือด
blood_fat_collection = db["blood-fat"]       # สำหรับเก็บข้อมูลโรคไขมันในเลือด
Disease_collection = db["Disease-status"]       # สำหรับเก็บข้อมูลความมเสี่ยง
# กำหนด collection ทั้ง 4
user_profiles = db['user_profiles']
diabetes_tests = db['diabetes_tests']
food_recommendations = db['food_recommendations']
daily_activities = db['daily_activities']

LINE_API_URL = "https://api.line.me/v2/bot/message/push"
#myhealth
# LINE_ACCESS_TOKEN = "1x3tE+qWFFWfG2wxF3B8iemgo4N9PSNxQ9pkXc66w+cq00iPoCgxq1XdHOVZHl+sgeWzO5TtQvYp8z/LgvUlwHrVWBCC9zp+FJrJGHeT9NoMJ9OQvpGDXAsYOuEYMRA/53Q0qkOCkRuiMa4VTENihAdB04t89/1O/w1cDnyilFU="
#sipsinse
LINE_ACCESS_TOKEN = "NeXMAZt6QoDOwz7ryhruPZ0xrkfHbWPhQVvA9mLII8Y0CAeOTB7zXUGhzs8Q6JhT8ntAKAilCJQKjE/6rTfonbVRFTLkg7WL8rtzfHisWYBLbOCc6jkx6iePMA1VNJuqN/0B05f3+jq8d2nOeFnGQgdB04t89/1O/w1cDnyilFU="


ngrok = "https://6358-223-206-78-182.ngrok-free.app"
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

def compare_and_visualize_diabetes_data():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']

    # ดึงข้อมูลจาก MongoDB ตาม user_id
    latest_data = Diabetes_collection.find_one({"userId": user}, sort=[("timestamp", -1)])  # ข้อมูลล่าสุด
    previous_data = list(Diabetes_collection.find({"userId": user}))  # ข้อมูลก่อนหน้า (หลายชุด)

    print(f"ข้อมูลล่าสุด{latest_data}")
    print(f"ข้อมูลเก่า{previous_data}")

    if not latest_data or len(previous_data) == 0:
        return "ไม่พบข้อมูลที่ต้องการเปรียบเทียบ", None

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
    font_path = r"D:\masaidee\Internship\from\THSarabun\THSarabun.ttf"  # แก้ไขเส้นทางไปยังฟอนต์ไทยที่คุณใช้งาน

    # โหลดฟอนต์ที่ระบุ
    prop = fm.FontProperties(fname=font_path)

    # สร้างกราฟ
    labels = [key for key in latest_avg.keys() if key != "อายุ"]
    latest_values = [latest_avg[key] for key in labels]
    previous_values = [previous_avg[key] for key in labels]

    plt.figure(figsize=(8, 6))
    plt.bar(range(len(labels)), latest_values, width=0.4, label="ข้อมูลล่าสุด", color="blue")
    plt.bar([i + 0.4 for i in range(len(labels))], previous_values, width=0.4, label="ค่าเฉลี่ยก่อนหน้า", color="orange")
    plt.xticks([i + 0.2 for i in range(len(labels))], labels, fontproperties=prop, rotation=45, ha='right')
    plt.ylabel("ค่าเฉลี่ย", color="red", fontsize=20, fontproperties=prop)
    plt.xlabel("ค่าของผู้ใช้", color="blue", fontsize=20, fontproperties=prop)
    plt.title("เปรียบเทียบ", fontproperties=prop, fontsize=30, color="red")
    plt.legend(prop=prop)
    plt.tight_layout()
    now = datetime.now()
    # แสดงวันที่และเวลาในรูปแบบที่ต้องการ
    formatted_time = now.strftime("%d-%m-%Y.%H-%M-%S")
    user_dir = os.path.join(f"static/{user}")
    os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
    graph_path = os.path.join(f"{user_dir}/{formatted_time}.png")
    plt.savefig(graph_path)
    plt.close()


    print(formatted_time)
    image_url = f"{ngrok}/{graph_path}"


    # send_comparison_result(user, comparison_result, image_url)
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
        return "เกิดข้อผิดพลาด: ไม่พบข้อมูลผู้ใช้ในระบบ"

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
    
    # ตรวจสอบว่าพบข้อมูลหรือไม่
    if not user_data_diabetes:
        return "ไม่พบข้อมูลผู้ใช้ในระบบ"

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

    if prediction[0] == 1:
        reply_text = "ความเสี่ยงต่ำ"
    elif prediction[0] == 2:
        reply_text = "ความเสี่ยงปานกลาง"
    else:
        reply_text = "ความเสี่ยงสูง"


            
    if ht == 1:
        ht_str = "มีประวัติ"
    else:
        ht_str = "ไม่มีประวัติ"

    if family_his == 1:
        family_his_str = "มีประวัติ"
    else:
                    family_his_str = "ไม่มีประวัติ"

    return user, reply_text, age, bmi, visceral, wc, ht, ht_str, sbp, dbp, fbs, HbAlc, family_his, family_his_str
   
#เพิ่มข้อมูล
def insertData():
    req = request.get_json(silent=True, force=True)
    user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    URL_add_user_form = f"{ngrok}/add_user_form"
    URL_add_diabetes_form = f"{ngrok}/add_diabetes_form"
    URL_add_blood_fat_form = f"{ngrok}/add_blood-fat_form"
    return user, URL_add_user_form, URL_add_diabetes_form, URL_add_blood_fat_form

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