import os
import cv2
import numpy as np
from tqdm import tqdm
import random
import matplotlib.pyplot as plt

# Define paths
dataset_path = "../data_db2"
target_path = "dataset/custom.npy"
labels_path = "dataset/custom_labels.npy"
pairs_touch = "outputs/custom.txt"

# Function to load images from the dataset folder
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

# Initialize empty lists for pairs and labels
pairs = []
labels = []

# Load all images and store them in a dictionary by person name
all_images = {}
for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if os.path.isdir(person_folder):
        images = load_images_from_folder(person_folder)
        all_images[person_name] = images

# Create positive pairs
for person_name, images in all_images.items():
    if len(images) >= 3:
        selected_images = random.sample(images, 3)  # Randomly select 3 images
        for i in range(2):
            for j in range(i + 1, 3):
                pairs.append([selected_images[i], selected_images[j]])
                labels.append(1)  # Positive pair (same person)

# Create negative pairs
person_names = list(all_images.keys())
num_persons = len(person_names)
for i in range(num_persons):
    for j in range(i + 1, num_persons):
        if len(all_images[person_names[i]]) >= 1 and len(all_images[person_names[j]]) >= 1:
            img1 = random.choice(all_images[person_names[i]])  # Randomly select 1 image from person i
            img2 = random.choice(all_images[person_names[j]])  # Randomly select 1 image from person j
            pairs.append([img1, img2])
            labels.append(0)  # Negative pair (different persons)

# Convert lists to numpy arrays
pairs = np.array(pairs)
labels = np.array(labels)

# Save the pairs and labels arrays
np.save(target_path, pairs)
np.save(labels_path, labels)

print(f"Total pairs: {len(pairs)}")
print(f"Total labels: {len(labels)}")

for i in tqdm(range(0, 1000)):
    img1_target = f"lfwe/custom/{i}_1.jpg"
    img2_target = f"lfwe/custom/{i}_2.jpg"
    
    if os.path.exists(img1_target) != True:
        img1 = pairs[i][0]
        # plt.imsave(img1_target, img1/255) #works for my mac
        plt.imsave(img1_target, img1) #works for my debian
    
    if os.path.exists(img2_target) != True:
        img2 = pairs[i][1]
        # plt.imsave(img2_target, img2/255) #works for my mac
        plt.imsave(img2_target, img2) #works for my debian
    
if os.path.exists(pairs_touch) != True:
    open(pairs_touch,'a').close()