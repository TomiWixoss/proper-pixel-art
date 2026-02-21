# Các Script Tạo Ảnh Pixel Art

Các script để tạo ảnh pixel art bằng cách sử dụng các mô hình AI.

## ppa-gen

Tạo ảnh pixel art bằng API gpt-image-1.5 của OpenAI và tự động pixelate chúng bằng thư viện proper-pixel-art.

### Cài đặt

#### Cài đặt các gói phụ thuộc

```bash
uv sync --extra scripts
```

#### Cấu hình môi trường

1. [Tạo khóa API mới](https://platform.openai.com/api-keys)
2. Tạo tệp `.env` trong thư mục gốc của dự án
3. Thêm khóa API của bạn vào `.env`:
4. `OPENAI_API_KEY=sk-your-api-key-here`

### Cách sử dụng

#### Cách dùng cơ bản

```bash
uv run ppa-gen --prompt "Một chú mèo pixel art 16 bit dễ thương"
```

#### Với các tùy chọn bổ sung

```bash
uv run ppa-gen \
  --prompt "Một nhân vật robot pixel art 16 bit với nền trong suốt" \
  --scale-result 10 \
  --transparent \
  --n 2
```

### Tùy chọn dòng lệnh

#### Tùy chọn OpenAI API

| Cờ | Kiểu | Mặc định | Mô tả |
|------|------|---------|-------------|
| `--prompt` | str | (bắt buộc) | Mô tả bằng văn bản để tạo ảnh |
| `--size` | str | 1024x1024 | Kích thước ảnh: '1024x1024', '1024x1536', hoặc '1536x1024' |
| `--n` | int | 1 | Số lượng ảnh cần tạo (1-10) |

#### Tùy chọn Pixelation

| Cờ | Kiểu | Mặc định | Mô tả |
|------|------|---------|-------------|
| `-c`, `--colors` | int | None | Số lượng màu (1-256). Bỏ qua để giữ nguyên tất cả các màu |
| `-s`, `--scale-result` | int | 1 | Độ rộng của từng pixel trong ảnh kết quả |
| `-t`, `--transparent` | cờ | False | Tạo nền trong suốt |
| `-w`, `--pixel-width` | int | None | Độ rộng của pixel trong đầu vào (tự động phát hiện nếu bỏ qua) |
| `-u`, `--initial-upscale` | int | 2 | Hệ số phóng to ban đầu để phát hiện lưới |

#### Tùy chọn đầu ra

| Cờ | Kiểu | Mặc định | Mô tả |
|------|------|---------|-------------|
| `-o`, `--output-dir` | path | '.' | Thư mục cho các ảnh được tạo |

### Tệp đầu ra

Các tệp được tạo được đặt tên theo mốc thời gian, kết thúc bằng `original.png` cho ảnh AI gốc và `pixelated.png` cho phiên bản đã pixelated.

### Mẹo để có kết quả tốt nhất

- Yêu cầu "16 bit pixel art" cho các ảnh pixel art căn chỉnh theo lưới tốt hơn.
- Yêu cầu nền trong suốt khi tạo nhân vật để làm nền (background) biến mất.

### Ví dụ

```uv run ppa-gen --prompt "Một khối blob pixel art 16 bit với nền trong suốt"```

<table align="center" width="100%">
  <tr>
    <td width="33%">
      <img src="https://raw.githubusercontent.com/KennethJAllen/proper-pixel-art/main/assets/blob/blob.png" style="width:100%;" />
      <br><small>Độ phân giải cao, bị nhiễu</small>
    </td>
    <td width="33%">
      <img src="https://raw.githubusercontent.com/KennethJAllen/proper-pixel-art/main/assets/blob/result.png" style="width:100%;" />
      <br><small>Độ phân giải pixel thực</small>
    </td>
  </tr>
</table>

Xem tệp README chính của dự án để biết thêm ví dụ.