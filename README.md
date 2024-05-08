<h1 align="center">Insightful <br> Detection</h1>

<p align="center">
  <a href="https://github.com/notobo15/object_detection_with_CNN/releases/tag/v1.0.0">
    <img src="https://img.shields.io/github/v/release/notobo15/object_detection_with_CNN?label=Version&style=flat-square" alt="Version">
  </a>
  <a href="https://github.com/notobo15/object_detection_with_CNN/releases/tag/v1.0.0">
    <img src="https://img.shields.io/github/v/release/notobo15/object_detection_with_CNN?label=Release&style=flat-square" alt="Release">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
</p>


# Xây Dựng Ứng Dụng Nhận Diện Vật Thể qua mô hình CNN

![alt text](docs/images/home.png)

## [Link File Báo Cáo](https://www.overleaf.com/read/ggttmjkvswmt#9b40b4)

## Table of Contents
- [Xây Dựng Ứng Dụng Nhận Diện Vật Thể qua mô hình CNN](#xây-dựng-ứng-dụng-nhận-diện-vật-thể-qua-mô-hình-cnn)
  - [Link File Báo Cáo](#link-file-báo-cáo)
  - [Table of Contents](#table-of-contents)
  - [Intro](#intro)
  - [Demo](#demo)
      - [New Project Page](#new-project-page)
      - [Standard Training Page](#standard-training-page)
      - [Custom Training Page](#custom-training-page)
      - [Import Model Training Page](#import-model-training-page)
      - [Prediction Result](#prediction-result)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
  - [Authors](#authors)
  - [Copyright and Licenses](#copyright-and-licenses)

  

## Intro
- Dễ dàng và nhanh chóng để tạo mô hình máy học cho trên web của bạn!
- Xây dựng mạng nơ-ron tích chập (CNN) đóng vai trò thiết yếu trong thị giác máy tính, giúp máy tính nhận diện và phân loại vật thể từ hình ảnh với độ chính xác cao. 
- Kết hợp với kiến trúc MobileNet mang lại khả năng nhận diện và phân loại vật thể từ hình ảnh với hiệu quả cao và tốc độ nhanh, ngay cả trên các thiết bị di động. MobileNet tối ưu hóa quá trình học đặc trưng thông qua các lớp tích chập phân tách theo chiều sâu, giảm thiểu số lượng phép tính cần thiết mà vẫn duy trì độ chính xác cao.  

## Demo
#### New Project Page
![alt text](docs/images/new-project.png)
#### Standard Training Page
![alt text](docs/images/standard-training.png)
#### Custom Training Page
![alt text](docs/images/custom-training.png)
#### Import Model Training Page
![alt text](docs/images/import-training.png)
#### Prediction Result 
![alt text](docs/images/prediction.png)
![alt text](docs/images/import-training-prediction.png)
  

## Prerequisites
**Do một số package không còn hổ trợ trên Windows và để tránh lỗi không mong muốn trong quá trình cài đặt cấu hình tối thiểu là:**
```
1. Hệ điểu hành: Linux
2. Python Version: >=3.7
3. Tensorflow Version: >=2.4
```

## Installing

**Step 1: Clone this repository**
- [Download the latest release](https://github.com/notobo15/object_detection_with_CNN/releases/tag/v1.0.0)

- Clone the repo: `git clone https://github.com/notobo15/object_detection_with_CNN.git`

**Step 2: Install dependencies**

```bash
cd object_detection_with_CNN
pip install -r setup.txt
```
**Step 3: Run the server**

```bash
python manage.py runserver
```

## Authors
- Nguyen Thanh Binh
- Ngo Kieu Lam

## Copyright and Licenses
Code released under the [MIT License](https://github.com/notobo15/object_detection_with_CNN/blob/v1.0.0/LICENSE).