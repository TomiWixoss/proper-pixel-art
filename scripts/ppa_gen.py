#!/usr/bin/env python3
"""Generate pixel art images using OpenAI's gpt-image-1.5 API and pixelate them."""

import argparse
import base64
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

from proper_pixel_art.cli import add_pixelation_args
from proper_pixel_art.pixelate import pixelate


def load_api_key() -> str:
    """Load OpenAI API key from .env file."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Không tìm thấy OPENAI_API_KEY trong môi trường. "
            "Vui lòng tạo tệp .env với khóa API của bạn. "
            "Xem scripts/README.md để biết hướng dẫn cài đặt."
        )
    return api_key


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Tạo ảnh bằng gpt-image-1.5 của OpenAI và pixelate chúng.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Cách dùng cơ bản
  python scripts/ppa_gen.py --prompt "Một chú mèo pixel art dễ thương"

  # Với tất cả tùy chọn OpenAI
  python scripts/ppa_gen.py \\
    --prompt "Một lâu đài giả tưởng pixel art 16 bit" \\
    --size 1024x1024 \\
    --n 2

  # Với tùy chọn pixelation
  python scripts/ppa_gen.py \\
    --prompt "Một robot pixel art 16 bit" \\
    --colors 16 \\
    --scale-result 20 \\
    --transparent
        """,
    )

    # OpenAI API parameters
    openai_group = parser.add_argument_group("Tùy chọn OpenAI API")
    openai_group.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Mô tả văn bản để tạo hình ảnh.",
    )
    openai_group.add_argument(
        "--size",
        type=str,
        choices=["1024x1024", "1024x1536", "1536x1024", "auto"],
        default="1024x1024",
        help="Kích thước ảnh được tạo (mặc định: 1024x1024).",
    )
    openai_group.add_argument(
        "--n",
        type=int,
        choices=range(1, 11),
        default=1,
        help="Số lượng ảnh cần tạo (1-10, mặc định: 1).",
    )

    # Add common pixelation arguments
    add_pixelation_args(parser)

    # Output parameters
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        type=Path,
        default=Path("."),
        help="Thư mục đầu ra cho các ảnh được tạo (mặc định: thư mục hiện tại).",
    )

    return parser.parse_args()


def generate_images(client: OpenAI, args: argparse.Namespace) -> list[Image.Image]:
    """Generate images using OpenAI API."""
    print(f"Đang tạo {args.n} ảnh với prompt: '{args.prompt}'")
    print(f"Cấu hình: size={args.size}")

    response = client.images.generate(
        model="gpt-image-1.5",
        prompt=args.prompt,
        n=args.n,
        size=args.size,
    )

    # Convert base64 images to PIL Images
    images = []
    for image_data in response.data:
        image_bytes = base64.b64decode(image_data.b64_json)
        images.append(Image.open(BytesIO(image_bytes)))

    return images


def process_image(
    original_image: Image.Image,
    args: argparse.Namespace,
    timestamp: str,
    index: int = 0,
) -> tuple[Path, Path]:
    """Pixelate and save a single image."""
    print(f"Đang xử lý ảnh {index + 1}...")

    # Generate filenames
    suffix = f"_{index}" if args.n > 1 else ""
    original_filename = f"{timestamp}{suffix}_original.png"
    pixelated_filename = f"{timestamp}{suffix}_pixelated.png"

    original_path = args.output_dir / original_filename
    pixelated_path = args.output_dir / pixelated_filename

    # Save original
    original_image.save(original_path)
    print(f"Đã lưu ảnh gốc: {original_path}")

    # Pixelate
    print(f"Đang pixelate ảnh {index + 1}...")
    pixelated_image = pixelate(
        original_image,
        num_colors=args.num_colors,
        initial_upscale_factor=args.initial_upscale,
        scale_result=args.scale_result,
        transparent_background=args.transparent,
        pixel_width=args.pixel_width,
    )

    # Save pixelated
    pixelated_image.save(pixelated_path)
    print(f"Đã lưu ảnh pixelated: {pixelated_path}")

    return original_path, pixelated_path


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load API key and create client
    try:
        api_key = load_api_key()
        client = OpenAI(api_key=api_key)
    except ValueError as e:
        print(f"Lỗi: {e}")
        return

    # Generate timestamp for this batch
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        # Generate images via OpenAI API
        images = generate_images(client, args)

        # Process each image
        for i, img in enumerate(images):
            process_image(img, args, timestamp, i)

        print(f"\nĐã xử lý thành công {len(images)} ảnh")
        print(f"Thư mục đầu ra: {args.output_dir.absolute()}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()
