import os
import cv2
from tqdm import tqdm # 顯示進度條

def crop_objects_from_yolo_dataset(data_root_dir, output_root_dir, class_mapping):
    """
    從 YOLOv5 格式的資料集中裁剪出物件圖片，並根據指定的類別合併邏輯進行分類。

    Args:
        data_root_dir (str): YOLOv5 資料集的根目錄 (例如：'./my_yolo_dataset')
                             此目錄下應包含 'train', 'val', 'test' 等子資料夾，
                             每個子資料夾內有 'images' 和 'labels'。
        output_root_dir (str): 裁剪後物件圖片的保存根目錄。
        class_mapping (dict): 定義 YOLO class_id 如何映射到輸出資料夾名稱的字典。
                              例如：{0: 'F', 1: 'Not_F', 2: 'Not_F'}
    """
    splits = ['train', 'valid', 'test'] # 根據您的資料集結構調整

    # 獲取所有唯一的輸出類別名稱
    output_class_names = sorted(list(set(class_mapping.values())))

    for split in splits:
        images_dir = os.path.join(data_root_dir, split, 'images')
        labels_dir = os.path.join(data_root_dir, split, 'labels')
        output_split_dir = os.path.join(output_root_dir, split)

        # 檢查路徑是否存在
        if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
            print(f"警告：找不到 '{split}' 資料夾下的 images 或 labels 目錄，跳過此分割。")
            continue

        # 為每個最終輸出類別創建輸出子資料夾
        for output_class_name in output_class_names:
            class_output_dir = os.path.join(output_split_dir, output_class_name)
            os.makedirs(class_output_dir, exist_ok=True)

        print(f"\n--- 開始處理 {split} 資料集 ---")
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

        for image_filename in tqdm(image_files, desc=f"裁剪 {split} 圖片"):
            image_path = os.path.join(images_dir, image_filename)
            # 假設標籤檔案名與圖片檔案名相同，只是副檔名是 .txt
            label_filename = os.path.splitext(image_filename)[0] + '.txt'
            label_path = os.path.join(labels_dir, label_filename)

            if not os.path.exists(label_path):
                # print(f"警告：圖片 '{image_filename}' 沒有對應的標籤檔案，跳過。")
                continue

            try:
                img = cv2.imread(image_path)
                if img is None:
                    print(f"警告：無法讀取圖片 '{image_path}'，跳過。")
                    continue

                img_h, img_w, _ = img.shape

                with open(label_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        parts = line.strip().split()
                        if len(parts) != 5:
                            print(f"警告：標籤檔案 '{label_path}' 第 {i+1} 行格式不正確，跳過。")
                            continue

                        original_class_id = int(parts[0])

                        # 根據映射字典獲取最終的輸出類別名稱
                        if original_class_id in class_mapping:
                            final_output_class_name = class_mapping[original_class_id]
                        else:
                            # 如果遇到沒有定義的 class_id，您可以選擇跳過，或把它歸到一個默認類別
                            print(f"警告：標籤檔案 '{label_path}' 第 {i+1} 行的 original_class_id {original_class_id} 未在 class_mapping 中定義，將其歸為 'Unknown'。")
                            final_output_class_name = 'Unknown' # 默認處理，您可以根據需求修改

                        # YOLO 格式是歸一化座標 (中心點x, 中心點y, 寬, 高)
                        x_center, y_center, bbox_w, bbox_h = map(float, parts[1:])

                        # 將歸一化座標轉換為像素座標
                        x1 = int((x_center - bbox_w / 2) * img_w)
                        y1 = int((y_center - bbox_h / 2) * img_h)
                        x2 = int((x_center + bbox_w / 2) * img_w)
                        y2 = int((y_center + bbox_h / 2) * img_h)

                        # 確保座標在圖片範圍內
                        x1 = max(0, x1)
                        y1 = max(0, y1)
                        x2 = min(img_w, x2)
                        y2 = min(img_h, y2)

                        # 裁剪物件
                        cropped_object = img[y1:y2, x1:x2]

                        if cropped_object.size == 0 or x2 <= x1 or y2 <= y1: # 確保裁剪區域有效
                            # print(f"警告：裁剪出空圖片，可能邊界框太小或座標有誤。檔案: {label_path}, 行: {i+1}")
                            continue

                        # 構建輸出檔案名 (原圖片名_物件索引_最終類別名.jpg)
                        output_class_dir = os.path.join(output_split_dir, final_output_class_name)
                        os.makedirs(output_class_dir, exist_ok=True) # 確保資料夾存在

                        output_filename = f"{os.path.splitext(image_filename)[0]}_{i:03d}_{final_output_class_name}.jpg"
                        output_path = os.path.join(output_class_dir, output_filename)

                        # 保存裁剪後的圖片
                        cv2.imwrite(output_path, cropped_object)

            except Exception as e:
                print(f"處理檔案 '{image_path}' 或標籤 '{label_path}' 時發生錯誤: {e}")

    print("\n--- 所有資料集分割處理完成！ ---")

# --- 使用範例 ---
if __name__ == "__main__":
    # 1. ***請修改這裡***：您的 YOLOv5 資料集根目錄
    yolov5_dataset_path = './yolov5dataset'

    # 2. ***請修改這裡***：裁剪後物件圖片的保存根目錄
    cropped_output_path = './prog'

    # 3. ***請修改這裡***：定義 YOLO class_id 如何映射到輸出資料夾名稱的字典。
    # 現在將 0 映射到 'F'，1 映射到 'S'，2 映射到 'V'。
    my_class_mapping = {
        0: 'F',
        1: 'S',
        2: 'V'
    }

    # --- 執行裁剪 ---
    crop_objects_from_yolo_dataset(yolov5_dataset_path, cropped_output_path, my_class_mapping)

    print(f"\n裁剪完成！物件圖片已保存到 '{cropped_output_path}'")
    print(f"現在您可以使用 '{cropped_output_path}' 作為 EfficientNetV2 的輸入資料。")