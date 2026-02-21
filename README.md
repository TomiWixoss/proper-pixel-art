# Proper Pixel Art

## Tóm tắt

Chuyển đổi các hình ảnh mang phong cách pixel-art bị nhiễu, độ phân giải cao do các mô hình AI tạo ra hoặc từ các nguồn tải lên web chất lượng thấp thành các tài nguyên pixel-art sạch sẽ, có độ phân giải thực.

### Thách thức

Các hình ảnh phong cách pixel-art do AI tạo ra thường bị nhiễu và có độ phân giải cao, thường kèm theo lưới không đồng đều và các lỗi hình ảnh ngẫu nhiên. Các kỹ thuật giảm lấy mẫu (downsampling) tiêu chuẩn thường không hoạt động hiệu quả. Cách tiếp cận hiện tại thường là sử dụng các kỹ thuật giảm tỷ lệ đơn giản hoặc tạo lại tài nguyên một cách thủ công từng pixel một.

Công cụ này giải quyết cả hai vấn đề trên bằng cách tự động hóa quy trình khôi phục các tài nguyên pixel-art có độ phân giải thực.

## Cài đặt

### Từ Nguồn

Sao chép kho lưu trữ

```bash
git clone git@github.com:KennethJAllen/proper-pixel-art.git
cd proper-pixel-art
```

#### Tạo Môi trường Ảo

- Cài đặt [uv](https://docs.astral.sh/uv/getting-started/installation/) nếu chưa cài đặt.
- Đồng bộ môi trường:
  - `uv sync`

### Từ Pip

```bash
pip install proper-pixel-art
```

Hoặc với uv:

```bash
uv add proper-pixel-art
```

## Cách sử dụng

Trước tiên, hãy chuẩn bị một ảnh phong cách pixel-art nguồn (ví dụ: ảnh do GPT-4o tạo ra hoặc ảnh chụp màn hình pixel-art).

### Giao diện dòng lệnh (CLI)

```bash
uv run ppa <đường_dẫn_vào> -o <đường_dẫn_ra> -c <số_màu> -s <tỷ_lệ_kết_quả> [-t] [--remove-watermark] [--trim]
# hoặc trực tiếp bằng uvx
uvx --from "proper-pixel-art" ppa <đường_dẫn_vào> -o <đường_dẫn_ra> -c <số_màu> -s <tỷ_lệ_kết_quả> [-t]
```

#### Các Cờ (Flags)

| Cờ                               | Mô tả                                                                                               |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- |
| INPUT (vị trí)        | Tệp nguồn có phong cách pixel-art                                                                      |
| `-o`, `--output` `<đường_dẫn>`        | Thư mục đầu ra hoặc đường dẫn tệp cho kết quả. (mặc định: '.')                                                  |
| `-c`, `--colors` `<int>`         | Số lượng màu cho đầu ra (1-256). Bỏ qua để giữ nguyên tất cả các màu. Có thể cần thử vài giá trị khác nhau. (mặc định: None)                         |
| `-s`, `--scale-result` `<int>`     | Độ rộng/chiều cao của mỗi "pixel" trong kết quả. (mặc định: 1)                                                          |
| `-t`, `--transparent` `<bool>`   | Đầu ra có nền trong suốt. (mặc định: tắt)                                                        |
| `-u`, `--initial-upscale` `<int>` | Hệ số phóng to ảnh ban đầu. Tăng giá trị này có thể giúp phát hiện các cạnh pixel. (mặc định: 2)                    |
| `-w`, `--pixel-width` `<int>`    | Độ rộng của pixel trong ảnh đầu vào. Nếu không đặt, nó sẽ được xác định tự động. (mặc định: None)  |
| `--remove-watermark`             | Tự động phát hiện và xóa watermark do AI tạo ra (như Gemini) ở góc dưới bên phải.                                |
| `--trim`                         | Cắt bỏ phần viền trong suốt thừa xung quanh vật thể.                                                         |

#### Ví dụ

```bash
uv run ppa assets/blob/blob.png -c 16 -s 20 -t --remove-watermark --trim
```

### Python

```python
from PIL import Image
from proper_pixel_art.pixelate import pixelate

image = Image.open('path/to/input.png')
result = pixelate(image, num_colors=16, remove_watermark=True, trim=True)
result.save('path/to/output.png')
```

#### Tham số

- `image` : `PIL.Image.Image`
  - Một đối tượng ảnh PIL cần pixelate.

- `num_colors` : `int | None`
  - Số lượng màu trong kết quả (1-256). Bỏ qua để giữ nguyên màu sắc.
  - 8, 16, 32, hoặc 64 thường hoạt động tốt cho đầu ra nén màu.

- `initial_upscale` : `int`
  - Phóng to ảnh ban đầu để giúp phát hiện các đường lưới.

- `scale_result` : `int`
  - Phóng to kết quả sau khi thuật toán hoàn tất.

- `transparent_background` : `bool`
  - Nếu True, sẽ làm nền trong suốt dựa trên màu phổ biến nhất ở viền.

- `remove_watermark` : `bool`
  - Nếu True, tự động xóa watermark ở góc dưới bên phải.

- `trim` : `bool`
  - Nếu True, cắt bỏ phần viền trong suốt thừa.

#### Trả về

Một đối tượng ảnh PIL với độ phân giải pixel thực và màu sắc đã được tối ưu.

### Giao diện Web

Chạy cục bộ:

```bash
uv sync --extra web
uv run ppa-web
# Mở địa chỉ http://127.0.0.1:7860
```

## Thuật toán

Thuật toán chính giải quyết các thách thức bằng quy trình sau:

1) **Xóa Watermark & Cắt viền**: Loại bỏ nhãn hiệu AI và các pixel nhiễu ở rìa.
2) **Phóng to ban đầu**: Tăng kích thước ảnh để nhận diện lưới pixel chính xác hơn.
3) **Phát hiện cạnh (Canny)**: Tìm ranh giới của các khối màu.
4) **Dựng lưới (Mesh)**: Sử dụng biến đổi Hough để tìm tọa độ lưới pixel ngang và dọc.
5) **Lấy mẫu trung bình (Mean Downsampling)**: Tính toán màu trung bình của mỗi ô lưới để giữ nguyên cấu trúc hình khối khi nhìn từ xa.
6) **Nén màu (Quantization)**: Giảm số lượng màu về bảng màu mong muốn.
7) **Cắt gọn (Trim)**: Loại bỏ các khoảng trống không cần thiết xung quanh vật thể.

## Ví dụ kết quả

| Gốc (AI) | Lưới phát hiện | Kết quả thực |
| :---: | :---: | :---: |
| ![Bat](https://raw.githubusercontent.com/KennethJAllen/proper-pixel-art/main/assets/bat/bat.png) | ![Mesh](https://raw.githubusercontent.com/KennethJAllen/proper-pixel-art/main/assets/bat/mesh.png) | ![Result](https://raw.githubusercontent.com/KennethJAllen/proper-pixel-art/main/assets/bat/result.png) |

Dự án này giúp biến những bản nháp từ AI thành tài nguyên game chuyên nghiệp chỉ trong tích tắc!
