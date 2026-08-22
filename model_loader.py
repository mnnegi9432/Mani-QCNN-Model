import torch
import joblib
import torch.nn as nn
from torchvision.models import efficientnet_b0
from models import HybridQCNN

# ======================================
# Device
# ======================================

device = torch.device("cpu")

# Global variables (Lazy Loading)
efficientnet = None
hybrid_model = None
scaler = None
pca = None


def load_models():
    global efficientnet, hybrid_model, scaler, pca

    # -----------------------------
    # EfficientNet
    # -----------------------------
    if efficientnet is None:

        efficientnet = efficientnet_b0(weights=None)
        efficientnet.classifier = nn.Identity()

        checkpoint = torch.load(
            "best_efficientnet.pth",
            map_location=device
        )

        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
        else:
            state_dict = checkpoint

        state_dict = {
            k: v
            for k, v in state_dict.items()
            if not k.startswith("classifier")
        }

        efficientnet.load_state_dict(
            state_dict,
            strict=False
        )

        efficientnet.to(device)
        efficientnet.eval()

    # -----------------------------
    # Hybrid QCNN
    # -----------------------------
    if hybrid_model is None:

        hybrid_model = HybridQCNN()

        checkpoint = torch.load(
            "best_hybrid_qcnn.pth",
            map_location=device
        )

        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:

            hybrid_model.load_state_dict(
                checkpoint["model_state_dict"],
                strict=False
            )

        else:

            hybrid_model.load_state_dict(
                checkpoint,
                strict=False
            )

        hybrid_model.to(device)
        hybrid_model.eval()

    # -----------------------------
    # Scaler
    # -----------------------------
    if scaler is None:
        scaler = joblib.load("standard_scaler.pkl")

    # -----------------------------
    # PCA
    # -----------------------------
    if pca is None:
        pca = joblib.load("pca16.pkl")

    return efficientnet, hybrid_model, scaler, pca, device