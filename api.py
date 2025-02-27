from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/healthdata', methods=['GET'])
def get_healthdata():
    url = "https://api.myhealthgroup.net/apiservice/line/getUserHealth"

    payload = json.dumps({
        "userId": "user1645ac833f9e753ea4698578c6ec2cdb",
        "payload": [],
        "clinicdate": {}
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 32a9fcf38fb1aebaed',
        'Cookie': 'PHPSESSID=b1hhj1jba4j17gi8krb9o0qnka'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            payload = data.get("payload", [])
            
            if payload:
                healthdata = payload[0].get("healthdata", {})
                clinicdate = payload[0].get("clinicdate", {})
                sbp1_value = healthdata[0].get("sbp1", {}).get("value")
                return jsonify({f"healthdata": healthdata})
            else:
                return jsonify({"error": "No payload data found."}), 404
        else:
            return jsonify({"error": "Response not OK."}), 400
    else:
        return jsonify({"error": f"Error: {response.status_code}, {response.text}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)