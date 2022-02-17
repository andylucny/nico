import torch

torch.cuda.is_available()
#>>> True

torch.cuda.current_device()
#>>> 0

torch.cuda.device(0)
#>>> <torch.cuda.device at 0x000001F807D7CCC0>

torch.cuda.device_count()
#>>> 1

torch.cuda.get_device_name(0)
#>>> 'NVIDIA GeForce GTX 1050'
