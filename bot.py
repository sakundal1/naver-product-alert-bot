import requests

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
    """
    JSON 전체를 돌아다니면서
    productName + productId가 있는 상품 데이터를 찾는다.
    """

    if isinstance(obj, dict):

        # 상품 데이터인지 확인
        if "productName" in obj and "productId" in obj:

            product_name = obj.get("productName")
            product_id = obj.get("productId")

            # 중복 방지
            if product_id is not None:

                product_id = str(product_id)

                if not any(
                    p["product_id"] == product_id
                    for p in products
                ):

                    click_info = obj.get("productClickUrl")

                    product_url = None

                    if isinstance(click_info, dict):
                        product_url = click_info.get("pcUrl")

                    products.append({
                        "product_id": product_id,
                        "name": product_name,
                        "price": obj.get("salePrice"),
                        "mall": obj.get("mallName"),
                        "url": product_url,
                    })

        # 모든 하위 데이터 계속 검색
        for value in obj.values():
            find_products(value, products)

    elif isinstance(obj, list):

        for item in obj:
            find_products(item, products)


def get_products():

    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS,
        timeout=30
    )

    print("HTTP 상태 코드:", response.status_code)

    response.raise_for_status()

    data = response.json()

    products = []

    # JSON 전체를 탐색
    find_products(data, products)

    return products


def main():

    print("=" * 60)
    print("네이버 상품 검색 결과")
    print("=" * 60)

    print()
    print("검색어:", QUERY)
    print("상품 정보 가져오는 중...")
    print()

    try:

        products = get_products()

        print("=" * 60)
        print("찾은 상품 수:", len(products))
        print("=" * 60)

        if not products:
            print()
            print("⚠️ 상품을 찾지 못했습니다.")
            print("네이버 응답은 정상적으로 받았지만")
            print("상품 데이터 구조가 예상과 다를 수 있습니다.")

        for i, product in enumerate(products, start=1):

            print()
            print(f"[{i}]")

            print("상품명:", product["name"])

            price = product["price"]

            if price is not None:

                try:
                    print("가격:", f"{int(price):,}원")
                except:
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
