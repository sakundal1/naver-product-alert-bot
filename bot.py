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


def find_products(obj, products):

    # ----------------------------------------
    # 1. 딕셔너리
    # ----------------------------------------
    if isinstance(obj, dict):

        # 상품 데이터 발견
        if "productName" in obj and "productId" in obj:

            product_id = obj.get("productId")
            product_name = obj.get("productName")

            if product_id is not None and product_name:

                product_id = str(product_id)

                # 중복 제거
                if not any(
                    p["product_id"] == product_id
                    for p in products
                ):

                    product_url = None

                    click_info = obj.get("productClickUrl")

                    if isinstance(click_info, dict):
                        product_url = click_info.get("pcUrl")

                    elif isinstance(click_info, str):
                        product_url = click_info

                    products.append({
                        "product_id": product_id,
                        "name": product_name,
                        "price": obj.get("salePrice"),
                        "mall": obj.get("mallName"),
                        "url": product_url,
                    })

        # 내부 데이터 계속 탐색
        for value in obj.values():
            find_products(value, products)

    # ----------------------------------------
    # 2. 리스트
    # ----------------------------------------
    elif isinstance(obj, list):

        for item in obj:
            find_products(item, products)

    # ----------------------------------------
    # 3. JSON 문자열
    # ----------------------------------------
    elif isinstance(obj, str):

        text = obj.strip()

        # JSON처럼 보이는 문자열만 검사
        if (
            (text.startswith("{") and text.endswith("}"))
            or
            (text.startswith("[") and text.endswith("]"))
        ):

            try:
                parsed = json.loads(text)
                find_products(parsed, products)

            except Exception:
                pass


def get_products():

    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS,
        timeout=30
    )

    print("HTTP 상태 코드:", response.status_code)
    print("응답 크기:", len(response.text))

    response.raise_for_status()

    data = response.json()

    products = []

    find_products(data, products)

    return products


def main():

    print("=" * 60)
    print("네이버 상품 검색 테스트")
    print("=" * 60)

    print()
    print("검색어:", QUERY)
    print("상품 정보 가져오는 중...")
    print()

    try:

        products = get_products()

        print()
        print("=" * 60)
        print("찾은 상품 수:", len(products))
        print("=" * 60)

        if len(products) == 0:

            print()
            print("⚠️ 아직 상품을 찾지 못했습니다.")
            print()
            print("네이버 응답은 정상적으로 받았습니다.")
            print("상품 데이터 구조를 추가로 확인해야 합니다.")

        else:

            for i, product in enumerate(products, start=1):

                print()
                print(f"[{i}]")
                print("-" * 40)

                print("상품명:", product["name"])

                price = product["price"]

                if price is not None:
                    try:
                        print("가격:", f"{int(price):,}원")
                    except Exception:
                        print("가격:", price)
                else:
                    print("가격: 확인 불가")

                print("판매처:", product["mall"])
                print("상품 ID:", product["product_id"])
                print("상품 URL:", product["url"])

        print()
        print("=" * 60)
        print("✅ 테스트 완료")
        print("=" * 60)

    except Exception as e:

        print()
        print("=" * 60)
        print("❌ 오류 발생")
        print("=" * 60)

        print(type(e).__name__, e)


if __name__ == "__main__":
    main()
