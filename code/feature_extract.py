import os
import glob
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
from torchvision.models import resnet18,resnet50
import numpy as np
import csv
import pandas as pd
#设置数据和特征存储路径

data_dir ='C:/Users/Hy-tech/Desktop/survival_data_2d/slicer/slicer_img'
features_dir ='C:/Users/Hy-tech/Desktop/survival_data_2d/slicer'
#加载ResNet50模型
model = resnet50(pretrained=True)
weight=torch.load('best.pth')
model = torch.nn.Sequential(*list(model.children())[:-1]) # 去掉最后一层全连接层，取平均池化层的特征
#定义特征提取函数
def extractor(img_path, net,use_gpu):
    transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor()])
    #读取图片并进行预处理
    img = Image.open(img_path).convert('RGB') #转换为RGB图像
    img = transform(img)
    #将图片转换为PyTorch Tensor，并添加batch维度
    x= Variable(torch.unsqueeze(img, dim=0).float(),requires_grad=False)
    # 如果使用GPU，则将数据和网络模型移动到GPU上
    if use_gpu:
        x = x.cuda()
        net = net.cuda()
    #使用网络模型提取特征
    y = net(x).cpu()
    y = torch.squeeze(y)
    y = y.data.numpy()#保存特征到文件中
    return y

#遍历数据目录中的图片文件
extensions = ['jpg','jpeg', 'JPG','JPEC','png']
files_list =[]
x = os.walk(data_dir)
for path,d,filelist in x:
        for filename in filelist:
            file_glob = os.path.join(path, filename)
            files_list.extend(glob.glob(file_glob))
# 单独提取每张图片的特征
# for img_path in files_list:
#     file_name = os.path.splitext(os.path.basename(img_path))[0]
#     feature_path = os.path.join(features_dir, file_name +'.txt')
#     extractor(img_path, feature_path, model,use_gpu=False)

#提取所有图片的特征并保存到DataFrame中
features=[]
for img_path in files_list:
    file_name =(os.path.splitext(os.path.basename(img_path))[0]).split('_')[-2]
    hospital_name=(os.path.splitext(os.path.basename(img_path))[0]).split('_')[-3:][0]
    feature = extractor(img_path,model, use_gpu=False)
    features.append([hospital_name]+[file_name] + feature.tolist())
columns =['hospital_name']+['file_name'] + ['feature_{}'.format(i) for i in range((len(features[0])-2))]

#     file_name =(os.path.splitext(os.path.basename(img_path))[0]).split('_')[-2]
#     feature = extractor(img_path,model, use_gpu=False)
#     features.append([file_name] + feature.tolist())
# columns =['file_name'] + ['feature_{}'.format(i) for i in range(len(features[0])-1)]
df =pd.DataFrame(features, columns=columns)
#将DataFrame保存为Excel文件
df.to_csv(features_dir+'/feature_slicer.csv',index=False)