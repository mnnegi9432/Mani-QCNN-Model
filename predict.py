import torch
from PIL import Image
from torchvision import transforms

from model_loader import load_models

CLASS_NAMES = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary"
]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def predict_image(image_path):

    # Load models only when prediction is requested
    efficientnet, hybrid_model, scaler, pca, device = load_models()

    image = Image.open(image_path).convert("RGB")

    image = transform(image).unsqueeze(0).to(device)

    # EfficientNet Feature Extraction
    with torch.no_grad():
        features = efficientnet(image)

    features = features.cpu().numpy()

    # Standardization
    features = scaler.transform(features)

    # PCA Reduction
    features = pca.transform(features)

    features = torch.tensor(
        features,
        dtype=torch.float32
    ).to(device)

    # Hybrid QCNN Prediction
    with torch.no_grad():

        output = hybrid_model(features)

        probabilities = torch.softmax(output, dim=1)

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    return (
        CLASS_NAMES[prediction.item()],
        round(confidence.item() * 100, 2)
    )