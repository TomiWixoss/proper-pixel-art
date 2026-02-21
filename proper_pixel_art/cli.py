"""Command line interface"""

import argparse
from pathlib import Path

from PIL import Image

from proper_pixel_art import pixelate


def add_pixelation_args(
    parser: argparse.ArgumentParser, group_name: str = "Tùy chọn Pixelation"
) -> argparse.ArgumentParser:
    """Add common pixelation arguments to an argument parser.

    Args:
        parser: The argument parser to add arguments to
        group_name: Name of the argument group (default: "Pixelation options")

    Returns:
        The parser with pixelation arguments added
    """
    pixel_group = parser.add_argument_group(group_name)
    pixel_group.add_argument(
        "-c",
        "--colors",
        dest="num_colors",
        type=int,
        default=None,
        help="Số lượng màu để nén ảnh (1-256). Bỏ qua để giữ nguyên tất cả các màu.",
    )
    pixel_group.add_argument(
        "-s",
        "--scale-result",
        dest="scale_result",
        type=int,
        default=1,
        help="Độ rộng của mỗi 'pixel' trong ảnh kết quả (mặc định: 1).",
    )
    pixel_group.add_argument(
        "-t",
        "--transparent",
        dest="transparent",
        action="store_true",
        default=False,
        help="Tạo nền trong suốt cho kết quả đầu ra.",
    )
    pixel_group.add_argument(
        "-w",
        "--pixel-width",
        dest="pixel_width",
        type=int,
        default=None,
        help="Độ rộng của pixel trong ảnh đầu vào. Nếu không đặt, nó sẽ được xác định tự động.",
    )
    pixel_group.add_argument(
        "-u",
        "--initial-upscale",
        dest="initial_upscale",
        type=int,
        default=2,
        help=(
            "Hệ số phóng to ảnh ban đầu trong thuật toán phát hiện lưới. "
            "Nếu khoảng cách lưới phát hiện quá lớn, "
            "việc tăng giá trị này có thể hữu ích."
        ),
    )
    pixel_group.add_argument(
        "--remove-watermark",
        dest="remove_watermark",
        action="store_true",
        default=False,
        help="Tự động phát hiện và xóa watermark do AI tạo ra (như Gemini) ở góc dưới bên phải.",
    )
    pixel_group.add_argument(
        "--trim",
        dest="trim",
        action="store_true",
        default=False,
        help="Cắt bỏ phần viền trong suốt xung quanh vật thể để kết quả vừa khít, không có pixel rỗng.",
    )
    return parser


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tạo ảnh pixel-art độ phân giải thực từ ảnh nguồn."
    )
    parser.add_argument(
        "input_path", type=Path, nargs="?", help="Đường dẫn đến tệp nguồn đầu vào."
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_path_flag",
        type=Path,
        help="Đường dẫn đến tệp nguồn đầu vào.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="out_path",
        type=Path,
        default=Path("."),
        help="Đường dẫn nơi ảnh pixelated sẽ được lưu. Có thể là thư mục hoặc đường dẫn tệp.",
    )

    # Add common pixelation arguments
    add_pixelation_args(parser)

    args = parser.parse_args()

    # Either take the input as the first argument or use the -i flag
    if args.input_path is None and args.input_path_flag is None:
        parser.error("Bạn phải cung cấp đường dẫn đầu vào (đối số hoặc qua flag -i).")
    args.input_path = (
        args.input_path if args.input_path is not None else args.input_path_flag
    )

    return args


def resolve_output_path(
    out_path: Path, input_path: Path, suffix: str = "_pixelated"
) -> Path:
    """
    If outpath is a directory, make it a file path
    with filename e.g. (input stem)_pixelated.png
    """
    if out_path.suffix:
        return out_path
    filename = f"{input_path.stem}{suffix}.png"
    return out_path / filename


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path).expanduser()

    out_path = resolve_output_path(Path(args.out_path), input_path)
    out_path.parent.mkdir(exist_ok=True, parents=True)

    img = Image.open(input_path)
    pixelated = pixelate.pixelate(
        img,
        num_colors=args.num_colors,
        scale_result=args.scale_result,
        transparent_background=args.transparent,
        pixel_width=args.pixel_width,
        initial_upscale_factor=args.initial_upscale,
        remove_watermark=args.remove_watermark,
        trim=args.trim,
    )

    pixelated.save(out_path)


if __name__ == "__main__":
    main()
