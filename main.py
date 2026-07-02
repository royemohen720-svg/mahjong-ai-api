from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import os

app = FastAPI()

# 自动加载仓库根目录下的所有 .PNG 图片作为模板
templates = {}
for file in os.listdir("."):
    if file.endswith(".PNG"):  # 已修改为大写匹配
        # 读取图片，转为灰度图
        templates[file.replace(".PNG", "")] = cv2.imread(file, 0)

@app.post("/analyze")
async def analyze_screen(file: UploadFile = File(...)):
    # 1. 解码上传的截图
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"status": "error", "title": "图片读取失败", "body": "请检查上传图片"}
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 核心识别逻辑：循环匹配所有模板
    results = []
    # 设置匹配阈值 (0.8 代表80%相似度)
    threshold = 0.8
    
    for name, template in templates.items():
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val >= threshold:
            results.append(name)
            
    # 3. 返回结果
    if not results:
        return {"status": "success", "title": "未识别到牌", "body": "请确保截图包含手牌"}
    
    return {
        "status": "success",
        "title": "🥇 识别结果: " + ",".join(results[:14]),
        "body": f"共识别到 {len(results)} 张牌"
    }
