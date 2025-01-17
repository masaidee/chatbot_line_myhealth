# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score

# # ข้อมูลตัวอย่างที่มีผู้ป่วยหลายคนและการเยี่ยมชมหลายครั้ง
# data = {
#     'PatientID': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
#     'VisitDate': ['2022-01-01', '2023-01-01', '2022-02-15', '2023-02-15', '2022-03-10', '2023-03-10', '2022-04-05', '2023-04-05', '2022-05-20', '2023-05-20'],
#     'อายุ': [30, 31, 45, 46, 50, 51, 40, 41, 35, 36],
#     'เพศ': [0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
#     'BMI': [25, 26, 30, 31, 28, 29, 22, 23, 27, 28],
#     'น้ำตาลในเลือด': [120, 125, 180, 185, 150, 155, 110, 115, 140, 145],
#     'ประวัติครอบครัว': [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
#     'เบาหวาน': [0, 0, 1, 1, 0, 0, 0, 0, 1, 1]
# }

# df = pd.DataFrame(data)
# df['VisitDate'] = pd.to_datetime(df['VisitDate'])
# df.sort_values(by=['PatientID', 'VisitDate'], inplace=True)

# # แยกคุณลักษณะและตัวแปรเป้าหมาย
# X = df[['อายุ', 'เพศ', 'BMI', 'น้ำตาลในเลือด', 'ประวัติครอบครัว']]
# y = df['เบาหวาน']

# # แบ่งข้อมูลเป็นชุดฝึกอบรมและชุดทดสอบ
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # การปรับขนาดคุณลักษณะ
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# # ฝึกโมเดล Logistic Regression
# model = LogisticRegression()
# model.fit(X_train_scaled, y_train)

# # ฟังก์ชันเพื่อทำนายความน่าจะเป็นในการเป็นเบาหวานสำหรับผู้ป่วยหลายคน
# def predict_diabetes_likelihood(patient_data_list):
#     # ดึงคุณลักษณะสำหรับการทำนาย
#     features = [patient['features'] for patient in patient_data_list]
#     patients_df = pd.DataFrame(features)
    
#     # ดึงตัวระบุ
#     identifiers = [{'PatientID': patient['PatientID'], 'VisitDate': patient['VisitDate']} for patient in patient_data_list]
    
#     # ปรับขนาดข้อมูลผู้ป่วย
#     patients_scaled = scaler.transform(patients_df)
    
#     # ทำนายความน่าจะเป็น
#     probabilities = model.predict_proba(patients_scaled)[:, 1]
    
#     # คำนวณค่า z-scores
#     z_scores = (patients_df - X.mean()) / X.std()
    
#     # พิมพ์ค่า z-scores และความน่าจะเป็น
#     for i in range(len(patient_data_list)):
#         print("Patient:", identifiers[i]['PatientID'])
#         print("VisitDate:", identifiers[i]['VisitDate'])
#         print("Z-scores เมื่อเทียบกับข้อมูลในอดีต:")
#         print(z_scores.iloc[i])
#         print(f"ความน่าจะเป็นในการพัฒนาระบบเบาหวานใน 3 ปีข้างหน้า: {probabilities[i]:.2%}")
#         print("a")
    
#     # ส่งคืน DataFrame ที่มีผลลัพธ์
#     results = pd.DataFrame(identifiers)
#     results['Probability'] = probabilities
#     return results

# # ตัวอย่างการใช้งานกับผู้ป่วยหลายคน
# patient_data_list = [
#     {
#         'PatientID': 1,
#         'VisitDate': '2023-01-01',
#         'features': {
#             'อายุ': 31,
#             'เพศ': 0,
#             'BMI': 26,
#             'น้ำตาลในเลือด': 125,
#             'ประวัติครอบครัว': 0
#         }
#     },
#     {
#         'PatientID': 1,
#         'VisitDate': '2023-02-15',
#         'features': {
#             'อายุ': 46,
#             'เพศ': 1,
#             'BMI': 31,
#             'น้ำตาลในเลือด': 185,
#             'ประวัติครอบครัว': 1
#         }
#     },
#     # เพิ่มผู้ป่วยเพิ่มเติมตามต้องการ
# ]

# # ทำนายและวิเคราะห์
# results_df = predict_diabetes_likelihood(patient_data_list)
# print(f"aa{results_df}")

