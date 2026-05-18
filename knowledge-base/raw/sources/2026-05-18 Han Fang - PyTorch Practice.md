---
type: raw-source
source_id: src-2026-05-18-hanfang-pytorch-practice
title: "PyTorch Practice - Learning Tutorial and Interview Prep"
author: Han Fang
url: https://github.com/hanfang/pytorch-practice
captured: 2026-05-18
tags:
  - pytorch
  - machine-learning
  - deep-learning
  - interview-prep
  - tutorials
---

# PyTorch Practice - Complete Source

Consolidated markdown capture of all Python tutorial files from [hanfang/pytorch-practice](https://github.com/hanfang/pytorch-practice).

---

## README.md

# PyTorch Learning Tutorial

A comprehensive PyTorch tutorial designed for learning and interview preparation.

## Overview

This tutorial covers PyTorch fundamentals through advanced topics commonly asked in machine learning engineer interviews.

## Tutorial Structure

### Part 1: Tensor Basics (`01_tensor_basics.py`)
- Creating and manipulating tensors
- Basic operations and broadcasting
- Indexing and slicing
- NumPy integration
- GPU operations
- Essential tensor operations for interviews

### Part 2: Autograd and Gradients (`02_autograd_gradients.py`)
- Automatic differentiation
- Gradient computation
- Higher-order gradients
- Gradient flow control
- Custom gradient functions
- Common gradient scenarios in interviews

### Part 3: Neural Networks (`03_neural_networks.py`)
- Building neural networks with `nn.Module`
- Activation functions and loss functions
- Training loops and optimization
- Model saving/loading
- Regularization techniques (Dropout, BatchNorm)
- Complete XOR problem implementation

### Part 4: Interview Problems (`04_interview_problems.py`)
- Softmax implementation from scratch
- Custom Dataset and DataLoader
- Batch Normalization implementation
- Learning rate scheduling
- Gradient clipping
- Multi-GPU training setup
- Custom loss functions
- Weight initialization strategies
- Memory optimization techniques
- Model ensembles

### Part 5: Advanced Topics (`05_advanced_topics.py`)
- Custom optimizers
- Attention mechanisms (Multi-Head Attention)
- Residual connections and Layer Normalization
- Learning rate warmup and cosine annealing
- Mixed precision training
- Model profiling and debugging
- Dynamic computation graphs
- Model quantization
- Best practices summary

## Quick Start

### Option 1: Run Individual Parts
```bash
python 01_tensor_basics.py
python 02_autograd_gradients.py
python 03_neural_networks.py
python 04_interview_problems.py
python 05_advanced_topics.py
```

### Option 2: Use the Tutorial Runner
```bash
python run_tutorial.py
```

The runner provides an interactive menu to:
- Run all tutorials sequentially
- Run individual tutorial parts

## Requirements

```bash
pip install torch torchvision numpy matplotlib
```

For CUDA support (optional):
```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Interview Preparation Focus

This tutorial emphasizes concepts frequently tested in ML engineering interviews:

**Fundamental Concepts:**
- Tensor operations and broadcasting
- Gradient computation and backpropagation
- Neural network architecture design

**Implementation Skills:**
- Custom layers and loss functions
- Training loops and optimization
- Data loading and preprocessing

**Advanced Topics:**
- Attention mechanisms
- Mixed precision training
- Model optimization and quantization
- Memory management

**Best Practices:**
- Code organization with `nn.Module`
- Proper gradient handling
- Efficient data loading
- Model evaluation patterns

## Key Learning Outcomes

After completing this tutorial, you should be able to:

1. **Manipulate tensors** efficiently and understand broadcasting
2. **Implement neural networks** from scratch using PyTorch primitives
3. **Debug gradient flow** and understand autograd mechanics
4. **Optimize training** with proper learning rate scheduling and regularization
5. **Handle advanced scenarios** like multi-GPU training and mixed precision
6. **Answer common interview questions** with practical implementations

## Tips for Interview Success

1. **Practice implementations**: Don't just read the code—type it out and experiment
2. **Understand the math**: Know why operations work, not just how to use them
3. **Optimize for readability**: In interviews, clean code is as important as correct code
4. **Know the trade-offs**: Be prepared to discuss memory vs. speed, accuracy vs. efficiency
5. **Stay current**: PyTorch evolves rapidly; be aware of newer features and best practices

## Common Interview Topics Covered

- ✅ Tensor operations and broadcasting rules
- ✅ Gradient computation and backpropagation
- ✅ Custom loss functions and optimizers
- ✅ Batch normalization and layer normalization
- ✅ Attention mechanisms and transformers
- ✅ Model quantization and optimization
- ✅ Multi-GPU training strategies
- ✅ Memory optimization techniques
- ✅ Debugging and profiling models

## Next Steps

After mastering these concepts:
1. Implement larger projects (image classification, NLP tasks)
2. Study specific architectures (ResNet, Transformer, etc.)
3. Practice on real datasets (ImageNet, GLUE, etc.)
4. Contribute to open-source PyTorch projects
5. Stay updated with PyTorch documentation and releases

---

*This tutorial is designed to provide a solid foundation for both learning PyTorch and succeeding in machine learning engineer interviews.*
---

## 01_tensor_basics.py

```python
"""
PyTorch Tutorial - Part 1: Tensor Basics
Essential tensor operations for PyTorch interviews
"""

import torch
import numpy as np

print("=== PyTorch Tensor Basics ===")

# 1. Creating tensors
print("\n1. Creating Tensors:")
tensor_from_data = torch.tensor([1, 2, 3, 4])
print(f"From list: {tensor_from_data}")

tensor_zeros = torch.zeros(2, 3)
print(f"Zeros tensor:\n{tensor_zeros}")

tensor_ones = torch.ones(2, 3)
print(f"Ones tensor:\n{tensor_ones}")

tensor_random = torch.rand(2, 3)
print(f"Random tensor:\n{tensor_random}")

tensor_randn = torch.randn(2, 3)  # Normal distribution
print(f"Normal random tensor:\n{tensor_randn}")

# 2. Tensor properties
print("\n2. Tensor Properties:")
x = torch.randn(3, 4, 5)
print(f"Shape: {x.shape}")
print(f"Size: {x.size()}")
print(f"Data type: {x.dtype}")
print(f"Device: {x.device}")
print(f"Number of dimensions: {x.dim()}")
print(f"Number of elements: {x.numel()}")

# 3. Basic operations
print("\n3. Basic Operations:")
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

print(f"a: {a}")
print(f"b: {b}")
print(f"Addition: {a + b}")
print(f"Element-wise multiplication: {a * b}")
print(f"Matrix multiplication: {torch.dot(a, b)}")

# 4. Reshaping tensors
print("\n4. Reshaping Tensors:")
x = torch.randn(12)
print(f"Original shape: {x.shape}")

reshaped = x.view(3, 4)
print(f"Reshaped (3,4):\n{reshaped}")

reshaped2 = x.view(-1, 2)  # -1 means infer this dimension
print(f"Reshaped (-1,2):\n{reshaped2}")

# 5. Indexing and slicing
print("\n5. Indexing and Slicing:")
x = torch.randn(3, 4)
print(f"Original tensor:\n{x}")
print(f"First row: {x[0]}")
print(f"First column: {x[:, 0]}")
print(f"Element at (1,2): {x[1, 2]}")
print(f"Last 2 rows, last 2 cols:\n{x[-2:, -2:]}")

# 6. Common tensor operations for interviews
print("\n6. Common Interview Operations:")

# Broadcasting
a = torch.tensor([[1], [2], [3]])  # 3x1
b = torch.tensor([10, 20, 30])     # 1x3
result = a + b  # Broadcasting to 3x3
print(f"Broadcasting example:\n{result}")

# Concatenation
x = torch.tensor([[1, 2], [3, 4]])
y = torch.tensor([[5, 6], [7, 8]])
concat_dim0 = torch.cat([x, y], dim=0)  # Along rows
concat_dim1 = torch.cat([x, y], dim=1)  # Along columns
print(f"Concatenate along dim=0:\n{concat_dim0}")
print(f"Concatenate along dim=1:\n{concat_dim1}")

# Stacking
stack_dim0 = torch.stack([x, y], dim=0)  # New dimension at index 0
print(f"Stack along dim=0 shape: {stack_dim0.shape}")
print(f"Stack along dim=0:\n{stack_dim0}")

# 7. Converting between NumPy and PyTorch
print("\n7. NumPy <-> PyTorch Conversion:")
numpy_array = np.array([1, 2, 3, 4])
tensor_from_numpy = torch.from_numpy(numpy_array)
print(f"NumPy to Tensor: {tensor_from_numpy}")

tensor = torch.tensor([1, 2, 3, 4])
numpy_from_tensor = tensor.numpy()
print(f"Tensor to NumPy: {numpy_from_tensor}")

# 8. GPU operations (if available)
print("\n8. GPU Operations:")
if torch.cuda.is_available():
    device = torch.device("cuda")
    tensor_gpu = torch.randn(3, 4).to(device)
    print(f"Tensor on GPU: {tensor_gpu.device}")
    tensor_cpu = tensor_gpu.cpu()
    print("Moved back to CPU")
else:
    print("CUDA not available, using CPU")

# 9. Gradient computation basics
print("\n9. Gradient Computation:")
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1
print(f"x: {x}")
print(f"y = x² + 3x + 1: {y}")

y.backward()  # Compute gradients
print(f"dy/dx at x=2: {x.grad}")  # Should be 2*2 + 3 = 7

print("\n=== End of Tensor Basics ===")```

---

## 02_autograd_gradients.py

```python
"""
PyTorch Tutorial - Part 2: Autograd and Gradients
Understanding automatic differentiation - crucial for interviews
"""

import torch
import torch.nn as nn

print("=== PyTorch Autograd and Gradients ===")

# 1. Basic gradient computation
print("\n1. Basic Gradient Computation:")
x = torch.tensor([3.0], requires_grad=True)
y = torch.tensor([2.0], requires_grad=True)

z = x * y + x ** 2
print(f"x: {x}, y: {y}")
print(f"z = x*y + x²: {z}")

z.backward()
print(f"dz/dx: {x.grad}")  # Should be y + 2*x = 2 + 6 = 8
print(f"dz/dy: {y.grad}")  # Should be x = 3

# 2. Multiple backward passes (need to zero gradients)
print("\n2. Multiple Backward Passes:")
x = torch.tensor([1.0], requires_grad=True)
for i in range(3):
    y = x ** 2
    y.backward()
    print(f"Iteration {i+1}, x.grad: {x.grad}")
    x.grad.zero_()  # Reset gradients

# 3. Vector gradients
print("\n3. Vector Gradients:")
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2
print(f"x: {x}")
print(f"y = x²: {y}")

# For vector outputs, need to provide gradient argument
gradient = torch.tensor([1.0, 1.0, 1.0])
y.backward(gradient)
print(f"dy/dx: {x.grad}")  # Should be 2*x = [2, 4, 6]

# 4. Matrix gradients
print("\n4. Matrix Gradients:")
x = torch.randn(2, 2, requires_grad=True)
y = x ** 2
z = y.mean()  # Scalar output
print(f"x shape: {x.shape}")
print(f"z (mean of x²): {z}")

z.backward()
print(f"dz/dx:\n{x.grad}")  # Should be 2*x/4 (mean divides by 4)

# 5. Higher order gradients
print("\n5. Higher Order Gradients:")
x = torch.tensor([2.0], requires_grad=True)
y = x ** 3
dy_dx = torch.autograd.grad(y, x, create_graph=True)[0]
print(f"y = x³: {y}")
print(f"dy/dx: {dy_dx}")  # Should be 3*2² = 12

d2y_dx2 = torch.autograd.grad(dy_dx, x)[0]
print(f"d²y/dx²: {d2y_dx2}")  # Should be 6*2 = 12

# 6. Gradient flow control
print("\n6. Gradient Flow Control:")

# detach() stops gradient computation
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2
z = y.detach() + x  # y.detach() has no gradient
z.backward()
print(f"With detach, dx: {x.grad}")  # Should be 1 (only from +x term)

# with torch.no_grad() context
x = torch.tensor([2.0], requires_grad=True)
with torch.no_grad():
    y = x ** 2  # No gradient tracked
print(f"y.requires_grad after no_grad: {y.requires_grad}")

# 7. Custom gradient functions (advanced)
print("\n7. Custom Gradient Function:")
class SquareFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input ** 2
    
    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        return 2 * input * grad_output

square = SquareFunction.apply
x = torch.tensor([3.0], requires_grad=True)
y = square(x)
y.backward()
print(f"Custom square function gradient: {x.grad}")  # Should be 6

# 8. Common interview scenario: Loss function gradients
print("\n8. Loss Function Gradients:")
# Simulate a simple linear model: y = wx + b
w = torch.tensor([0.5], requires_grad=True)
b = torch.tensor([0.1], requires_grad=True)
x_data = torch.tensor([1.0, 2.0, 3.0])
y_true = torch.tensor([2.0, 4.0, 6.0])

# Forward pass
y_pred = w * x_data + b
loss = ((y_pred - y_true) ** 2).mean()  # MSE loss

print(f"Predictions: {y_pred}")
print(f"Loss: {loss}")

# Backward pass
loss.backward()
print(f"dL/dw: {w.grad}")
print(f"dL/db: {b.grad}")

# 9. Gradient accumulation pattern
print("\n9. Gradient Accumulation:")
w = torch.tensor([1.0], requires_grad=True)
optimizer = torch.optim.SGD([w], lr=0.01)

for i in range(3):
    # Forward pass
    loss = (w - 5) ** 2
    
    # Backward pass (accumulates gradients)
    loss.backward()
    
    print(f"Step {i+1}: w.grad = {w.grad}")
    
    # Optimizer step and zero gradients
    optimizer.step()
    optimizer.zero_grad()
    
    print(f"Step {i+1}: w = {w}")

print("\n=== End of Autograd and Gradients ===")```

---

## 03_neural_networks.py

```python
"""
PyTorch Tutorial - Part 3: Neural Networks
Building and training neural networks - essential for interviews
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

print("=== PyTorch Neural Networks ===")

# 1. Simple linear layer
print("\n1. Simple Linear Layer:")
linear = nn.Linear(3, 2)  # 3 inputs, 2 outputs
print(f"Linear layer: {linear}")
print(f"Weight shape: {linear.weight.shape}")
print(f"Bias shape: {linear.bias.shape}")

x = torch.randn(5, 3)  # Batch size 5, 3 features
output = linear(x)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")

# 2. Simple feedforward network
print("\n2. Simple Feedforward Network:")
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

net = SimpleNet(10, 5, 1)
print(f"Network: {net}")

x = torch.randn(32, 10)  # Batch size 32
output = net(x)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")

# 3. Common activation functions
print("\n3. Activation Functions:")
x = torch.linspace(-3, 3, 100)
activations = {
    'ReLU': F.relu(x),
    'Sigmoid': F.sigmoid(x), 
    'Tanh': F.tanh(x),
    'LeakyReLU': F.leaky_relu(x, negative_slope=0.1),
    'Softmax': F.softmax(x.unsqueeze(0), dim=1).squeeze(0)
}

for name, activation in activations.items():
    print(f"{name} output range: [{activation.min():.3f}, {activation.max():.3f}]")

# 4. Loss functions
print("\n4. Loss Functions:")
# Binary classification
pred_binary = torch.randn(10, 1)
target_binary = torch.randint(0, 2, (10, 1)).float()
bce_loss = F.binary_cross_entropy_with_logits(pred_binary, target_binary)
print(f"Binary Cross Entropy Loss: {bce_loss:.4f}")

# Multi-class classification
pred_multi = torch.randn(10, 5)  # 10 samples, 5 classes
target_multi = torch.randint(0, 5, (10,))  # Class indices
ce_loss = F.cross_entropy(pred_multi, target_multi)
print(f"Cross Entropy Loss: {ce_loss:.4f}")

# Regression
pred_reg = torch.randn(10, 1)
target_reg = torch.randn(10, 1)
mse_loss = F.mse_loss(pred_reg, target_reg)
print(f"MSE Loss: {mse_loss:.4f}")

# 5. Complete training example - XOR problem
print("\n5. Complete Training Example - XOR Problem:")

class XORNet(nn.Module):
    def __init__(self):
        super(XORNet, self).__init__()
        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# XOR dataset
X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

model = XORNet()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.1)

print("Training XOR network...")
losses = []
for epoch in range(1000):
    # Forward pass
    outputs = model(X)
    loss = criterion(outputs, y)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    losses.append(loss.item())
    
    if (epoch + 1) % 200 == 0:
        print(f'Epoch [{epoch+1}/1000], Loss: {loss.item():.4f}')

# Test the trained model
with torch.no_grad():
    test_outputs = model(X)
    predictions = (test_outputs > 0.5).float()
    accuracy = (predictions == y).float().mean()
    print(f"\nFinal predictions vs targets:")
    for i in range(len(X)):
        print(f"Input: {X[i].numpy()}, Predicted: {test_outputs[i].item():.4f}, Target: {y[i].item()}")
    print(f"Accuracy: {accuracy.item():.4f}")

# 6. Model saving and loading
print("\n6. Model Saving and Loading:")
# Save the model
torch.save(model.state_dict(), '/Users/hanfang/Coding/pytorch-practice/xor_model.pth')
print("Model saved to xor_model.pth")

# Load the model
new_model = XORNet()
new_model.load_state_dict(torch.load('/Users/hanfang/Coding/pytorch-practice/xor_model.pth'))
new_model.eval()

# Verify loaded model works
with torch.no_grad():
    loaded_outputs = new_model(X)
    print("Loaded model predictions:", loaded_outputs.flatten())

# 7. Common neural network patterns
print("\n7. Common Neural Network Patterns:")

# Dropout for regularization
class NetWithDropout(nn.Module):
    def __init__(self):
        super(NetWithDropout, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(50, 1)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)  # Only active during training
        x = self.fc2(x)
        return x

dropout_net = NetWithDropout()
print("Network with dropout:", dropout_net)

# Batch normalization
class NetWithBatchNorm(nn.Module):
    def __init__(self):
        super(NetWithBatchNorm, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.bn1 = nn.BatchNorm1d(50)
        self.fc2 = nn.Linear(50, 1)
    
    def forward(self, x):
        x = self.bn1(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

bn_net = NetWithBatchNorm()
print("Network with batch norm:", bn_net)

# 8. Parameter counting and model info
print("\n8. Model Information:")
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"Simple net parameters: {count_parameters(net)}")
print(f"XOR net parameters: {count_parameters(model)}")

# Print model architecture
print("\nXOR model architecture:")
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

print("\n=== End of Neural Networks ===")```

---

## 04_interview_problems.py

```python
"""
PyTorch Tutorial - Part 4: Common Interview Problems
Real interview questions with PyTorch implementations
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader

print("=== Common PyTorch Interview Problems ===")

# Problem 1: Implement Softmax from scratch
print("\n1. Implement Softmax from Scratch:")
def softmax_from_scratch(x):
    """Numerically stable softmax implementation"""
    exp_x = torch.exp(x - torch.max(x, dim=-1, keepdim=True)[0])
    return exp_x / torch.sum(exp_x, dim=-1, keepdim=True)

x = torch.randn(3, 5)
our_softmax = softmax_from_scratch(x)
pytorch_softmax = F.softmax(x, dim=-1)

print(f"Our softmax:\n{our_softmax}")
print(f"PyTorch softmax:\n{pytorch_softmax}")
print(f"Difference: {torch.max(torch.abs(our_softmax - pytorch_softmax))}")

# Problem 2: Custom Dataset and DataLoader
print("\n2. Custom Dataset Implementation:")
class CustomDataset(Dataset):
    def __init__(self, data, targets):
        self.data = data
        self.targets = targets
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

# Create sample data
data = torch.randn(100, 10)
targets = torch.randint(0, 3, (100,))

dataset = CustomDataset(data, targets)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

print(f"Dataset length: {len(dataset)}")
print(f"Number of batches: {len(dataloader)}")

for batch_idx, (batch_data, batch_targets) in enumerate(dataloader):
    print(f"Batch {batch_idx}: data shape {batch_data.shape}, targets shape {batch_targets.shape}")
    if batch_idx == 2:  # Show first 3 batches
        break

# Problem 3: Implement Batch Normalization
print("\n3. Batch Normalization from Scratch:")
class CustomBatchNorm1d(nn.Module):
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super().__init__()
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum
        
        # Learnable parameters
        self.weight = nn.Parameter(torch.ones(num_features))
        self.bias = nn.Parameter(torch.zeros(num_features))
        
        # Running statistics (not learnable)
        self.register_buffer('running_mean', torch.zeros(num_features))
        self.register_buffer('running_var', torch.ones(num_features))
    
    def forward(self, x):
        if self.training:
            # Training mode: use batch statistics
            batch_mean = x.mean(dim=0)
            batch_var = x.var(dim=0, unbiased=False)
            
            # Update running statistics
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * batch_mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * batch_var
            
            mean, var = batch_mean, batch_var
        else:
            # Evaluation mode: use running statistics
            mean, var = self.running_mean, self.running_var
        
        x_normalized = (x - mean) / torch.sqrt(var + self.eps)
        return self.weight * x_normalized + self.bias

# Test custom batch norm
x = torch.randn(32, 10)
custom_bn = CustomBatchNorm1d(10)
pytorch_bn = nn.BatchNorm1d(10)

# Initialize with same parameters
pytorch_bn.weight.data = custom_bn.weight.data.clone()
pytorch_bn.bias.data = custom_bn.bias.data.clone()

custom_output = custom_bn(x)
pytorch_output = pytorch_bn(x)

print(f"Custom BN output mean: {custom_output.mean(dim=0)}")
print(f"PyTorch BN output mean: {pytorch_output.mean(dim=0)}")
print(f"Difference: {torch.max(torch.abs(custom_output - pytorch_output))}")

# Problem 4: Learning Rate Scheduling
print("\n4. Learning Rate Scheduling:")
model = nn.Linear(10, 1)
optimizer = optim.SGD(model.parameters(), lr=0.1)

# Different schedulers
step_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
exp_scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.9)
cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)

print("Learning rate changes with StepLR:")
for epoch in range(10):
    print(f"Epoch {epoch}: LR = {optimizer.param_groups[0]['lr']:.6f}")
    step_scheduler.step()

# Problem 5: Gradient Clipping
print("\n5. Gradient Clipping Implementation:")
model = nn.Linear(10, 1)
optimizer = optim.SGD(model.parameters(), lr=0.1)

x = torch.randn(32, 10)
y = torch.randn(32, 1)

def gradient_clipping_example():
    for epoch in range(3):
        pred = model(x)
        loss = F.mse_loss(pred, y)
        
        optimizer.zero_grad()
        loss.backward()
        
        # Check gradients before clipping
        total_norm_before = 0
        for p in model.parameters():
            if p.grad is not None:
                param_norm = p.grad.data.norm(2)
                total_norm_before += param_norm.item() ** 2
        total_norm_before = total_norm_before ** (1. / 2)
        
        # Clip gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        # Check gradients after clipping
        total_norm_after = 0
        for p in model.parameters():
            if p.grad is not None:
                param_norm = p.grad.data.norm(2)
                total_norm_after += param_norm.item() ** 2
        total_norm_after = total_norm_after ** (1. / 2)
        
        print(f"Epoch {epoch}: Grad norm before: {total_norm_before:.4f}, after: {total_norm_after:.4f}")
        optimizer.step()

gradient_clipping_example()

# Problem 6: Multi-GPU Training Setup
print("\n6. Multi-GPU Training Setup:")
if torch.cuda.device_count() > 1:
    print(f"Found {torch.cuda.device_count()} GPUs")
    
    model = nn.Linear(10, 1)
    model = nn.DataParallel(model)  # Wrap model for multi-GPU
    
    if torch.cuda.is_available():
        model = model.cuda()
        x = torch.randn(32, 10).cuda()
        y = model(x)
        print(f"Multi-GPU output shape: {y.shape}")
else:
    print("Single GPU or CPU training")

# Problem 7: Custom Loss Function
print("\n7. Custom Loss Function:")
class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        bce_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        pt = torch.exp(-bce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * bce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

# Test focal loss
pred = torch.randn(10, 1)
target = torch.randint(0, 2, (10, 1)).float()

focal_loss = FocalLoss()
bce_loss = nn.BCEWithLogitsLoss()

focal_result = focal_loss(pred, target)
bce_result = bce_loss(pred, target)

print(f"Focal Loss: {focal_result:.4f}")
print(f"BCE Loss: {bce_result:.4f}")

# Problem 8: Weight Initialization
print("\n8. Weight Initialization Strategies:")
def init_weights(module):
    if isinstance(module, nn.Linear):
        print(f"Initializing Linear layer with shape {module.weight.shape}")
        nn.init.xavier_uniform_(module.weight)
        nn.init.constant_(module.bias, 0)
    elif isinstance(module, nn.Conv2d):
        print(f"Initializing Conv2d layer with shape {module.weight.shape}")
        nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')

class TestNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 1)
        self.conv = nn.Conv2d(3, 16, 3)
    
    def forward(self, x):
        return self.fc2(F.relu(self.fc1(x)))

net = TestNet()
print("Before initialization:")
print(f"fc1 weight mean: {net.fc1.weight.mean():.4f}, std: {net.fc1.weight.std():.4f}")

net.apply(init_weights)
print("\nAfter initialization:")
print(f"fc1 weight mean: {net.fc1.weight.mean():.4f}, std: {net.fc1.weight.std():.4f}")

# Problem 9: Memory Optimization
print("\n9. Memory Optimization Techniques:")
def memory_efficient_training():
    model = nn.Sequential(
        nn.Linear(1000, 500),
        nn.ReLU(),
        nn.Linear(500, 100),
        nn.ReLU(),
        nn.Linear(100, 1)
    )
    
    x = torch.randn(64, 1000)
    y = torch.randn(64, 1)
    
    optimizer = optim.Adam(model.parameters())
    
    # Technique 1: Gradient accumulation
    accumulation_steps = 4
    
    for step in range(accumulation_steps):
        # Smaller batch
        batch_x = x[step * 16:(step + 1) * 16]
        batch_y = y[step * 16:(step + 1) * 16]
        
        pred = model(batch_x)
        loss = F.mse_loss(pred, batch_y) / accumulation_steps  # Scale loss
        loss.backward()
    
    optimizer.step()
    optimizer.zero_grad()
    
    print("Gradient accumulation completed")
    
    # Technique 2: Checkpointing (saves memory during backward pass)
    from torch.utils.checkpoint import checkpoint
    
    def checkpoint_function(x):
        return model(x)
    
    x_checkpoint = torch.randn(32, 1000, requires_grad=True)
    # y_checkpoint = checkpoint(checkpoint_function, x_checkpoint)  # Uncomment if needed
    print("Checkpointing example prepared")

memory_efficient_training()

# Problem 10: Model Ensemble
print("\n10. Model Ensemble:")
class SimpleEnsemble(nn.Module):
    def __init__(self, models):
        super().__init__()
        self.models = nn.ModuleList(models)
    
    def forward(self, x):
        outputs = [model(x) for model in self.models]
        return torch.mean(torch.stack(outputs), dim=0)

# Create ensemble of 3 models
models = [nn.Linear(10, 1) for _ in range(3)]
ensemble = SimpleEnsemble(models)

x = torch.randn(32, 10)
ensemble_output = ensemble(x)
print(f"Ensemble output shape: {ensemble_output.shape}")

# Individual model predictions
individual_outputs = [model(x) for model in models]
manual_average = torch.mean(torch.stack(individual_outputs), dim=0)
print(f"Manual average matches ensemble: {torch.allclose(ensemble_output, manual_average)}")

print("\n=== End of Interview Problems ===")```

---

## 05_advanced_topics.py

```python
"""
PyTorch Tutorial - Part 5: Advanced Topics and Best Practices
Advanced concepts frequently asked in senior ML engineer interviews
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import math

print("=== Advanced PyTorch Topics ===")

# 1. Custom Optimizers
print("\n1. Custom Optimizer Implementation:")
class SGDWithMomentum:
    def __init__(self, parameters, lr=0.01, momentum=0.9):
        self.parameters = list(parameters)
        self.lr = lr
        self.momentum = momentum
        self.velocities = [torch.zeros_like(p) for p in self.parameters]
    
    def step(self):
        for param, velocity in zip(self.parameters, self.velocities):
            if param.grad is not None:
                velocity.mul_(self.momentum).add_(param.grad, alpha=1)
                param.data.add_(velocity, alpha=-self.lr)
    
    def zero_grad(self):
        for param in self.parameters:
            if param.grad is not None:
                param.grad.zero_()

# Test custom optimizer
model = nn.Linear(2, 1)
custom_optimizer = SGDWithMomentum(model.parameters(), lr=0.01)

x = torch.randn(10, 2)
y = torch.randn(10, 1)

for epoch in range(5):
    pred = model(x)
    loss = F.mse_loss(pred, y)
    
    custom_optimizer.zero_grad()
    loss.backward()
    custom_optimizer.step()
    
    print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

# 2. Attention Mechanism
print("\n2. Attention Mechanism Implementation:")
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()
        assert d_model % n_heads == 0
        
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        for module in [self.W_q, self.W_k, self.W_v, self.W_o]:
            nn.init.xavier_uniform_(module.weight)
            nn.init.constant_(module.bias, 0)
    
    def create_padding_mask(self, seq, pad_idx=0):
        """Create padding mask to ignore padded tokens"""
        return (seq != pad_idx).unsqueeze(1).unsqueeze(2)
    
    def create_causal_mask(self, size):
        """Create causal mask for autoregressive generation"""
        mask = torch.tril(torch.ones(size, size))
        return mask.unsqueeze(0).unsqueeze(0)  # Add batch and head dimensions
    
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            # Handle both padding masks (True/False) and causal masks (1/0)
            if mask.dtype == torch.bool:
                scores.masked_fill_(~mask, float('-inf'))
            else:
                scores.masked_fill_(mask == 0, float('-inf'))
        
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights
    
    def forward(self, query, key, value, padding_mask=None, causal_mask=None):
        batch_size, seq_length, d_model = query.size()
        
        # Linear transformations and reshape
        Q = self.W_q(query).view(batch_size, seq_length, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, seq_length, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, seq_length, self.n_heads, self.d_k).transpose(1, 2)
        
        # Combine masks if both are provided
        combined_mask = None
        if padding_mask is not None:
            combined_mask = padding_mask
        if causal_mask is not None:
            if combined_mask is not None:
                combined_mask = combined_mask & causal_mask
            else:
                combined_mask = causal_mask
        
        # Apply attention
        attention_output, attention_weights = self.scaled_dot_product_attention(Q, K, V, combined_mask)
        
        # Concatenate heads
        attention_output = attention_output.transpose(1, 2).contiguous().view(
            batch_size, seq_length, d_model)
        
        # Final linear transformation
        output = self.W_o(attention_output)
        
        return output, attention_weights

# Test attention with different masking scenarios
d_model, n_heads, seq_len, batch_size = 512, 8, 10, 2
attention = MultiHeadAttention(d_model, n_heads)

# Example 1: Self-attention without masks
x = torch.randn(batch_size, seq_len, d_model)
output, weights = attention(x, x, x)
print(f"Basic self-attention - Input: {x.shape}, Output: {output.shape}")

# Example 2: With padding mask (for variable-length sequences)
seq_tokens = torch.randint(1, 1000, (batch_size, seq_len))  # Token IDs
padding_mask = attention.create_padding_mask(seq_tokens, pad_idx=0)
output, weights = attention(x, x, x, padding_mask=padding_mask)
print(f"With padding mask - Output: {output.shape}")

# Example 3: With causal mask (for autoregressive generation)
causal_mask = attention.create_causal_mask(seq_len)
output, weights = attention(x, x, x, causal_mask=causal_mask)
print(f"With causal mask - Output: {output.shape}")

# Example 4: With both masks (common in decoder self-attention)
output, weights = attention(x, x, x, padding_mask=padding_mask, causal_mask=causal_mask)
print(f"With both masks - Output: {output.shape}")
print(f"Attention weights shape: {weights.shape}")

# 3. Residual Connections and Layer Normalization
print("\n3. Residual Connections and Layer Normalization:")
class ResidualBlock(nn.Module):
    def __init__(self, dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, dim)
        )
        self.layer_norm = nn.LayerNorm(dim)
    
    def forward(self, x):
        return self.layer_norm(x + self.net(x))  # Residual connection + LayerNorm

residual_block = ResidualBlock(256, 512)
x = torch.randn(32, 256)
output = residual_block(x)
print(f"Residual block - Input: {x.shape}, Output: {output.shape}")

# 4. Learning Rate Warmup and Cosine Annealing
print("\n4. Learning Rate Scheduling with Warmup:")
class WarmupCosineScheduler:
    def __init__(self, optimizer, warmup_steps, max_steps, max_lr, min_lr=0):
        self.optimizer = optimizer
        self.warmup_steps = warmup_steps
        self.max_steps = max_steps
        self.max_lr = max_lr
        self.min_lr = min_lr
        self.step_count = 0
    
    def step(self):
        self.step_count += 1
        
        if self.step_count <= self.warmup_steps:
            # Warmup phase
            lr = self.max_lr * (self.step_count / self.warmup_steps)
        else:
            # Cosine annealing phase
            progress = (self.step_count - self.warmup_steps) / (self.max_steps - self.warmup_steps)
            lr = self.min_lr + (self.max_lr - self.min_lr) * 0.5 * (1 + math.cos(math.pi * progress))
        
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

model = nn.Linear(10, 1)
optimizer = optim.Adam(model.parameters())
scheduler = WarmupCosineScheduler(optimizer, warmup_steps=100, max_steps=1000, max_lr=0.001)

print("Learning rate schedule (first 20 steps):")
for step in range(20):
    scheduler.step()
    lr = optimizer.param_groups[0]['lr']
    print(f"Step {step+1}: LR = {lr:.6f}")

# 5. Mixed Precision Training
print("\n5. Mixed Precision Training:")
if torch.cuda.is_available():
    print("CUDA available - demonstrating mixed precision")
    
    model = nn.Linear(10, 1).cuda()
    optimizer = optim.Adam(model.parameters())
    scaler = torch.cuda.amp.GradScaler()
    
    x = torch.randn(32, 10).cuda()
    y = torch.randn(32, 1).cuda()
    
    # Mixed precision training loop
    for epoch in range(3):
        optimizer.zero_grad()
        
        with torch.cuda.amp.autocast():
            pred = model(x)
            loss = F.mse_loss(pred, y)
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        print(f"Mixed precision epoch {epoch+1}: Loss = {loss.item():.4f}")
else:
    print("CUDA not available - skipping mixed precision example")

# 6. Custom Backward Hook
print("\n6. Custom Backward Hook:")
def gradient_hook(grad):
    print(f"Gradient shape: {grad.shape}, norm: {grad.norm().item():.4f}")
    return grad  # Can modify gradient here

model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)

# Register hook on the first layer
handle = model[0].weight.register_hook(gradient_hook)

x = torch.randn(32, 10)
y = torch.randn(32, 1)

pred = model(x)
loss = F.mse_loss(pred, y)
loss.backward()

# Remove hook
handle.remove()

# 7. Model Profiling and Debugging
print("\n7. Model Profiling:")
model = nn.Sequential(
    nn.Linear(1000, 500),
    nn.ReLU(),
    nn.Linear(500, 100),
    nn.ReLU(),
    nn.Linear(100, 1)
)

x = torch.randn(64, 1000)

# Memory profiling
def profile_model_memory():
    torch.cuda.empty_cache() if torch.cuda.is_available() else None
    
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
        start_memory = torch.cuda.memory_allocated()
    
    # Forward pass
    output = model(x)
    
    if torch.cuda.is_available():
        forward_memory = torch.cuda.memory_allocated()
        print(f"Memory after forward: {(forward_memory - start_memory) / 1024**2:.2f} MB")
    else:
        print("CUDA not available - memory profiling skipped")

profile_model_memory()

# 8. Dynamic Computation Graphs
print("\n8. Dynamic Computation Graphs:")
class DynamicNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 20)
        self.fc2 = nn.Linear(20, 20)
        self.fc3 = nn.Linear(20, 1)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        
        # Dynamic: random number of layers
        for _ in range(torch.randint(1, 4, (1,)).item()):
            x = F.relu(self.fc2(x))
        
        return self.fc3(x)

dynamic_net = DynamicNet()
x = torch.randn(32, 10)

print("Dynamic computation graph outputs:")
for i in range(3):
    output = dynamic_net(x)
    print(f"Run {i+1}: Output shape = {output.shape}, mean = {output.mean().item():.4f}")

# 9. Model Quantization
print("\n9. Model Quantization:")
model = nn.Sequential(
    nn.Linear(10, 50),
    nn.ReLU(),
    nn.Linear(50, 1)
)

# Post-training quantization
model.eval()
quantized_model = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

x = torch.randn(32, 10)
original_output = model(x)
quantized_output = quantized_model(x)

print(f"Original model size: ~{sum(p.numel() * 4 for p in model.parameters()) / 1024:.1f} KB")
print(f"Quantized model parameters: {sum(p.numel() for p in quantized_model.parameters() if hasattr(p, 'numel'))}")
print(f"Output difference: {torch.mean(torch.abs(original_output - quantized_output)).item():.6f}")

# 10. Best Practices Summary
print("\n10. Best Practices Summary:")

best_practices = {
    "Data Loading": "Use DataLoader with num_workers > 0 for faster loading",
    "Memory": "Use torch.cuda.empty_cache() and del unnecessary variables",
    "Gradients": "Always call optimizer.zero_grad() before backward()",
    "Evaluation": "Use model.eval() and torch.no_grad() during inference",
    "Reproducibility": "Set random seeds: torch.manual_seed(42)",
    "Debugging": "Use torch.autograd.set_detect_anomaly(True) for gradient issues",
    "Performance": "Use appropriate data types (float16 for inference if possible)",
    "Initialization": "Use proper weight initialization schemes",
    "Regularization": "Apply dropout, batch norm, weight decay as needed",
    "Monitoring": "Track gradient norms, learning rates, and loss curves"
}

print("PyTorch Best Practices:")
for category, practice in best_practices.items():
    print(f"• {category}: {practice}")

print("\n=== End of Advanced Topics ===")```

---

## run_tutorial.py

```python
"""
PyTorch Tutorial Runner
Run this to execute all tutorial parts
"""

import subprocess
import sys
import os

def run_tutorial_part(filename, description):
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"File: {filename}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, filename], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
        else:
            print(f"Error running {filename}:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Failed to run {filename}: {e}")

def main():
    tutorials = [
        ("01_tensor_basics.py", "Part 1: Tensor Basics and Operations"),
        ("02_autograd_gradients.py", "Part 2: Autograd and Gradients"),
        ("03_neural_networks.py", "Part 3: Neural Networks"),
        ("04_interview_problems.py", "Part 4: Common Interview Problems"),
        ("05_advanced_topics.py", "Part 5: Advanced Topics and Best Practices")
    ]
    
    print("PyTorch Tutorial Series")
    print("Choose an option:")
    print("0. Run all tutorials")
    for i, (filename, description) in enumerate(tutorials, 1):
        print(f"{i}. {description}")
    
    try:
        choice = int(input("\nEnter your choice (0-5): "))
        
        if choice == 0:
            for filename, description in tutorials:
                run_tutorial_part(filename, description)
        elif 1 <= choice <= len(tutorials):
            filename, description = tutorials[choice - 1]
            run_tutorial_part(filename, description)
        else:
            print("Invalid choice!")
            
    except ValueError:
        print("Please enter a valid number!")
    except KeyboardInterrupt:
        print("\nTutorial interrupted by user.")

if __name__ == "__main__":
    main()```

