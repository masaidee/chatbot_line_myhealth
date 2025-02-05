#เช็คโรคไขมันในเลือด
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


#เช็คโรคเบาหวาน
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



#เช็คโรคเบาหวาน
def flex_predict_Staggers(reply_text, reply_text_color):
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

def flex_analysis_data_Staggers(sbp, dbp, his_str, smoke_str, fbs, HbAlc, total_Cholesterol, Exe, bmi, family_his_str, colors):
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
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "เพศ:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{sbp}", "color": f"{colors['sbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ดัชนีมวลกาย:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{dbp}", "color": f"{colors['dbp']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "Visceral Fat:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{his_str}", "color": f"{colors['his']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "รอบเอาต่อความสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{smoke_str}", "color": f"{colors['smoke']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "โรคความดันโลหิตสูง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{fbs}", "color": f"{colors['fbs']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงบน:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{HbAlc}", "color": f"{colors['HbAlc']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ความดันโลหิตช่วงล่าง:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{total_Cholesterol}", "color": f"{colors['total_Cholesterol']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "น้ำตาลในเลือดก่อนอาหาร:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{Exe}", "color": f"{colors['Exe']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ระดับน้ำตาลสะสมนเลือด:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{bmi}", "color": f"{colors['bmi']}","align": "end"}]},
                    {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": "ประวัติเบาหวานในครอบครัว:", "wrap": True, "flex": 3}, {"type": "text", "text": f"{family_his_str}", "color": f"{colors['family_his']}","align": "end"}]}
                ]
            }
        }
    }

def flex_recommendations_Staggers(recommendations):
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


#เปรียบเทียบข้อมูล
def compare(key1, diff1, avg1):
    key_contents = [
        {
            "type": "text",
            "text": forkey,
            "size": "sm",
            "color": "#555555",
            "flex": 0
        } for forkey in key1
    ]

    diff_contents = [
        {
            "type": "text",
            "text": str(fordiff[0]),
            "size": "sm",
            "color": fordiff[1],  # ใช้ข้อมูลสี
            "flex": 0,
            "wrap": True
        } for fordiff in diff1
    ]

    avg_contents = [
        {
            "type": "text",
            "text": foravg,
            "size": "sm",
            "color": "#555555",
            "flex": 0,
            "wrap": True
        } for foravg in avg1
    ]

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
                        "type": "text",
                        "text": "ผลการเปรียบเทียบ",
                        "weight": "bold",
                        "size": "lg",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": key_contents,
                                "height": "100%",
                                "width": "100px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": diff_contents,
                                "height": "100%",
                                "width": "50px",
                                "spacing": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": avg_contents,
                                "height": "100%",
                                "width": "100%",
                                "spacing": "sm"

                            }
                        ]
                    }
                ]
            },
            "styles": {
                "footer": {
                    "separator": True
                }
            }
        }
    }
    
    
    # {
    #     "type": "flex",
    #     "altText": "Flex Message",
    #     "contents": {
    #         "type": "bubble",
    #         "body": {
    #             "type": "box",
    #             "layout": "vertical",
    #             "contents": [
    #                 {"type": "text", "text": "ผลลัพธ์การเปรียบเทียบ", "size": "lg", "weight": "bold"},
    #                 {"type": "separator"},
    #             ] + 
    #             [{"type": "text", "text": f"{rec}aaa", "wrap": True} for rec in key1]
    #         }
    #     }
    # }

def compare_img(image_url):
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

def payloadinsertData(URL_add_user_form, URL_add_diabetes_form, URL_add_blood_fat_form, URL_add_staggers_form ):
    return {
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "carousel",
    "contents": [
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://tse3.mm.bing.net/th?id=OIP.yyb_fEnU90jvsagWV0iy1gHaHa&pid=Api&P=0&h=180",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "ข้อมูลส่วนตัว",
              "weight": "bold",
              "size": "xl",
              "contents": []
            }
          ],
          "alignItems": "center"
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "uri": URL_add_user_form,
                "label": "เพิ่มข้อมูล"
              },
              "style": "primary"
            }
          ]
        }
      },
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://tse2.mm.bing.net/th?id=OIP.iQkrJy3wolMxKYESs4UO-gHaDq&pid=Api&P=0&h=180",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "โรคเบาหวาน",
              "weight": "bold",
              "size": "xl",
              "contents": []
            }
          ],
          "alignItems": "center"
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "uri": URL_add_diabetes_form,
                "label": "เพิ่มข้อมูล"
              },
              "style": "primary"
            }
          ]
        }
      },
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://tse4.mm.bing.net/th?id=OIP.PW8FqeDmyXK1qpGgv-sLUgHaEK&pid=Api&P=0&h=180",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "โรคไขมันในเลือด",
              "weight": "bold",
              "size": "xl",
              "contents": []
            }
          ],
          "alignItems": "center"
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "uri": URL_add_blood_fat_form,
                "label": "เพิ่มข้อมูล"
              },
              "style": "primary"
            }
          ]
        }
      },
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://tse3.mm.bing.net/th?id=OIP.mYZOsolcq794sn847AQjlAHaHa&pid=Api&P=0&h=180",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "โรคสมอง",
              "weight": "bold",
              "size": "xl",
              "contents": []
            }
          ],
          "alignItems": "center"
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "action",
                "uri": URL_add_staggers_form
              },
              "style": "primary"
            }
          ]
        }
      }
    ]
  }
}

