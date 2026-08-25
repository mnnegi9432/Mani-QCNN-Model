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

    efficientnet, hybrid_model, scaler, pca, device = load_models()

    efficientnet.eval()
    hybrid_model.eval()

    image = Image.open(image_path).convert("RGB")

    image = transform(image).unsqueeze(0).to(device)

    # EfficientNet
    with torch.inference_mode():

        features = efficientnet(image)

        features = features.cpu().numpy()

    # StandardScaler
    features = scaler.transform(features)

    # PCA
    features = pca.transform(features)

    # Convert back to PyTorch
    features = torch.from_numpy(
        features
    ).to(
        device=device,
        dtype=torch.float32
    )

    # Hybrid QCNN
    with torch.inference_mode():

        output = hybrid_model(features)

        probabilities = torch.softmax(
            output,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    return (
        CLASS_NAMES[prediction.item()],
        round(
            confidence.item() * 100,
            2
        )
    )
