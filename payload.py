def flex_predict_blood_fat(reply_text, reply_text_color):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "ความเสี่ยงโรคไขมันในเลือด",
                    "size": "lg"
                    },
                    {
                    "type": "text",
                    "text": reply_text,
                    "color": reply_text_color,
                    "weight": "bold",
                    "size": "lg",
                    "offsetStart": "md"
                    }
                ],
                "margin": "md"
                }
            ],
            "margin": "none"
            }
        }
    }

    



def flex_analysis_data_blood_fat(Gender_status, Weight, Height, Cholesterol, Triglycerides, Hdl, Ldl, colors):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อมูลการวิเคราะห์", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "เพศ:"}, {"type": "text", "text": f"{Gender_status}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "น้ำหนัก:"}, {"type": "text", "text": f"{Weight}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ส่วนสูง:"}, {"type": "text", "text": f"{Height}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "คอเลสเตอรอล:"}, {"type": "text", "text": f"{Cholesterol}", "color": f"{colors['Cholesterol']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ไตรกลเซอไรด์:"}, {"type": "text", "text": f"{Triglycerides}", "color": f"{colors['Triglycerides']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ไขมันดี:"}, {"type": "text", "text": f"{Hdl}", "color": f"{colors['Hdl']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ไขมันไม่ดี:"}, {"type": "text", "text": f"{Ldl}", "color": f"{colors['Ldl']}","align": "end"}]}
                ]
            }
        }
    }

def flex_recommendations_blood_fat(recommendations):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อแนะนำ", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                ] + [{"type": "text", "text": rec, "wrap": True} for rec in recommendations]
            }
        }
    }

def generate_payload(user, reply_text, reply_text_color, Gender_status, Weight, Height, 
                     Cholesterol, Cholesterol_color, Triglycerides, Triglycerides_color, 
                     Hdl, Hdl_color, Ldl, Ldl_color, recommendations):
    return {
        "to": user,
        "messages": [
            {
                "type": "flex",
                "altText": "ข้อ",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "ความเสี่ยงโรคไขมันในเลือด", "size": "lg"},
                            {"type": "text", "text": f"  {reply_text}", "size": "xl", "color": f"{reply_text_color}"}
                        ]
                    }
                }
            },
            {
                "type": "flex",
                "altText": "Flex Message",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": "ข้อมูลการวิเคราะห์", "size": "lg", "weight": "bold"},
                            {"type": "separator"},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "เพศ:"},
                                {"type": "text", "text": f"{Gender_status}"}
                            ]},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "น้ำหนัก:"},
                                {"type": "text", "text": f"{Weight}"}
                            ]},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "ส่วนสูง"},
                                {"type": "text", "text": f"{Height}"}
                            ]},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "คอเลสเตอรอล:"},
                                {"type": "text", "text": f"{Cholesterol}", "color": f"{Cholesterol_color}"}
                            ]},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "ไตรกลเซอไรด์:"},
                                {"type": "text", "text": f"{Triglycerides}", "color": f"{Triglycerides_color}"}
                            ]},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "ความดันตัวบน:"},
                                {"type": "text", "text": f"{Hdl}", "color": f"{Hdl_color}"}
                            ]},
                            {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
                                {"type": "text", "text": "ความดันตัวล่าง:"},
                                {"type": "text", "text": f"{Ldl}", "color": f"{Ldl_color}"}
                            ]}
                        ]
                    }
                }
            },
            {
                "type": "flex",
                "altText": "Flex Message",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "คำแนะนำ", "size": "lg", "weight": "bold"},
                            {"type": "separator", "margin": "md"}
                        ] + [{"type": "text", "text": rec, "wrap": True} for rec in recommendations]
                    }
                }
            }
        ]
    }

def flex_predict_diabetes(reply_text, reply_text_color):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "ความเสี่ยงโรคเบาหวาน",
                    "size": "lg"
                    },
                    {
                    "type": "text",
                    "text": reply_text,
                    "color": reply_text_color,
                    "weight": "bold",
                    "size": "lg",
                    "offsetStart": "md"
                    }
                ],
                "margin": "md"
                }
            ],
            "margin": "none"
            }
        }
    }

def flex_analysis_data_diabetes(age, bmi, visceral, wc, ht_str, sbp, dbp, fbs, HbAlc, family_his_str, colors):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อมูลการวิเคราะห์", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "เพศ:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{age}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ดัชนีมวลกาย:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{bmi}", "color": f"{colors['bmi']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "Visceral Fat:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{visceral}", "color": f"{colors['visceral']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "รอบเอาต่อความสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{wc}", "color": f"{colors['wc']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "โรคความดันโลหิตสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{ht_str}", "color": f"{colors['ht']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงบน:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{sbp}", "color": f"{colors['sbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงล่าง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{dbp}", "color": f"{colors['dbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "น้ำตาลในเลือดก่อนอาหาร:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{fbs}", "color": f"{colors['fbs']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ระดับน้ำตาลสะสมนเลือด:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{HbAlc}", "color": f"{colors['HbAlc']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ประวัติเบาหวานในครอบครัว:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{family_his_str}", "color": f"{colors['family_his']}","align": "end"}]}
                ]
            }
        }
    }

def flex_recommendations_diabetes(recommendations):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ข้อแนะนำ", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                ] + [{"type": "text", "text": rec, "wrap": True} for rec in recommendations]
            }
        }
    }


def flex(key1):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ผลลัพธ์การเปรียบเทียบ", "size": "lg", "weight": "bold"},
                    {"type": "separator"},
                ] + 
                [{"type": "text", "text": f"{rec}aaa", "wrap": True} for rec in key1]
            }
        }
    }

def flex2(image_url):
    return {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit"
                }
            ]
            }
        }
    }



