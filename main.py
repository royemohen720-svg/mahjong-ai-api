from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import os

app = FastAPI()

# 自动加载仓库根目录下的所有 .png 图片作为模板
templates = {}
for file in os.listdir("."):
    if file.endswith(".png"):
        # 读取图片，转为灰度图
        templates[file.replace(".png", "")] = cv2.imread(file, 0)

@app.post("/analyze")
async def analyze_screen(file: UploadFile = File(...)):
    # 1. 解码上传的截图
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 核心识别逻辑：在这里循环匹配所有模板
    results = []
    # 这里是一个简单的匹配演示，实际项目中会对截图区域进行切片匹配
    for name, template in templates.items():
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8:  # 匹配度阈值，大于 80% 认为识别到了
            results.append(name)
            
    return {
        "status": "success",
        "title": "🥇 识别结果: " + ",".join(results[:14]), # 只取前14张牌
        "body": "已自动对比你的真牌库"
    }
