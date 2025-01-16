from pymongo import MongoClient

# เชื่อมต่อกับ MongoDB (เชื่อมต่อกับ localhost ที่พอร์ต 27017)
client = MongoClient("mongodb://localhost:27017/")

# เลือกฐานข้อมูลที่ต้องการใช้
db = client["mydb"]

# เลือก collection ที่ต้องการ
collection = db["users"]

# ดึงข้อมูลทั้งหมดจาก collection "users"
all_users = collection.find()

# แสดงผลลัพธ์
# for user in all_users:
#     print(user)

# ดึงข้อมูลผู้ใช้ที่อายุมากกว่า 30 ปี
filtered_users = collection.find({"Age": {"$gt": 50}, "Email": {"$regex": "@gmail.com"}})

# แสดงผลลัพธ์
for user in filtered_users:
    print(user)







# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# from bson import ObjectId

# # สร้าง Flask app
# app = Flask(__name__)
# CORS(app)

# # เชื่อมต่อ MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["mydb"]  # ชื่อฐานข้อมูล
# users_collection = db["users"]  # ชื่อ collection

# # Helper function: แปลง ObjectId ให้เป็น string
# def serialize_user(user):
#     user["_id"] = str(user["_id"])
#     return user

# # Routes

# # 1. อ่านข้อมูลทั้งหมด (GET)
# @app.route("/api/users", methods=["GET"])
# def get_users():
#     users = list(users_collection.find())
#     return jsonify([serialize_user(user) for user in users]), 200

# # 2. เพิ่มข้อมูลใหม่ (POST)
# @app.route("/api/users", methods=["POST"])
# def create_user():
#     data = request.json
#     new_user = {
#         "name": data["name"],
#         "age": data["age"],
#         "email": data["email"]
#     }
#     result = users_collection.insert_one(new_user)
#     created_user = users_collection.find_one({"_id": result.inserted_id})
#     return jsonify(serialize_user(created_user)), 201

# # 3. แก้ไขข้อมูล (PUT)
# @app.route("/api/users/<id>", methods=["PUT"])
# def update_user(id):
#     data = request.json
#     updated_user = {
#         "name": data["name"],
#         "age": data["age"],
#         "email": data["email"]
#     }
#     users_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_user})
#     user = users_collection.find_one({"_id": ObjectId(id)})
#     return jsonify(serialize_user(user)), 200

# # 4. ลบข้อมูล (DELETE)
# @app.route("/api/users/<id>", methods=["DELETE"])
# def delete_user(id):
#     result = users_collection.delete_one({"_id": ObjectId(id)})
#     if result.deleted_count > 0:
#         return jsonify({"message": "User deleted successfully"}), 200
#     else:
#         return jsonify({"error": "User not found"}), 404

# # เริ่มเซิร์ฟเวอร์
# if __name__ == "__main__":
#     app.run(debug=True)
