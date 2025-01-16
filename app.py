from flask import Flask, request, jsonify
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
    flex,
    flex2
    )
from funtion import (compare_and_visualize_diabetes_data,
                     Checkup_blood_fat,
                     Checkup_diabetes
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



LINE_API_URL = "https://api.line.me/v2/bot/message/push"
#myhealth
# LINE_ACCESS_TOKEN = "1x3tE+qWFFWfG2wxF3B8iemgo4N9PSNxQ9pkXc66w+cq00iPoCgxq1XdHOVZHl+sgeWzO5TtQvYp8z/LgvUlwHrVWBCC9zp+FJrJGHeT9NoMJ9OQvpGDXAsYOuEYMRA/53Q0qkOCkRuiMa4VTENihAdB04t89/1O/w1cDnyilFU="
#sipsinse
LINE_ACCESS_TOKEN = "NeXMAZt6QoDOwz7ryhruPZ0xrkfHbWPhQVvA9mLII8Y0CAeOTB7zXUGhzs8Q6JhT8ntAKAilCJQKjE/6rTfonbVRFTLkg7WL8rtzfHisWYBLbOCc6jkx6iePMA1VNJuqN/0B05f3+jq8d2nOeFnGQgdB04t89/1O/w1cDnyilFU="

import warnings
from sklearn.exceptions import InconsistentVersionWarning
    
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user


@app.route('/webhook', methods=['GET'])
def home():
    return "Hello, Flask!"
# # 1. อ่านข้อมูลทั้งหมด (GET)
# @app.route("/api/users", methods=["GET"])
# def get_users():
#     users = list(users_collection.find())
#     return jsonify([serialize_user(user) for user in users]), 200

@app.route('/', methods=['POST'])
def MainFunction():
    # req = request.get_json()

    # # ดึงข้อมูลจาก Dialogflow
    # user_id = req.get("originalDetectIntentRequest", {}).get("payload", {}).get("data", {}).get("source", {}).get("userId", "unknown_user")
    # intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "unknown_intent")
    # parameters = req.get("queryResult", {}).get("parameters", "unknown_user")
    # timestamp = datetime.now()




    # รับข้อมูลที่ส่งมาจาก Dialogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    # ส่งคำตอบกลับไปยัง LINE
    response_json = {
        "fulfillmentText": answer_from_bot
    }
    return jsonify(response_json)

def generating_answer(question_from_dailogflow_raw):
    # ดึง queryResult จากข้อมูลที่ได้รับ
    question_from_dailogflow_dict = question_from_dailogflow_raw.get("queryResult", {})
    intent_name = question_from_dailogflow_dict.get("intent", {}).get("displayName", "")

    # ตรวจสอบค่า intent_name เพื่อเรียกใช้ฟังก์ชันที่ต้องการ 
    if intent_name == 'view_user_profile':#กรอกข้อมูลโรคสมอง ลงใน monggodb ทำนายโรคสมอง
        answer_str = add_user() 
    elif intent_name == 'Diabetes - custom':#กรอกข้อมูลโรคเบาหวาน ลงใน monggodb ทำนายโรคเบาหวาน
        answer_str = (question_from_dailogflow_dict) 
    elif intent_name == 'Blood fat - custom':#กรอกข้อมูลโรคไขมันในเลือด ลงใน monggodb ทำนายโรคไขมันในเลือด
        answer_str = ()

    elif intent_name == 'compare':#กรอกข้อมูลโรคไขมันในเลือด ลงใน monggodb ทำนายโรคไขมันในเลือด
        answer_str = send_comparison_result()

    elif intent_name == 'Checkup_blood-fat':  # ตรวจโรคไขมันในเลือดโดยที่ไม่ต้องกรอกข้อมูล แต่เป็นการดึงข้อมูลจาก monggodb มาใช้
        answer_str = send_blood_fat()
    elif intent_name == 'Checkup_diabetes':  # ตรวจโรคเบาหวาน โดยที่ไม่ต้องกรอกข้อมูล แต่เป็นการดึงข้อมูลจาก monggodb มาใช้
        answer_str = send_diabetes()
    elif intent_name == "view_user_profile":
        answer_str = send_diabetes()
    else:
        answer_str = "คุณต้องการแบบไหน"
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
    if bmi > 24.9:
        recommendations.append("- aaaaaaaaaaaaaaaaaaaaaaclscls")
    if visceral > 9:
        recommendations.append("- ลดการบริโภคอาหารที่มีน้ำตาลและไขมันทรานส์")
    if wc >= 0.50:
        recommendations.append("- เพิ่มการบริโภคอาหารที่ช่วยเพิ่ม HDL เช่น ปลาที่มีโอเมก้า-4")
    if ht == 1:
        recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")
    if sbp >= 120:
        recommendations.append("- ลดการบริโภคอาหารที่มีคอเลสเตอรอลสูง")
    if dbp >= 80:
        recommendations.append("- ลดการบริโภคอาหารที่มีน้ำตาลและไขมันทรานส์")
    if fbs >= 80:
        recommendations.append("- เพิ่มการบริโภคอาหารที่ช่วยเพิ่ม HDL เช่น ปลาที่มีโอเมก้า-912")
    if HbAlc > 5.6:
        recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")
    if family_his == 0:
        recommendations.append("- ลดการบริโภคไขมันอิ่มตัวและอาหารที่มี LDL สูง")


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


def send_comparison_result():
    user, comparison_result, image_url = compare_and_visualize_diabetes_data()
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    comparison_text = "\n".join(comparison_result)

    Flex_message = []

    if user:
        # เพิ่มข้อความการวิเคราะห์ความเสี่ยง
        predict = flex2(comparison_text, image_url)
        if predict:  # ตรวจสอบว่า message ถูกสร้างและไม่ว่างเปล่า
            Flex_message.append(predict)

        # เพิ่มข้อความการวิเคราะห์ข้อมูล
        analysis_data = flex(comparison_text, image_url)
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

@app.route('/api/user_profiles', methods=['GET'])
def get_user_profile():
    user_id = request.args.get('user_id')
    user_profiles = db["user_profiles"]       # สำหรับเก็บข้อมูลความมเสี่ยง
    try:
        user_profile = user_profiles.find_one({"_id": 121})
        if user_profile:
            return jsonify(serialize_user(user_profile)), 200
        else:
            return jsonify({"error": "User profile not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data.get("_id")
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    weight = data.get("weight")
    height = data.get("height")

    if not all([user_id, name, age, gender, weight, height]):
        return jsonify({"error": "Missing data"}), 400

    user_data = {
        "_id": user_id,
        "name": name,
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height
    }

    try:
        db.users.insert_one(user_data)
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/user_profiles', methods=['POST'])
def add_user_profile():
    
    # user_profiles = db["user_profiles"] 
    
    data = request.get_json()
    user_id = data.get("_id")
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    weight = data.get("weight")
    height = data.get("height")

    if not all([user_id, name, age, gender, weight, height]):
        return jsonify({"error": "Missing data"}), 400

    user_profile_data = {
        "_id": user_id,
        "name": name,
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height
    }

    try:
        db.user_profiles.insert_one(user_profile_data)
        return jsonify({"message": "User profile added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    app.run(debug=False, port=5000)



