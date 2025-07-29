# TwoStage-DefectSystem

本專案為結合 YOLOv5 與 EfficientNetV2-S 的雙階段缺陷檢測系統。

系統架構圖如下：

<img src="docs/ui/Process.png" alt="System Architecture" width="600px">

## 🎯 雙階段架構簡介

- **第一階段（YOLOv5s）**：快速偵測目標區域
- **第二階段（EfficientNetV2s）**：針對每個區域進行分類辨識

## 🧪 模型訓練流程（Google Colab）

- [YOLOv5 訓練筆記本](ai_model/notebooks/yolov5_training.ipynb)
- [EfficientNetV2 訓練筆記本](ai_model/notebooks/effnetv2_training.ipynb)
- [雙階段推論流程](ai_model/notebooks/dual_inference.ipynb)

## 🔗 模型下載（Google Drive）

```bash
!gdown --id YOLO_FILE_ID
!gdown --id EFFNET_FILE_ID
```
