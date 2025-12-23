#!/usr/bin/env python3
"""
상세페이지 이미지 최적화 스크립트
- 긴 이미지를 그리드 형태로 분할/배치
- 메인 이미지 (정사각형) 생성
- 상세 이미지 (600px 이상 x 3000px 이하) 생성
"""

from PIL import Image
import os
import math

def create_grid_image(image_path, output_path, rows, cols, max_height=3000):
    """
    긴 이미지를 그리드 형태로 분할하여 배치

    Args:
        image_path: 원본 이미지 경로
        output_path: 출력 이미지 경로
        rows: 행 수
        cols: 열 수
        max_height: 최대 세로 크기
    """
    print(f"처리 중: {os.path.basename(image_path)}")

    # 원본 이미지 로드
    img = Image.open(image_path)
    width, height = img.size
    print(f"  원본 크기: {width} x {height}px")

    # 분할 개수
    num_pieces = rows * cols
    piece_height = height // num_pieces

    print(f"  분할: {num_pieces}조각 ({rows}행 x {cols}열)")
    print(f"  각 조각 크기: {width} x {piece_height}px")

    # 각 조각의 최종 크기 계산 (세로를 max_height에 맞춤)
    final_piece_height = max_height // rows
    scale_ratio = final_piece_height / piece_height
    final_piece_width = int(width * scale_ratio)

    print(f"  축소 후 조각 크기: {final_piece_width} x {final_piece_height}px")

    # 최종 캔버스 크기
    final_width = final_piece_width * cols
    final_height = final_piece_height * rows

    print(f"  최종 이미지 크기: {final_width} x {final_height}px")

    # 새 캔버스 생성
    result = Image.new('RGBA', (final_width, final_height), (255, 255, 255, 0))

    # 조각 분할 및 배치
    for i in range(num_pieces):
        row = i // cols
        col = i % cols

        # 조각 추출
        y_start = i * piece_height
        y_end = min((i + 1) * piece_height, height)
        piece = img.crop((0, y_start, width, y_end))

        # 리사이즈
        piece_resized = piece.resize(
            (final_piece_width, final_piece_height),
            Image.Resampling.LANCZOS
        )

        # 배치
        x_pos = col * final_piece_width
        y_pos = row * final_piece_height
        result.paste(piece_resized, (x_pos, y_pos))

    # 저장
    result.save(output_path, 'PNG', optimize=True)
    print(f"  ✅ 저장 완료: {output_path}")
    print()

    return result

def create_main_image(image_path, output_path, size=800):
    """
    메인 이미지 생성 (정사각형, 1:1 비율)

    Args:
        image_path: 원본 이미지 경로
        output_path: 출력 이미지 경로
        size: 정사각형 크기 (기본 800px)
    """
    print(f"메인 이미지 생성 중: {os.path.basename(image_path)}")

    img = Image.open(image_path)
    width, height = img.size

    # 상단에서 정사각형 영역 추출
    crop_size = min(width, size * 4)  # 원본에서 충분히 큰 영역 추출
    cropped = img.crop((0, 0, crop_size, crop_size))

    # 리사이즈
    result = cropped.resize((size, size), Image.Resampling.LANCZOS)

    # 저장
    result.save(output_path, 'PNG', optimize=True)
    print(f"  ✅ 메인 이미지 저장: {size} x {size}px -> {output_path}")
    print()

    return result

def main():
    # 출력 디렉토리 생성
    output_dir = "optimized"
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("상세페이지 이미지 최적화 시작")
    print("=" * 60)
    print()

    # 1. PT4_상세페이지_제작.png 처리 (3x4 그리드)
    pt4_input = "PT4_상세페이지_제작.png"
    pt4_output = os.path.join(output_dir, "PT4_detail.png")
    pt4_main = os.path.join(output_dir, "PT4_main.png")

    if os.path.exists(pt4_input):
        create_grid_image(pt4_input, pt4_output, rows=4, cols=3, max_height=3000)
        create_main_image(pt4_input, pt4_main, size=800)

    # 2. Component 17.png 처리 (3x2 그리드)
    comp_input = "Component 17.png"
    comp_output = os.path.join(output_dir, "Component17_detail.png")
    comp_main = os.path.join(output_dir, "Component17_main.png")

    if os.path.exists(comp_input):
        create_grid_image(comp_input, comp_output, rows=2, cols=3, max_height=3000)
        create_main_image(comp_input, comp_main, size=800)

    print("=" * 60)
    print("✅ 모든 이미지 처리 완료!")
    print("=" * 60)
    print()
    print(f"결과 파일 위치: {output_dir}/")
    print()
    print("생성된 파일:")
    for f in sorted(os.listdir(output_dir)):
        filepath = os.path.join(output_dir, f)
        size = os.path.getsize(filepath) / 1024 / 1024  # MB
        print(f"  - {f} ({size:.2f} MB)")

if __name__ == "__main__":
    main()
