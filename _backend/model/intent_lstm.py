"""
@author : Hyunwoong
@when : 5/11/2020
@homepage : https://github.com/gusdnd852
"""

import torch
from torch import nn

from _backend.decorators import intent


@intent
class IntentLSTM(nn.Module):

    def __init__(self, label_dict, bidirectional=True):
        """
        Intent Classification을 위한 LSTM 클래스입니다.

        :param label_dict: 라벨 딕셔너리
        :param bidirectional: bidirectional 여부
        """

        super().__init__()
        self.label_dict = label_dict
        self.direction = 2 if bidirectional else 1
        self.lstm = nn.LSTM(input_size=self.vector_size,
                            hidden_size=self.d_model,
                            num_layers=self.layers,
                            batch_first=True,
                            bidirectional=True if self.direction == 2 else False)

        # ret features, logits => retrieval시 사용
        # clf logits => softmax classification시 사용
        self.ret_features = nn.Linear(self.d_model * self.direction, self.d_loss)
        self.ret_logits = nn.Linear(self.d_loss * self.direction, len(self.label_dict))
        self.clf_logits = nn.Linear(self.d_model, len(self.label_dict))

    def init_hidden(self, batch_size):
        param1 = torch.randn(self.layers * self.direction, batch_size, self.d_model).to(self.device)
        param2 = torch.randn(self.layers * self.direction, batch_size, self.d_model).to(self.device)
        return torch.autograd.Variable(param1), torch.autograd.Variable(param2)

    def forward(self, x):
        b, l, v = x.size()
        out, (h_s, c_s) = self.lstm(x, self.init_hidden(b))
        return h_s[0]
