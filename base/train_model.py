# train_model.py
import threading
import time
from django.core.cache import cache

def train_model_async():
    # Hàm này sẽ huấn luyện mô hình không đồng bộ và gửi cập nhật tiến trình

    # Ví dụ đơn giản: Huấn luyện trong 10 epoch và gửi cập nhật sau mỗi epoch
    for epoch in range(1, 11):
        # Huấn luyện mô hình ở mỗi epoch
        time.sleep(2)  # Giả sử mỗi epoch mất 2 giây

        # Lưu thông tin tiến trình vào cache để gửi cho máy khách
        cache.set('training_progress', {'epoch': epoch, 'total_epochs': 10})

    # Báo cho máy khách biết rằng huấn luyện đã hoàn tất
    cache.set('training_progress', {'message': 'Training completed'})

# Khởi tạo một luồng riêng để thực hiện huấn luyện không đồng bộ
training_thread = threading.Thread(target=train_model_async)
training_thread.daemon = True
