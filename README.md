# 🧠 TwoStage-DefectSystem

本專案為結合 **YOLOv5s** 與 **EfficientNetV2-S** 的雙階段缺陷檢測系統，可應用於瑕疵檢測、自動分類等場景。

---

<h3>📌 系統流程圖</h3>
<p align="center">
  <img src="docs/ui/Process.png" alt="System Architecture" width="700px">
</p>

---

## 🎯 雙階段系統簡介

- 🔹 **第一階段 - YOLOv5s**
  - 對整張圖片進行快速物件偵測，找出缺陷候選區域
- 🔹 **第二階段 - EfficientNetV2s**
  - 對候選區域進行圖像分類，辨識缺陷類型

---

## 🧪 模型訓練流程（使用 Google Colab）

📂 [點我進入雲端資料夾](https://drive.google.com/drive/folders/1Id0aTjWZQ73lc_3HOMBqD-YMszYA39OG?usp=drive_link)  
內含訓練與推論的 `.ipynb` 筆記本檔案：

| Notebook 說明            | 路徑                                  |
| ------------------------ | ------------------------------------- |
| YOLOv5s 訓練流程         | `/程式/yolov5s.ipynb`                 |
| EfficientNetV2s 訓練流程 | `/程式/EfficientNetV2s.ipynb`         |
| 雙階段模型推論           | `/程式/yolov5s+EfficientNetV2s.ipynb` |

---

## 🔗 模型與結果下載連結（Google Drive）

請從雲端資料夾中下載以下模型與結果：

| 模型或資料           | 路徑                          |
| -------------------- | ----------------------------- |
| YOLOv5s 權重         | `/輸出/yolo 輸出/`            |
| EfficientNetV2s 權重 | `/輸出/EfficientNetV2s 輸出/` |
| 雙階段模型推論結果   | `/輸出/yolo+efficientnet/`    |

---

## 🖼️ 成果展示

### 📥 使用者介面示意

<p align="center">
  <img src="docs/ui/ui_demo.png" alt="Frontend UI" width="500px">
</p>

### ✅ 缺陷分類結果展示

<p align="center">
  <img src="docs/ui/prediction_result.jpg" alt="Prediction Result" width="700px">
</p>

---

## 📁 資料集格式說明

> 資料集皆存於 Google Drive，內含：

- 原始圖片
- YOLOv5 標註格式（`.txt`）
- Crop 後供 EfficientNet 分類使用的子圖

---

## 📄 授權 License

本專案採用 MIT License，如需商業應用請註明出處。

---

## ✉️ 聯絡方式

如需了解更多細節，歡迎聯絡開發者：

- **作者**：[你的名字]
- **Email**：[your_email@example.com]
