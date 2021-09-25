import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='weight/best.pt')

result = model('data/images/example_americano2.jpg')

result.show()