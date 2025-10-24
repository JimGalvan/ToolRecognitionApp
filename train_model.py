from fastai.vision.all import *
from pathlib import Path
import json
from PIL import Image
import numpy as np
import multiprocessing


def label_func(fn):
    return path / 'masks' / f'{fn.stem}.png'


def prepare_masks_and_train():
    global path  # so label_func sees it
    path = Path('tool_dataset/train')
    mask_dir = path / 'masks'
    ann_path = path / '_annotations.coco.json'

    # === Load COCO annotations ===
    with open(ann_path) as f:
        coco = json.load(f)

    # Build ID → consecutive index mapping
    id2idx = {cat['id']: i + 1 for i, cat in enumerate(coco['categories'])}
    codes = ['background'] + [cat['name'] for cat in coco['categories']]
    print("COCO id → index mapping:", id2idx)
    print("Class codes:", codes)

    # === Remap all masks ===
    for mask_path in mask_dir.glob("*.png"):
        mask = np.array(Image.open(mask_path))
        remapped = np.zeros_like(mask, dtype=np.uint8)
        for coco_id, idx in id2idx.items():
            remapped[mask == coco_id] = idx
        Image.fromarray(remapped).save(mask_path)

    # === GPU Check ===
    print(torch.cuda.is_available())
    if torch.cuda.is_available():
        print(torch.cuda.get_device_name(0))

    # === Dataset ===
    fnames = get_image_files(path)
    print(f"Found {len(fnames)} training images")

    # === Sanity check ===
    sample_mask_path = label_func(fnames[0])
    mask = np.array(Image.open(sample_mask_path))
    print("Mask shape:", mask.shape)
    print("Mask dtype:", mask.dtype)
    print("Unique values:", np.unique(mask)[:20])

    # === DataLoaders ===
    dls = SegmentationDataLoaders.from_label_func(
        path,
        bs=8,
        fnames=fnames,
        label_func=label_func,
        codes=codes,
        item_tfms=Resize(256),
        batch_tfms=[],
        num_workers=0  # avoids multiprocessing startup issue
    )

    # === Model & Training ===
    learn = unet_learner(dls, resnet50, metrics=Dice(), pretrained=True)
    learn.fine_tune(6)
    learn.export('modelv3.pkl')


if __name__ == "__main__":
    multiprocessing.freeze_support()  # <-- Required for Windows
    prepare_masks_and_train()
