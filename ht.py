
import httpx
import asyncio
from flask import Flask, jsonify

app = Flask(__name__)


async def fetch_user_health():
    # URL ของ API
    url = "https://api.myhealthgroup.net/apiservice/line/getUserHealth"

    # Header
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 32a9fcf38fb1aebaed"
    }
    
    # ข้อมูลที่ส่งใน body
    data = {
        "userId":"user1645ac833f9e753ea4698578c6ec2cdb"
    }

    # ใช้ AsyncClient สำหรับการทำงานแบบ async
    async with httpx.AsyncClient() as client:
        try:
            # ส่งคำขอ POST แบบ async
            response = await client.post(url, headers=headers, json=data)

            # ตรวจสอบผลลัพธ์
            if response.status_code == 200:
                result = response.json()
                healthdata = result.get("payload", [{}])[0].get("healthdata", [{}[0]])
                
                print(f"ข้อมูลสำหรับ : {result}")
                return result
            else:
                print(f"ข้อผิดพลาดสำหรับ : รหัส {response.status_code}, {response.text}")

        except httpx.HTTPStatusError as e:
            print(f"เกิดข้อผิดพลาด HTTP สำหรับ : {e}")
        except httpx.RequestError as e:
            print(f"เกิดข้อผิดพลาดการเชื่อมต่อสำหรับ : {e}")
            
@app.route('/api/health', methods=['GET'])
def get_health():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_user_health())
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
