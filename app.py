from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, session
from pymongo import MongoClient
from bson.objectid import ObjectId
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
from payload import (
    flex_predict_blood_fat,
    flex_analysis_data_blood_fat,
    flex_recommendations_blood_fat,

    flex_predict_diabetes,
    flex_analysis_data_diabetes,
    flex_recommendations_diabetes,

    flex_predict_Staggers,
    flex_analysis_data_Staggers,
    flex_recommendations_Staggers,

    compare_diabetes,
    compare_img_diabetes,
    payloadinsertData
    )
from funtion import (compare_and_visualize_diabetes_data,
                     compare_and_visualize_blood_fat_data,
                     compare_and_visualize_staggers_data,

                     find_best_match_with_fuzzy,
                     
                     Checkup_blood_fat,
                     Checkup_diabetes,
                     Checkup_Staggers,
                     insertData,
                     getUser
                     )



app = Flask(__name__)
CORS(app)



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


def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user


# @app.route('/webhook1', methods=['POST'])
# def home():
    # return "Hello, Flask!"

# 1. อ่านข้อมูลทั้งหมด (GET)
# @app.route("/api/users", methods=["GET"])
# def get_users():
#     users = list(users_collection.find())
#     return jsonify([serialize_user(user) for user in users]), 200



@app.route('/', methods=['POST'])
def MainFunction():
    
    # รับข้อมูลที่ส่งมาจาก Dialogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    print("Received request:", question_from_dailogflow_raw)  # Debugging line
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    # ส่งคำตอบกลับไปยัง LINE
    response_json = {
        "fulfillmentText": answer_from_bot
    }
    print("Response to be sent:", response_json)  # Debugging line
    return jsonify(response_json)

def generating_answer(question_from_dailogflow_raw):
    # ดึง queryResult จากข้อมูลที่ได้รับ
    question_from_dailogflow_dict = question_from_dailogflow_raw.get("queryResult", {})
    intent_name = question_from_dailogflow_dict.get("intent", {}).get("displayName", "")
    question = question_from_dailogflow_dict.get("queryText", "")
    

    # ตรวจสอบค่า intent_name เพื่อเรียกใช้ฟังก์ชันที่ต้องการ 
    if intent_name == 'insertData': #เพิ่มข้อมูล
        answer_str = send_insertData()

    elif intent_name == 'compare - diabetes': #เปรียบเทียบข้อมูล
        answer_str = send_comparison_result_diabetes()
    elif intent_name == 'compare - blood_fat': #เปรียบเทียบข้อมูล
        answer_str = send_comparison_result_blood_fat()
    elif intent_name == 'compare - staggers': #เปรียบเทียบข้อมูล
        answer_str = send_comparison_result_staggers()

    elif intent_name == 'getUser': #เปรียบเทียบข้อมูล
        answer_str = getUser()
    elif intent_name == 'Check - Blood_fat':  # ตรวจโรคไขมันในเลือดโดยที่ไม่ต้องกรอกข้อมูล แต่เป็นการดึงข้อมูลจาก monggodb มาใช้
        answer_str = send_blood_fat()
    elif intent_name == 'Check - Diabetes':  # ตรวจโรคเบาหวาน โดยที่ไม่ต้องกรอกข้อมูล แต่เป็นการดึงข้อมูลจาก monggodb มาใช้
        answer_str = send_diabetes()
    elif intent_name == 'Check - Staggers':  # ตรวจโรคสมอง โดยที่ไม่ต้องกรอกข้อมูล แต่เป็นการดึงข้อมูลจาก monggodb มาใช้
        answer_str = send_Staggers()
    else:
        # ถ้า intent_name ไม่ตรงกับเงื่อนไขที่กำหนด ให้ใช้ฟังก์ชัน find_best_match_with_fuzzy
        answer_str = find_best_match_with_fuzzy(question, threshold=50)

    return answer_str

def send_diabetes():

    user, reply_text, age, bmi, visceral, wc, ht, ht_str, sbp, dbp, fbs, HbAlc, family_his, family_his_str = Checkup_diabetes()
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    if reply_text == "ความเสี่ยงต่ำ":
        reply_text_color = "#008000"  # สีเขียว
    elif reply_text == "ความเสี่ยงปานกลาง":
        reply_text_color = "#FFD700"  # ฟอนต์สีเหลืองทอง
    else:
        reply_text_color = "#FF0000"  # สีแดงถ้า 

    colors = {
        "bmi": "#008000" if bmi < 24.9 else "#FF0000",
        "visceral": "#008000" if visceral < 9 else "#FF0000",
        "wc": "#008000" if wc <= 0.50 else "#FF0000",
        "ht": "#008000" if ht == 0 else "#FF0000",
        "sbp": "#008000" if sbp <= 120 else "#FF0000",
        "dbp": "#008000" if dbp <= 80 else "#FF0000",
        "fbs": "#008000" if fbs <= 80 else "#FF0000",
        "HbAlc": "#008000" if HbAlc < 5.6 else "#FF0000",
        "family_his": "#008000" if family_his == 0 else "#FF0000"
    }

    # สร้างรายการคำแนะนำเพิ่มเติม
    recommendations = []
    if reply_text == "ความเสี่ยงต่ำ":
        recommendations.append("- เพื่อป้องกันการเกิดโรคเบาหวานในอนาคต ควรออกกำลังกายอย่างสม่ำเสมอ ควบคุมน้ำหนักตัวให้อยู่ในเกณฑ์ปกติ ความ ดันโลหิตโดยไม่ควรเกิน 140/90 มม.ปรอท")
    elif reply_text == "ความเสี่ยงปานกลาง":
        recommendations.append("- เพื่อป้องกันการเกิดโรคเบาหวานในอนาคต ควรออกกำลังกายอย่างสม่ำเสมอ ควบคุมน้ำหนักตัวให้อยู่ในเกณฑ์ปกติ ความ คันโลหิตโดยไม่ควรเกิน 140/90 มม.ปรอท และตรวจน้ำตาลในเลือด อย่างน้อยปีละ 1 ครั้ง ทุกปี")
    else:
        recommendations.append("- ด้วยมีโอกาสสูงมากที่จะเกิดโรคเบาหวานในอนาคต ควรควบคุมอาหารอย่างเคร่งครัดโดยเฉพาะเกี่ยวกับปริมาณคาร์โบไฮเดรตหรือคาร์บในอาหารซึ่งเป็นสารอาหารที่มีผลต่อระดับตาลในเลือด มากที่สุดเมื่อเทียบกับสารอาหารชนิดอื่น ๆมากที่สุดเมื่อเทียบกับสารอาหารชนิดอื่น ๆ ออกกำลังกายอย่างสม่ำเสมอ ควบคุมน้ำหนักตัวให้อยู่ในเกณฑ์ปกติ ความันโลหิตไม่ควรเกิน 140/90 มม.ปรอท และตรวจติดตามระดับน้ำตาลในเลือดอย่างน้อยปีละ 1 ครั้ง ทุกปี")
        
    # if bmi > 24.9:
    #     recommendations.append("- ใหม่")
    # if visceral > 9:
    #     recommendations.append("- ลดการบริโภคอาหารที่มีน้ำตาลและไขมันทรานส์")
    # if wc >= 0.50:
    #     recommendations.append("- เพิ่มการบริโภคอาหารที่ช่วยเพิ่ม HDL เช่น ปลาที่มีโอเมก้า-4")
    # if ht == 1:
    #     recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")
    # if sbp >= 120:
    #     recommendations.append("- ลดการบริโภคอาหารที่มีคอเลสเตอรอลสูง")
    # if dbp >= 80:
    #     recommendations.append("- ลดการบริโภคอาหารที่มีน้ำตาลและไขมันทรานส์")
    # if fbs >= 80:
    #     recommendations.append("- เพิ่มการบริโภคอาหารที่ช่วยเพิ่ม HDL เช่น ปลาที่มีโอเมก้า-912")
    # if HbAlc > 5.6:
    #     recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")
    # if family_his == 0:
    #     recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")

    print(type(recommendations))
    print(f"a{recommendations}")

    Flex_message = []    
    


    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = flex_predict_diabetes(reply_text, reply_text_color)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = flex_analysis_data_diabetes(age, bmi, visceral, wc, ht_str, sbp, dbp, fbs, HbAlc, family_his_str, colors)
        if analysis_data:
            Flex_message.append(analysis_data)

        # เพิ่มข้อความคำแนะนำ
        recommendations = flex_recommendations_diabetes(recommendations)
        if recommendations:
            Flex_message.append(recommendations)

            

    # ตรวจสอบว่ามีข้อความใน Flex_message ก่อนสร้าง payload
    if Flex_message:
        payload = {
            "to": user,
            "messages": Flex_message
        }
        # ส่งข้อมูลไปยัง LINE API
        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        # ตรวจสอบผลลัพธ์
        if response.status_code == 200:
            print("ส่งข้อความสำเร็จโรคเบาหวาน")
        else:
            print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}")
    else:
        print("ไม่มีข้อความที่ต้องส่ง")



def send_Staggers():
    user, reply_text, sbp, dbp, his, his_str, smoke, smoke_str, fbs, HbAlc, total_Cholesterol, Exe, Exe_str, bmi, family_his, family_his_str = Checkup_Staggers()
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    if reply_text == "ความเสี่ยงต่ำ":
        reply_text_color = "#008000"  # สีเขียว
    elif reply_text == "ความเสี่ยงปานกลาง":
        reply_text_color = "#FFD700"  # ฟอนต์สีเหลืองทอง
    else:
        reply_text_color = "#FF0000"  # สีแดงถ้า 

    colors = {
        "sbp": "#FF0000" if sbp > 130 else "#008000",
        "dbp": "#FF0000" if dbp > 85 else "#008000",
        "his": "#FF0000" if his == 1 else "#008000",
        "smoke": "#FF0000" if smoke == 2 else "#008000",
        "fbs": "#FF0000" if fbs > 125 else "#008000",
        "HbAlc": "#FF0000" if HbAlc > 6.0 else "#008000",
        "total_Cholesterol": "#FF0000" if total_Cholesterol > 240 else "#008000",
        "Exe": "#FF0000" if Exe == 0 else "#008000",
        "bmi": "#FF0000" if bmi > 30 else "#008000",
        "family_his": "#FF0000" if family_his == 1 else "#008000"
    }

    # สร้างรายการคำแนะนำเพิ่มเติม
    recommendations = []

    if reply_text == "ความเสี่ยงต่ำ":
        recommendations.append("- เพื่อป้องกันการเกิดโรคหลอดเลือดเลือดสมองในอนาคต ควรออกกำลังกายอย่างสม่ำเสมอควบคุมน้ำหนักตัวให้ BMI อยู่ในเกณฑ์ไม่เกิน 23 และควรประเมินความเสี่ยงทุก 2 ปี")
    elif reply_text == "ความเสี่ยงปานกลาง":
        recommendations.append("- เพื่อป้องกันก่รเกิดโรคหลอดเลือดสมองในอนาคต ควรควบคุมอาหาร ควบคุมน้ำหนักตัว ความดันโลหิตไม่ควรเกิน 120/80 มม.ปรอด ออกกำลังกายสม่ำเสมอ ควรงดการดื่มสุรา และสูบบุหรี่ และตรวจสุขภาพประจำปีทุกปี")
    else:
        recommendations.append("- เพื่อป้องกันการเกิดโรคหลอดเลือดสมองในอนาคต แนะนำให้ปรึกษาแพทย์ ควบคุมอาหาร ควบคุมนำหนักตัว ความดันโลหิตไม่ควรเกิน 120/80 มม.ปรอด ต้องงดการดื่มสุราและสูบบุหรี่อย่างเคร่งครัด รักษาดรคประจำตัวอย่างต่อเนื่องแลัตรวจสุขภาพประจำปีทุกปี")
    # if bmi > 24.9:
    #     recommendations.append("- ใหม่")
    # if his == 1:
    #     recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")
    # if sbp >= 120:
    #     recommendations.append("- ลดการบริโภคอาหารที่มีคอเลสเตอรอลสูง")
    # if dbp >= 80:
    #     recommendations.append("- ลดการบริโภคอาหารที่มีน้ำตาลและไขมันทรานส์")
    # if fbs >= 80:
    #     recommendations.append("- เพิ่มการบริโภคอาหารที่ช่วยเพิ่ม HDL เช่น ปลาที่มีโอเมก้า-912")
    # if HbAlc > 5.6:
    #     recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")
    # if family_his == 0:
    #     recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")

    print(type(recommendations))
    print(f"a{recommendations}")

    Flex_message = []    
    


    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = flex_predict_Staggers(reply_text, reply_text_color)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = flex_analysis_data_Staggers(sbp, dbp, his_str, smoke_str, fbs, HbAlc, total_Cholesterol, Exe_str, bmi, family_his_str, colors)
        if analysis_data:
            Flex_message.append(analysis_data)

        # เพิ่มข้อความคำแนะนำ
        recommendations = flex_recommendations_Staggers(recommendations)
        if recommendations:
            Flex_message.append(recommendations)

            

    # ตรวจสอบว่ามีข้อความใน Flex_message ก่อนสร้าง payload
    if Flex_message:
        payload = {
            "to": user,
            "messages": Flex_message
        }
        # ส่งข้อมูลไปยัง LINE API
        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        # ตรวจสอบผลลัพธ์
        if response.status_code == 200:
            print("ส่งข้อความสำเร็จโรคเบาหวาน")
        else:
            print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}")
    else:
        print("ไม่มีข้อความที่ต้องส่ง")


def send_blood_fat():

    user, reply_text, Gender_status, Weight, Height, Cholesterol, Triglycerides, Hdl, Ldl = Checkup_blood_fat()

    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # กำหนดสีข้อความตามเงื่อนไข
    colors = {
        "Cholesterol": "#FF0000" if Cholesterol >= 200 else "#008000",
        "Triglycerides": "#FF0000" if Triglycerides >= 150 else "#008000",
        "Hdl": "#FF0000" if Hdl <= 40 else "#008000",
        "Ldl": "#FF0000" if Ldl >= 100 else "#008000"
    }

    reply_text_color = "#FF0000" if reply_text == "มีความเสี่ยง" else "#008000"

    # สร้างรายการคำแนะนำเพิ่มเติม
    recommendations = []
    if Cholesterol >= 200:
        recommendations.append("- ลดการบริโภคอาหารที่มีคอเลสเตอรอลสูง")
    if Triglycerides >= 150:
        recommendations.append("- ลดการบริโภคอาหารที่มีน้ำตาลและไขมันทรานส์")
    if Hdl <= 40:
        recommendations.append("- เพิ่มการบริโภคอาหารที่ช่วยเพิ่ม HDL เช่น ปลาที่มีโอเมก้า-3")
    if Ldl >= 100:
        recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")

    print(recommendations)

    Flex_message = []

    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = flex_predict_blood_fat(reply_text, reply_text_color)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = flex_analysis_data_blood_fat(Gender_status, Weight, Height, Cholesterol, Triglycerides, Hdl, Ldl, colors)
        if analysis_data:
            Flex_message.append(analysis_data)

        # เพิ่มข้อความคำแนะนำ
        recommendations = flex_recommendations_blood_fat(recommendations)
        if recommendations:
            Flex_message.append(recommendations)

        print(type(Flex_message))

    # ตรวจสอบว่ามีข้อความใน Flex_message ก่อนสร้าง payload
    if Flex_message:
        payload = {
            "to": user,
            "messages": Flex_message
        }
        # ส่งข้อมูลไปยัง LINE API
        response = requests.post(LINE_API_URL, headers=headers, json=payload)

        # ตรวจสอบผลลัพธ์
        if response.status_code == 200:
            print("ส่งข้อความสำเร็จโรคไขมันในเลือด")
        else:
            print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}")
    else:
        print("ไม่มีข้อความที่ต้องส่ง")


def send_comparison_result_diabetes():
    user, latest_avg, previous_avg, image_url = compare_and_visualize_diabetes_data()
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    key1 = []
    diff1 = []
    avg1 = []
    print(key1)
    print(type(key1))
    for key in latest_avg.keys():
        if key == "อายุ":
            continue
        if key in previous_avg:
            diff = latest_avg[key] - previous_avg[key]
            if diff > 0:
                key1.append(key)
                diff1.append((round(diff, 1), "#00FF00"))  # ใช้รหัสสีเขียว
                avg1.append(f"({round(previous_avg[key], 1)} -> {round(latest_avg[key], 1)})")
            elif diff < 0:
                key1.append(key)
                diff1.append((round(diff, 1), "#FF0000"))  # ใช้รหัสสีแดง
                avg1.append(f"({round(previous_avg[key], 1)} -> {round(latest_avg[key], 1)})")
            else:
                key1.append(f"{key}: ไม่มีการเปลี่ยนแปลง")

    Flex_message = []
    
    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = compare_img_diabetes(image_url)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = compare_diabetes(key1, diff1, avg1)
        if analysis_data:
            Flex_message.append(analysis_data)

    payload = {
        "to": user,
        "messages": Flex_message
    }


    response = requests.post(LINE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("ส่งข้อความสำเร็จ")
    else:
        print(f"เกิดข้อผิดพลาดในการส่งข้อความa: {response.status_code}, {response.text}")

def send_comparison_result_blood_fat():
    user, latest_avg, previous_avg, image_url = compare_and_visualize_blood_fat_data()
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    key1 = []
    diff1 = []
    avg1 = []
    for key in latest_avg.keys():
        if key == "อายุ":
            continue
        if key in previous_avg:
            diff = latest_avg[key] - previous_avg[key]
            if diff > 0:
                key1.append(key)
                diff1.append((round(diff, 1), "#00FF00"))  # ใช้รหัสสีเขียว
                avg1.append(f"({round(previous_avg[key], 1)} -> {round(latest_avg[key], 1)})")
            elif diff < 0:
                key1.append(key)
                diff1.append((round(diff, 1), "#FF0000"))  # ใช้รหัสสีแดง
                avg1.append(f"({round(previous_avg[key], 1)} -> {round(latest_avg[key], 1)})")
            else:
                key1.append(f"{key}: ไม่มีการเปลี่ยนแปลง")

    Flex_message = []
    
    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = compare_img_diabetes(image_url)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = compare_diabetes(key1, diff1, avg1)
        if analysis_data:
            Flex_message.append(analysis_data)

    payload = {
        "to": user,
        "messages": Flex_message
    }

    response = requests.post(LINE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("ส่งข้อความสำเร็จ")
    else:
        print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}")

def send_comparison_result_staggers():
    user, latest_avg, previous_avg, image_url = compare_and_visualize_staggers_data()
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    key1 = []
    diff1 = []
    avg1 = []
    for key in latest_avg.keys():
        if key == "อายุ":
            continue
        if key in previous_avg:
            diff = latest_avg[key] - previous_avg[key]
            if diff > 0:
                key1.append(key)
                diff1.append((round(diff, 1), "#00FF00"))  # ใช้รหัสสีเขียว
                avg1.append(f"({round(previous_avg[key], 1)} -> {round(latest_avg[key], 1)})")
            elif diff < 0:
                key1.append(key)
                diff1.append((round(diff, 1), "#FF0000"))  # ใช้รหัสสีแดง
                avg1.append(f"({round(previous_avg[key], 1)} -> {round(latest_avg[key], 1)})")
            else:
                key1.append(f"{key}: ไม่มีการเปลี่ยนแปลง")

    Flex_message = []
    
    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = compare_img_diabetes(image_url)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = compare_diabetes(key1, diff1, avg1)
        if analysis_data:
            Flex_message.append(analysis_data)

    payload = {
        "to": user,
        "messages": Flex_message
    }

    response = requests.post(LINE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("ส่งข้อความสำเร็จ")
    else:
        print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {response.status_code}, {response.text}")

def send_insertData():
    user, URL_add_user_form, URL_add_diabetes_form, URL_add_blood_fat_form, URL_add_staggers_form = insertData()
    print("User:", user)

    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    Flex_message = []
    
    if user:

        predict = payloadinsertData(URL_add_user_form, URL_add_diabetes_form, URL_add_blood_fat_form, URL_add_staggers_form )
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

    payload = {
        "to": user,
        "messages": Flex_message
    }


    response = requests.post(LINE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("ส่งข้อความสำเร็จ")
    else:
        print(f"เกิดข้อผิดพลาดในการส่งข้อความa: {response.status_code}, {response.text}")





# สร้างเส้นทางสำหรับเรียกใช้งาน
@app.route('/add_user_form')
def index():
    return render_template('add_user_form.html')
# Route สำหรับเพิ่มข้อมูลใน user_profiles
@app.route('/add_user', methods=['POST'])
def add_user():
    userId = request.form['userId']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    height = request.form['height']
    weight = request.form['weight']
    timestamp = datetime.now().strftime("%d-%m-%Y.%H-%M-%S")
    user1 = {'userId': userId, 'name': name, 'age': age, 'gender': gender, 'height': height, 'weight': weight, 'timestamp': timestamp}
    user_profiles.insert_one(user1)
    return redirect('/add_user_form')

# สร้างเส้นทางสำหรับเรียกใช้งาน
@app.route('/add_diabetes_form')
def index1():
    return render_template('add_diabetes_form.html')
# Route สำหรับเพิ่มข้อมูลใน Diabetes_collection
@app.route('/add_Diabetes', methods=['POST'])
def add_Diabetes():
    userId = request.form['userId']
    age = request.form['age']
    bmi = request.form['bmi']
    visceral = request.form['visceral']
    wc = request.form['wc']
    ht = request.form['ht']
    sbp = request.form['sbp']
    dbp = request.form['dbp']
    fbs = request.form['fbs']
    HbAlc = request.form['HbAlc']
    family_his = request.form['family_his']

    try:
        age = float(age)
        bmi = float(bmi)
        visceral = float(visceral)
        wc = float(wc)
        ht = int(ht)
        sbp = float(sbp)
        dbp = float(dbp)
        fbs = float(fbs)
        HbAlc = float(HbAlc)
        family_his = int(family_his)
    except ValueError:
        return jsonify({"error": "Invalid input value"}), 400  # ส่งข้อความแสดงข้อผิดพลาดกลับไปยังผู้ใช้

    timestamp = datetime.now().strftime("%d-%m-%Y.%H-%M-%S")
    test = {
        'userId': userId,
        'age': age,
        'bmi': bmi,
        'visceral': visceral,
        'wc': wc,
        'ht': ht,
        'sbp': sbp,
        'dbp': dbp,
        'fbs': fbs,
        'HbAlc': HbAlc,
        'family_his': family_his,
        'timestamp': timestamp
    }
    Diabetes_collection.insert_one(test)
    return redirect('/add_diabetes_form')

# สร้างเส้นทางสำหรับเรียกใช้งาน
@app.route('/add_blood_fat_form')
def index2():
    return render_template('add_blood-fat_form.html')
# Route สำหรับเพิ่มข้อมูลใน Diabetes_collection
@app.route('/add_Blood_fat', methods=['POST'])
def add_Blood_fat():
    userId = request.form['userId']
    Gender = request.form['Gender']
    Weight = request.form['Weight']
    Height = request.form['Height']
    Cholesterol = request.form['Cholesterol']
    Triglycerider = request.form['Triglycerider']
    Hdl = request.form['Hdl']
    Ldl = request.form['Ldl']

    try:
        Gender = int(Gender)
        Weight = float(Weight)
        Height = float(Height)
        Cholesterol = float(Cholesterol)
        Triglycerider = float(Triglycerider)
        Hdl = float(Hdl)
        Ldl = float(Ldl)
    except ValueError:
        return jsonify({"error": "Invalid input value"}), 400  # ส่งข้อความแสดงข้อผิดพลาดกลับไปยังผู้ใช้

    timestamp = datetime.now().strftime("%d-%m-%Y.%H-%M-%S")
    test = {
        'userId': userId,
        'Gender': Gender,
        'Weight': Weight,
        'Height': Height,
        'Cholesterol': Cholesterol,
        'Triglycerider': Triglycerider,
        'Hdl': Hdl,
        'Ldl': Ldl,
        'timestamp': timestamp

    }
    blood_fat_collection.insert_one(test)
    return redirect('/add_blood_fat_form')


# สร้างเส้นทางสำหรับเรียกใช้งาน
@app.route('/add_staggers_form')
def index3():
    return render_template('add_staggers_form.html')
# Route สำหรับเพิ่มข้อมูลใน Diabetes_collection
@app.route('/add_Staggers', methods=['POST'])
def add_Staggers():
    userId = request.form['userId']
    sbp = request.form['sbp']
    dbp = request.form['dbp']
    his = request.form['his']
    smoke = request.form['smoke']
    fbs = request.form['fbs']
    HbAlc = request.form['HbAlc']
    total_Cholesterol = request.form['total_Cholesterol']
    Exe = request.form['Exe']
    bmi = request.form['bmi']
    family_his = request.form['family_his']

    try:
        sbp = float(sbp)
        dbp = float(dbp)
        his = int(his)
        smoke = int(smoke)
        fbs = float(fbs)
        HbAlc = float(HbAlc)
        total_Cholesterol = float(total_Cholesterol)
        Exe = float(Exe)
        bmi = float(bmi)
        family_his = int(family_his)
    except ValueError:
        return jsonify({"error": "Invalid input value"}), 400  # ส่งข้อความแสดงข้อผิดพลาดกลับไปยังผู้ใช้

    timestamp = datetime.now().strftime("%d-%m-%Y.%H-%M-%S")
    test = {
        'userId': userId,
        'sbp': sbp,
        'dbp': dbp,
        'his': his,
        'smoke': smoke,
        'fbs': fbs,
        'HbAlc': HbAlc,
        'total_Cholesterol': total_Cholesterol,
        'Exe': Exe,
        'bmi': bmi,
        'family_his': family_his,
        'timestamp': timestamp
    }
    Staggers_collection.insert_one(test)
    return redirect('/add_staggers_form')


















# import pickle
# from fuzzywuzzy import process, fuzz
# from datetime import datetime

# # โหลดโมเดลและข้อมูล
# try:
#     with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\chatbot_model.pkl", "rb") as f:
#         model = pickle.load(f)

#     with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\vectorizer.pkl", "rb") as f:
#         vectorizer = pickle.load(f)

#     with open(r"D:\masaidee\Internship\project\chatbot_line_myhealth\questions_answers.pkl", "rb") as f:
#         data = pickle.load(f)
#         questions = data["questions"]
#         answers = data["answers"]
# except FileNotFoundError as e:
#     print(f"เกิดข้อผิดพลาด: {e}")
#     exit()

# # ฟังก์ชัน Fuzzy Matching
# def find_best_match_with_fuzzy(question, threshold=50):
#     best_match = process.extractOne(question, questions, scorer=fuzz.partial_ratio)

#     if best_match is None or best_match[1] < threshold:
#         return "ขอโทษค่ะ ฉันไม่เข้าใจคำถาม กรุณาถามใหม่อีกครั้ง"

#     best_answer = answers[questions.index(best_match[0])]

#     # รับค่าปัจจุบันของวัน/เวลา
#     now = datetime.now()
#     today_date = now.strftime("%d/%m/%Y")
#     today_name = now.strftime("%A")
#     current_time = now.strftime("%H:%M:%S")

#     days_th = {
#         "Monday": "วันจันทร์",
#         "Tuesday": "วันอังคาร",
#         "Wednesday": "วันพุธ",
#         "Thursday": "วันพฤหัสบดี",
#         "Friday": "วันศุกร์",
#         "Saturday": "วันเสาร์",
#         "Sunday": "วันอาทิตย์"
#     }

#     # แทนค่าตัวแปรในข้อความ
#     best_answer = best_answer.replace("{date}", today_date)
#     best_answer = best_answer.replace("{day}", days_th.get(today_name, today_name))
#     best_answer = best_answer.replace("{time}", current_time)

#     return best_answer






if __name__ == "__main__":
    app.run(debug=False, port=5000)