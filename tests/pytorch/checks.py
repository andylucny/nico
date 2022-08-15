import torch

print(torch.cuda.is_available())
#>>> True

print(torch.cuda.current_device())
#>>> 0

print(torch.cuda.device(0))
#>>> <torch.cuda.device at 0x000001F807D7CCC0>

print(torch.cuda.device_count())
#>>> 1

print(torch.cuda.get_device_name(0))
#>>> 'NVIDIA GeForce GTX 1050'

print(torch.version.cuda)
#'10.2'
