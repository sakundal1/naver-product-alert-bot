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

    # 네이버 응답 구조
    result_data = data.get("data", {})
    slots = result_data.get("slots", [])

    for slot in slots:
        product = slot.get("data", {})

        # 상품 카드만 추출
        if product.get("cardType") != "ORGANIC_CARD":
            continue

        product_name = product.get("productName")
        product_id = product.get("productId")
        mall_name = product.get("mallName")
        sale_price = product.get("salePrice")
        product_url = product.get("productClickUrl", {}).get("pcUrl")

        if not product_name or not product_id:
            continue

        products.append({
            "product_id": str(product_id),
            "name": product_name,
            "price": sale_price,
            "mall": mall_name,
            "url": product_url,
        })

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
        print(f"상품 수: {len(products)}")
        print("=" * 60)

        for i, product in enumerate(products, start=1):
            print()
            print(f"[{i}]")
            print("상품명:", product["name"])

            price = product["price"]

            if price is not None:
                print("가격:", f"{int(price):,}원")
            else:
                print("가격: 확인 불가")

            print("판매처:", product["mall"])
            print("상품 ID:", product["product_id"])
            print("상품 URL:", product["url"])

        print()
        print("=" * 60)
        print("✅ 상품 추출 성공")
        print("=" * 60)

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 오류 발생")
        print("=" * 60)
        print(type(e).__name__, e)


if __name__ == "__main__":
    main()
