from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np

app = FastAPI()

# 定义接收图片的接口
@app.post("/analyze")
async def analyze_screen(file: UploadFile = File(...)):
    # 1. 接收快捷指令传来的图片数据
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # ==========================================
    # 2. 在这里接入你之前的 OpenCV 认牌和计算代码
    # hand_tiles = recognize_tiles(img)
    # best_discard, ukeire = calculate_best_discard(hand_tiles)
    # ==========================================

    # 3. 假设经过你的算法，得出了结果（这里用假数据演示）
    best_discard = "3万"
    details = "进张 12 张 (4,5,6万)"

    # 4. 将结果以 JSON 格式返回给手机
    return {
        "status": "success",
        "title": f"🥇 推荐打出: 【{best_discard}】",
        "body": details
    }
