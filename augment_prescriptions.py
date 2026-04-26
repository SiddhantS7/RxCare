import cv2
import numpy as np
import os
from pathlib import Path
import random


INPUT_DIR = "data/raw_prescriptions"
OUTPUT_DIR = "data/augmented_prescriptions"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def random_brightness_contrast(image):
    alpha = random.uniform(0.9, 1.2)  # contrast
    beta = random.randint(-20, 20)    # brightness
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def random_rotation(image):
    angle = random.uniform(-5, 5)
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)


def add_shadow(image):
    h, w = image.shape[:2]
    shadow = np.zeros_like(image, dtype=np.uint8)

    x1, y1 = random.randint(0, w//2), 0
    x2, y2 = random.randint(w//2, w), h

    cv2.rectangle(shadow, (x1, y1), (x2, y2), (50, 50, 50), -1)

    alpha = random.uniform(0.2, 0.5)
    return cv2.addWeighted(image, 1 - alpha, shadow, alpha, 0)


def add_noise(image):
    noise = np.random.normal(0, 10, image.shape).astype(np.uint8)
    return cv2.add(image, noise)


def slight_blur(image):
    if random.random() > 0.5:
        return cv2.GaussianBlur(image, (3, 3), 0)
    return image


def process_image(image_path, output_path, idx):
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"Skipping {image_path}")
        return

    # Apply transformations
    image = random_rotation(image)
    image = random_brightness_contrast(image)

    if random.random() > 0.5:
        image = add_shadow(image)

    if random.random() > 0.5:
        image = slight_blur(image)

    if random.random() > 0.5:
        image = add_noise(image)

    filename = output_path / f"{image_path.stem}_aug_{idx}.jpg"
    cv2.imwrite(str(filename), image)


def augment_dataset(num_variations=3):
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)

    for img_file in input_path.glob("*"):
        for i in range(num_variations):
            process_image(img_file, output_path, i)

    print("✅ Augmentation complete!")


if __name__ == "__main__":
    augment_dataset(num_variations=5)