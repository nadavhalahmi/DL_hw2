import torch
import itertools as it
import torch.nn as nn


class ConvClassifier(nn.Module):
    """
    A convolutional classifier model based on PyTorch nn.Modules.

    The architecture is:
    [(CONV -> ReLU)*P -> MaxPool]*(N/P) -> (Linear -> ReLU)*M -> Linear
    """

    def __init__(self, in_size, out_classes: int, channels: list,
                 pool_every: int, hidden_dims: list):
        """
        :param in_size: Size of input images, e.g. (C,H,W).
        :param out_classes: Number of classes to output in the final layer.
        :param channels: A list of of length N containing the number of
            (output) channels in each conv layer.
        :param pool_every: P, the number of conv layers before each max-pool.
        :param hidden_dims: List of of length M containing hidden dimensions of
            each Linear layer (not including the output layer).
        """
        super().__init__()
        assert channels and hidden_dims

        self.in_size = in_size
        self.out_classes = out_classes
        self.channels = channels
        self.pool_every = pool_every
        self.hidden_dims = hidden_dims

        self.feature_extractor = self._make_feature_extractor()
        self.classifier = self._make_classifier()

    def _make_feature_extractor(self):
        in_channels, in_h, in_w, = tuple(self.in_size)

        layers = []
        # TODO: Create the feature extractor part of the model:
        #  [(CONV -> ReLU)*P -> MaxPool]*(N/P)
        #  Use only dimension-preserving 3x3 convolutions. Apply 2x2 Max
        #  Pooling to reduce dimensions after every P convolutions.
        #  Note: If N is not divisible by P, then N mod P additional
        #  CONV->ReLUs should exist at the end, without a MaxPool after them.
        # ====== YOUR CODE: ======
        layers.append(nn.Conv2d(in_channels=in_channels, out_channels=self.channels[0], kernel_size=3, padding=(1,1)))
        layers.append(nn.ReLU())
        N = len(self.channels)
        P = self.pool_every
        if P == 1:
            layers.append(nn.MaxPool2d(kernel_size=2))
        for i in range(1, N):
            layers.append(nn.Conv2d(in_channels=self.channels[i-1], out_channels=self.channels[i], kernel_size=3,padding=(1,1)))
            layers.append(nn.ReLU())
            if (i+1) % P == 0:
                layers.append(nn.MaxPool2d(kernel_size=2))
        # ========================
        seq = nn.Sequential(*layers)
        return seq

    def _make_classifier(self):
        in_channels, in_h, in_w, = tuple(self.in_size)

        layers = []
        # TODO: Create the classifier part of the model:
        #  (Linear -> ReLU)*M -> Linear
        #  You'll first need to calculate the number of features going in to
        #  the first linear layer.
        #  The last Linear layer should have an output dim of out_classes.
        # ====== YOUR CODE: ======
        N = len(self.channels)
        P = self.pool_every
        for i in range(N//P):
            in_h = in_h // 2
            in_w = in_w // 2
        M = len(self.hidden_dims)
        layers.append(nn.Linear(in_features=self.channels[-1]*in_h*in_w, out_features=self.hidden_dims[0]))
        layers.append(nn.ReLU())
        for i in range(M-1):
            layers.append(nn.Linear(in_features=self.hidden_dims[i], out_features=self.hidden_dims[i+1]))
            layers.append(nn.ReLU())
        layers.append(nn.Linear(in_features=self.hidden_dims[-1], out_features=self.out_classes))
        # ========================
        seq = nn.Sequential(*layers)
        return seq

    def forward(self, x):
        # TODO: Implement the forward pass.
        #  Extract features from the input, run the classifier on them and
        #  return class scores.
        # ====== YOUR CODE: ======
        features = self.feature_extractor(x)
        features = features.view(features.size(0), -1)
        out = self.classifier(features)
        # ========================
        return out


class ResidualBlock(nn.Module):
    """
    A general purpose residual block.
    """

    def __init__(self, in_channels: int, channels: list, kernel_sizes: list,
                 batchnorm=False, dropout=0.):
        """
        :param in_channels: Number of input channels to the first convolution.
        :param channels: List of number of output channels for each
        convolution in the block. The length determines the number of
        convolutions.
        :param kernel_sizes: List of kernel sizes (spatial). Length should
        be the same as channels. Values should be odd numbers.
        :param batchnorm: True/False whether to apply BatchNorm between
        convolutions.
        :param dropout: Amount (p) of Dropout to apply between convolutions.
        Zero means don't apply dropout.
        """
        super().__init__()
        assert channels and kernel_sizes
        assert len(channels) == len(kernel_sizes)
        assert all(map(lambda x: x % 2 == 1, kernel_sizes))

        self.main_path, self.shortcut_path = None, None

        # TODO: Implement a generic residual block.
        #  Use the given arguments to create two nn.Sequentials:
        #  - main_path, which should contain the convolution, dropout,
        #    batchnorm, relu sequences (in this order). Should end with a
        #    final conv as in the diagram.
        #  - shortcut_path which should represent the skip-connection and
        #    may contain a 1x1 conv.
        #  Notes:
        #  - Use convolutions which preserve the spatial extent of the input.
        #  - Use bias in the main_path conv layers, and no bias in the skips.
        #  - For simplicity of implementation, assume kernel sizes are odd.
        #  - Don't create layers which you don't use. This will prevent
        #    correct comparison in the test.
        # ====== YOUR CODE: ======
        layers = []
        layers.append(nn.Conv2d(in_channels=in_channels, out_channels=channels[0], kernel_size=kernel_sizes[0],
                                padding=kernel_sizes[0]//2, bias=True))
        N = len(channels)
        for i in range(1, N):
            if dropout > 0:
                layers.append(nn.Dropout2d(dropout))
            if batchnorm:
                layers.append(nn.BatchNorm2d(channels[i-1]))
            layers.append(nn.ReLU())
            layers.append(nn.Conv2d(in_channels=channels[i - 1], out_channels=channels[i], kernel_size=kernel_sizes[i],
                                    padding=kernel_sizes[i]//2, bias=True))
        self.main_path = nn.Sequential(*layers)

        layers = []
        if in_channels != channels[-1]:
            layers.append(nn.Conv2d(in_channels=in_channels, out_channels=channels[-1], kernel_size=1, bias=False))
        self.shortcut_path = nn.Sequential(*layers)
        # ========================

    def forward(self, x):
        out = self.main_path(x)
        out += self.shortcut_path(x)
        out = torch.relu(out)
        return out


class ResNetClassifier(ConvClassifier):
    def __init__(self, in_size, out_classes, channels, pool_every,
                 hidden_dims):
        super().__init__(in_size, out_classes, channels, pool_every,
                         hidden_dims)

    def _make_feature_extractor(self):
        in_channels, in_h, in_w, = tuple(self.in_size)

        layers = []
        # TODO: Create the feature extractor part of the model:
        #  [-> (CONV -> ReLU)*P -> MaxPool]*(N/P)
        #   \------- SKIP ------/
        #  Use only dimension-preserving 3x3 convolutions. Apply 2x2 Max
        #  Pooling to reduce dimensions after every P convolutions.
        #  Notes:
        #  - If N is not divisible by P, then N mod P additional
        #    CONV->ReLUs (with a skip over them) should exist at the end,
        #    without a MaxPool after them.
        #  - Use your ResidualBlock implemetation.
        # ====== YOUR CODE: ======
        N = len(self.channels)
        P = self.pool_every
        for i in range(N//P):
            if i == 0:
                layers.append(ResidualBlock(in_channels, self.channels[:P], [3]*P))
            else:
                layers.append(ResidualBlock(self.channels[i*P-1], self.channels[i*P:min(P*(i+1), N)],
                                            [3]*min(P, N-(i*P))))
            layers.append(nn.MaxPool2d(kernel_size=2))
        if N % P != 0:
            layers.append(ResidualBlock(self.channels[-(N % P)-1], self.channels[-(N % P):], [3]*(N % P)))

        # ========================
        seq = nn.Sequential(*layers)
        return seq


class YourCodeNet(ConvClassifier):
    def __init__(self, in_size, out_classes, channels, pool_every,
                 hidden_dims):
        super().__init__(in_size, out_classes, channels, pool_every,
                         hidden_dims)

    # TODO: Change whatever you want about the ConvClassifier to try to
    #  improve it's results on CIFAR-10.
    #  For example, add batchnorm, dropout, skip connections, change conv
    #  filter sizes etc.
    # ====== YOUR CODE: ======

    def _make_feature_extractor(self):
        in_channels, in_h, in_w, = tuple(self.in_size)
        layers = []

        N = len(self.channels)
        P = self.pool_every

        layers.append(nn.Conv2d(in_channels, self.channels[0], 3, padding=1))
        layers.append(nn.Dropout(p=0.2))
        layers.append(nn.ReLU())
        if P == 1:
            layers.append(nn.MaxPool2d(kernel_size=2, stride=2))

        for i in range(1, N):
            layers.append(nn.Conv2d(self.channels[i - 1], self.channels[i], 3, padding=1))
            if i % 3 == 0:
                layers.append(nn.BatchNorm2d(self.channels[i]))
            layers.append(nn.Dropout(p=0.2))
            layers.append(nn.ReLU())

            if ((i+1) % P) == 0:
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))

        seq = nn.Sequential(*layers)
        return seq

    def _make_classifier(self):
        N = len(self.channels)
        P = self.pool_every

        in_channels, in_h, in_w, = tuple(self.in_size)

        layers = []
        for i in range(N//P):
            in_h = in_h // 2
            in_w = in_w // 2

        layers.append(nn.Linear(self.channels[-1] * in_h * in_w, self.hidden_dims[0]))
        layers.append(nn.Dropout(p=0.5))
        layers.append(nn.ReLU())

        for i in range(len(self.hidden_dims) - 1):
            layers.append(nn.Linear(self.hidden_dims[i], self.hidden_dims[i + 1]))
            layers.append(nn.Dropout(p=0.5))
            layers.append(nn.ReLU())

        layers.append(nn.Linear(self.hidden_dims[-1], self.out_classes))

        seq = nn.Sequential(*layers)
        return seq

    # ========================
