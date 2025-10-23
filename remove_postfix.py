import os

# Path to your dataset root
DATASET_DIR = "tool_dataset"

# Subfolders to process
SUBFOLDERS = ["train", "valid", "test"]

def remove_mask_suffix():
    for subset in SUBFOLDERS:
        mask_folder = os.path.join(DATASET_DIR, subset, "masks")

        if not os.path.exists(mask_folder):
            print(f"Skipping missing folder: {mask_folder}")
            continue

        for filename in os.listdir(mask_folder):
            if "_mask" in filename:
                old_path = os.path.join(mask_folder, filename)
                new_filename = filename.replace("_mask", "")
                new_path = os.path.join(mask_folder, new_filename)

                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_filename}")

if __name__ == "__main__":
    remove_mask_suffix()
    print("✅ Done! All '_mask' suffixes removed.")
