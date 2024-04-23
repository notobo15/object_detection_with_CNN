from CNN.Training import FlowerClassifier

path = '\home\notobo\detector_python\static\\uploads\d57f4234-d72e-4012-a48b-d00c34c2d353'
flower_classifier = FlowerClassifier(10)
flower_classifier.build_model()
train_generator, validation_generator = flower_classifier.make_data(path)
flower_classifier.train_model(train_generator, validation_generator)
flower_classifier.save_model(path)
