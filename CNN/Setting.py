class Setting:
  def __init__(self, padding=0, epochs=10, patch_sizes=32, stride=0, optimizer='adam', loss='categorical_crossentropy', activation='softmax',max_pooling=2):
    self.padding = padding
    self.epochs = epochs
    self.patch_sizes = patch_sizes
    self.stride = stride
    self.optimizer = optimizer
    self.loss = loss
    self.activation = activation
    self.max_pooling = max_pooling
