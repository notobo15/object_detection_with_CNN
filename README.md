
# Xây Dựng Ứng Dụng Nhận Diện Vật Thể qua mô hình CNN

![alt text](docs/images/home.png)

## Tóm tắt
- [Xây Dựng Ứng Dụng Nhận Diện Vật Thể qua mô hình CNN](#xây-dựng-ứng-dụng-nhận-diện-vật-thể-qua-mô-hình-cnn)
  - [Tóm tắt](#tóm-tắt)
  - [Intro](#intro)
  - [Demo](#demo)
  - [Quick Start](#quick-start)
    - [Lưu Ý](#lưu-ý)
  - [Authors](#authors)
  - [Copyright and license](#copyright-and-license)

  

## Intro
- Dễ dàng và nhanh chóng để tạo mô hình máy học cho trên web của bạn!
- Xây dựng mạng nơ-ron tích chập (CNN) đóng vai trò thiết yếu trong thị giác máy tính, giúp máy tính nhận diện và phân loại vật thể từ hình ảnh với độ chính xác cao. 
- Kết hợp với kiến trúc MobileNet mang lại khả năng nhận diện và phân loại vật thể từ hình ảnh với hiệu quả cao và tốc độ nhanh, ngay cả trên các thiết bị di động. MobileNet tối ưu hóa quá trình học đặc trưng thông qua các lớp tích chập phân tách theo chiều sâu, giảm thiểu số lượng phép tính cần thiết mà vẫn duy trì độ chính xác cao.  

## Demo
Chọn Tạo Mới Project
![alt text](docs/images/new-project.png)
Train với Dataset Có Sẵn
![alt text](docs/images/standard-training.png)
Train với Dataset Chính Mình
![alt text](docs/images/custom-training.png)
Kết Quả Dự Đoán 
![alt text](docs/images/prediction.png)

## Quick Start  

### Lưu Ý
**Do một số package không còn hổ trợ trên Windows và để tránh lỗi không mong muốn trong quá trình cài đặt cấu hình tối thiểu là:**
```
1. Hệ điểu hành: Linux
2. Python Version: >=3.7
3. Tensorflow Version: >=2.4
```
- [Download the latest release](https://github.com/notobo15/detector_python/releases/tag/v1.0.0)

- Clone the repo: `git clone https://github.com/notobo15/detector_python.git`

```bash
cd detector_python
```

```bash
pip install -r setup.txt
```

```bash
python manage.py runserver
```

## Authors
- Nguyen Thanh Binh
- Ngo Kieu Lam

## Copyright and license
Code released under the [MIT License](https://github.com/notobo15/detector_python/blob/v1.0.0/LICENSE).