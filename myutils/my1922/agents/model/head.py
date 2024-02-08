import torch
import torch.nn.functional as F

import torch

class NewGaussianPolicyHead(torch.nn.Module):
    def __init__(
        self,
        loc_activation=torch.nn.Tanh(),
        loc_fn=None,
        scale_activation=torch.nn.Softplus(),
        scale_min=1e-4,
        scale_max=1,
        scale_fn=None,
        distribution=torch.distributions.normal.Normal,
    ):
        super().__init__()
        self.loc_activation = loc_activation
        self.loc_fn = loc_fn
        self.scale_activation = scale_activation
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.scale_fn = scale_fn
        self.distribution = distribution

    def initialize(self, input_size, action_size):
        # loc_layer에서 마지막 3개 노드만 선형 활성화를 적용
        self.loc_layer = CustomActivationLayer(input_size, action_size)
        if self.loc_fn:
            self.loc_layer.apply(self.loc_fn)

        # scale_layer에서 마지막 3개 노드만 선형 활성화를 적용
        self.scale_layer = CustomActivationLayer(input_size, action_size)
        if self.scale_fn:
            self.scale_layer.apply(self.scale_fn)

    def forward(self, inputs):
        loc = self.loc_layer(inputs)
        scale = self.scale_layer(inputs)
        scale = torch.clamp(scale, self.scale_min, self.scale_max)
        return self.distribution(loc, scale)

class CustomActivationLayer(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear = torch.nn.Linear(input_size, output_size)
        # Hardtanh 활성화 함수는 모든 노드에 대해 적용 가능합니다. 필요에 따라 조정하세요.
        self.hardtanh = torch.nn.Hardtanh(min_val=-100, max_val=100)
        # Tanh 활성화 함수도 마찬가지로 적용 가능합니다.
        self.tanh = torch.nn.Tanh()

    def forward(self, x):
        x = self.linear(x)
        # 전체 출력에 tanh 적용
        tanh_output = self.tanh(x)
        # 전체 출력에 hardtanh 적용
        hardtanh_output = self.hardtanh(10*x)
        # 마지막 3개 노드만 hardtanh 적용을 위해 조건부로 출력을 선택합니다.
        
        # 이를 위해 마지막 차원 (노드 차원)에서 각 노드에 대한 마스크를 생성합니다.
        output_mask = torch.ones_like(x, dtype=torch.bool)

        output_mask[-3:] = False  # 마지막 3개 노드를 제외한 나머지에 True 설정
        # 마스크를 사용하여 적절한 출력을 선택하고 병합합니다.
        output = torch.where(output_mask, tanh_output, hardtanh_output)

        return output