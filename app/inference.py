import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import json, os

# --- Configuration ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = "./weights/mobilenet_v2_SmartPlant.pth"
CLASS_MAP_PATH = "./weights/class_mapping.json"
IMG_SIZE = 224

# --- Transforms ---
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

# --- Load model ---
def load_model():
    with open(CLASS_MAP_PATH, "r") as f:
        idx_to_class = json.load(f)
    num_classes = len(idx_to_class)

    model = models.mobilenet_v2(weights=None)
    in_feat = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(in_feat, num_classes)
    state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(state_dict, strict=False)
    model.eval().to(DEVICE)
    return model, idx_to_class

model, idx_to_class = load_model()

def predict_image(image_path: str):
    image = Image.open(image_path).convert("RGB")
    x = transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        logits = model(x)
        probs = F.softmax(logits, dim=1).squeeze(0)
        conf, pred = torch.max(probs, dim=0)
        species_name = idx_to_class[str(pred.item())] if isinstance(idx_to_class, dict) else idx_to_class[pred.item()]
    return species_name, float(conf.item())
