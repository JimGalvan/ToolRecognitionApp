import os
import json
import numpy as np
from PIL import Image
from pycocotools.coco import COCO
from pycocotools import mask as maskUtils

def coco_to_masks(coco_json_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    coco = COCO(coco_json_path)

    for img_info in coco.dataset['images']:
        img_id = img_info['id']
        file_name = img_info['file_name']
        height, width = img_info['height'], img_info['width']

        mask = np.zeros((height, width), dtype=np.uint8)

        ann_ids = coco.getAnnIds(imgIds=[img_id])
        anns = coco.loadAnns(ann_ids)

        for ann in anns:
            if 'segmentation' in ann:
                rle = coco.annToRLE(ann)
                m = maskUtils.decode(rle)
                mask[m > 0] = ann['category_id']

        mask_img = Image.fromarray(mask)
        mask_name = os.path.splitext(file_name)[0] + "_mask.png"
        mask_img.save(os.path.join(output_dir, mask_name))

        print(f"Saved mask for {file_name}")

if __name__ == "__main__":
    base_path = "tool_dataset"
    splits = ["train", "valid", "test"]

    for split in splits:
        coco_json = os.path.join(base_path, split, "_annotations.coco.json")
        if os.path.exists(coco_json):
            output_dir = os.path.join(base_path, split, "masks")
            coco_to_masks(coco_json, output_dir)
