from torch import nn
import torch
import torch.nn.functional as F


class CCE(nn.Module):
    def __init__(self, device, balancing_factor=1):
        super(CCE, self).__init__()
        self.nll_loss = nn.NLLLoss()
        self.device = device # {'cpu', 'cuda:0', 'cuda:1', ...}
        self.balancing_factor = balancing_factor

    def forward(self, yHat, y):
        # Note: yHat.shape[1] <=> number of classes
        batch_size = len(y)
        # cross entropy
        cross_entropy = self.nll_loss(F.log_softmax(yHat, dim=1), y)
        # complement entropy
        yHat = F.softmax(yHat, dim=1)
        Yg = yHat.gather(dim=1, index=torch.unsqueeze(y, 1))
        Px = yHat / (1 - Yg) + 1e-7
        Px_log = torch.log(Px + 1e-10)
        y_zerohot = torch.ones(batch_size, yHat.shape[1]).scatter_(
            1, y.view(batch_size, 1).data.cpu(), 0)
        output = Px * Px_log * y_zerohot.to(device=self.device)
        complement_entropy = torch.sum(output) / (float(batch_size) * float(yHat.shape[1]))

        return cross_entropy - self.balancing_factor * complement_entropy


class Classification_Loss(nn.Module):
    def __init__(self):
        super(Classification_Loss, self).__init__()
        self.criterionCE = nn.CrossEntropyLoss()


    def forward(self, model_output, targets, model):

        # torch.empty(3, dtype=torch.long)
        # model_output = model_output.long()
        # targets = targets.long()
        # print(model_output)
        # print(F.sigmoid(model_output))
        # print(targets)
        # print('kkk')
        regularization_loss = 0
        for param in model.module.parameters():
            regularization_loss += torch.sum(torch.abs(param)) #+torch.sum(torch.abs(param))**2
        # loss = 0.00001 * regularization_loss
        loss = 0

        # model_output = F.sigmoid(model_output)
        # loss = self.mse_criterion(model_output,targets)
        loss += self.criterionCE(model_output,targets)
        return loss
