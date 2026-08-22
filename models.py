import torch
import torch.nn as nn
import pennylane as qml

# =====================================
# Quantum Configuration
# =====================================

NUM_QUBITS = 8
NUM_LAYERS = 4 

dev = qml.device("default.qubit", wires=NUM_QUBITS)

# =====================================
# Quantum Circuit
# =====================================

@qml.qnode(
    dev,
    interface="torch",
    diff_method="backprop"
)
def quantum_circuit(inputs, weights):

    # Angle Encoding
    for i in range(NUM_QUBITS):
        qml.RY(inputs[i], wires=i)

    # Variational Layers
    for l in range(NUM_LAYERS):

        for i in range(NUM_QUBITS):
            qml.RY(weights[l, i, 0], wires=i)
            qml.RZ(weights[l, i, 1], wires=i)

        # Ring Entanglement
        for i in range(NUM_QUBITS):
            qml.CNOT(wires=[i, (i + 1) % NUM_QUBITS])

    return [
        qml.expval(qml.PauliZ(i))
        for i in range(NUM_QUBITS)
    ]


# =====================================
# Quantum Layer
# =====================================

weight_shapes = {
    "weights": (NUM_LAYERS, NUM_QUBITS, 2)
}

quantum_layer = qml.qnn.TorchLayer(
    quantum_circuit,
    weight_shapes
)


# =====================================
# Hybrid QCNN
# =====================================

class HybridQCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.embedding = nn.Sequential(
            nn.Linear(16, 8),
            nn.ReLU()
        )

        self.quantum = quantum_layer

        self.classifier = nn.Sequential(
            nn.Linear(8, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 4)
        )

    def forward(self, x):

        x = self.embedding(x)

        outputs = []

        for sample in x:
            outputs.append(self.quantum(sample))

        x = torch.stack(outputs)

        return self.classifier(x)