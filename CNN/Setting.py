class Setting:
  def __init__(self, padding=0, epochs=10, patch_sizes=32, stride=0, optimizer='adam', loss='categorical_crossentropy', activation='softmax',max_pooling=2, test_size=0.2, num_classes=''):
    self.padding = padding
    self.epochs = epochs
    self.patch_sizes = patch_sizes
    self.stride = stride
    self.optimizer = optimizer
    self.loss = loss
    self.num_classes = num_classes
    self.activation = activation
    self.max_pooling = max_pooling
    self.test_size = test_size
  def __str__(self):
      return (f"Padding: {self.padding}, "
              f"Epochs: {self.epochs}, "
              f"Patch Sizes: {self.patch_sizes}, "
              f"Stride: {self.stride}, "
              f"Optimizer: {self.optimizer}, "
              f"Loss: {self.loss}, "
              f"Activation: {self.activation}, "
              f"Max Pooling: {self.max_pooling}")