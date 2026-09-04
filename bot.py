import requests
import json

QUERY = "리프트바운드"

URL = "https://ns-portal.shopping.naver.com/api/v2/shopping-paged-slot"

PARAMS = {
    "query": QUERY,
    "source": "shp_gui",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://search.shopping.naver.com/",
}


def inspect_data(obj, path="data", depth=0):

    # 너무 깊게 내려가지 않음
    if depth > 10:
        return

    # 딕셔너리
    if isinstance(obj, dict):

        keys = list(obj.keys())

        # 상품 관련 키가 있는지 확인
        product_keys = [
            "productName",
            "productId",
            "mallName",
            "salePrice",
            "productClickUrl"
        ]

        found = [key for key in product_keys if key in obj]

        if found:
            print()
            print("=" * 60)
            print("🔎 상품 관련 데이터 발견!")
            print("=" * 60)

            print("위치:", path)
            print("발견한 키:", found)

            for key in found:
                value = obj.get(key)

                print()
                print(f"{key}:")
                print(str(value)[:1000])

        # 하위 데이터 탐색
        for key, value in obj.items():
            inspect_data(
                value,
                f"{path}.{key}",
                depth + 1
            )

    # 리스트
    elif isinstance(obj, list):

        for i, item in enumerate(obj):
            inspect_data(
                item,
                f"{path}[{i}]",
                depth + 1
            )

    # 문자열 안에 JSON이 들어있는 경우
    elif isinstance(obj, str):

        text = obj.strip()

        if len(text) < 2:
            return

        # 문자열 안에 productName이 있는지 먼저 확인
        if "productName" in text or "productId" in text:

            print()
            print("=" * 60)
            print("🔎 상품 데이터가 문자열 안에서 발견!")
            print("=" * 60)

            print("위치:", path)

            # 상품명 주변 내용 출력
            index = text.find("productName")

            if index >= 0:
                start = max(0, index - 300)
                end = min(len(text), index + 1500)

                print()
                print(text[start:end])

        # JSON 문자열이면 다시 파싱
        if (
            (text.startswith("{") and text.endswith("}"))
            or
            (text.startswith("[") and text.endswith("]"))
        ):

            try:
                parsed = json.loads(text)

                inspect_data(
                    parsed,
                    path + " → JSON문자열",
                    depth + 1
                )

            except Exception:
                pass


def main():

    print("=" * 60)
    print("네이버 쇼핑 데이터 구조 진단")
    print("=" * 60)

    print()
    print("검색어:", QUERY)
    print("데이터 요청 중...")
    print()

    try:

        response = requests.get(
            URL,
            params=PARAMS,
            headers=HEADERS,
            timeout=30
        )

        print("HTTP 상태 코드:", response.status_code)
        print("응답 크기:", len(response.text))

        response.raise_for_status()

        # 원본 응답에서 상품 키가 존재하는지도 확인
        print()
        print("=" * 60)
        print("원본 응답 확인")
        print("=" * 60)

        if "productName" in response.text:
            print("✅ 원본 응답에 productName이 존재합니다.")
        else:
            print("❌ 원본 응답에 productName이 없습니다.")

        if "productId" in response.text:
            print("✅ 원본 응답에 productId가 존재합니다.")
        else:
            print("❌ 원본 응답에 productId가 없습니다.")

        # JSON 변환
        data = response.json()

        print()
        print("JSON 변환 성공")
        print("최상위 타입:", type(data).__name__)

        if isinstance(data, dict):
            print("최상위 키:", list(data.keys()))

        elif isinstance(data, list):
            print("리스트 길이:", len(data))

        print()
        print("=" * 60)
        print("상품 데이터 위치 탐색 시작")
        print("=" * 60)

        inspect_data(data)

        print()
        print("=" * 60)
        print("✅ 진단 완료")
        print("=" * 60)

    except Exception as e:

        print()
        print("=" * 60)
        print("❌ 오류 발생")
        print("=" * 60)

        print(type(e).__name__, e)


if __name__ == "__main__":
    main()
