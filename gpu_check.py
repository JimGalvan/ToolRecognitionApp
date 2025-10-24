import torch
print(torch.cuda.is_available())  # True means GPU is available
print(torch.cuda.get_device_name(0))  # Name of your GPU
