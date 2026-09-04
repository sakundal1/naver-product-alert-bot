import requests
import re
import os

QUERY = "리프트바운드"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
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

def send_discord_message(message):

    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={
            "content": message
        },
        timeout=30
    )

    print("디스코드 응답 코드:", response.status_code)

    response.raise_for_status()

def clean_product_name(name):
    """네이버 검색어 강조용 <mark> 태그 제거"""

    if not name:
        return ""

    name = re.sub(r"<mark>", "", name)
    name = re.sub(r"</mark>", "", name)

    return name


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

    # 실제 네이버 구조
    result_data = data.get("data", [])

    if not result_data:
        return products

    first_result = result_data[0]

    slots = first_result.get("slots", [])

    for slot in slots:

        product = slot.get("data", {})

        if not isinstance(product, dict):
            continue

        product_name = product.get("productName")

        if not product_name:
            continue

        # 상품 ID
        product_benefit = product.get("productBenefit", {})

        product_id = None

        if isinstance(product_benefit, dict):
            product_id = product_benefit.get("productId")

        if product_id is None:
            continue

        # 상품 URL
        product_click_url = product.get(
            "productClickUrl",
            {}
        )

        product_url = None

        if isinstance(product_click_url, dict):
            product_url = product_click_url.get("pcUrl")

        # 상품명 정리
        product_name = clean_product_name(product_name)

        # 가격
        sale_price = product.get("salePrice")

        # 판매처
        mall_name = product.get("mallName")

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
    print("네이버 쇼핑 상품 추출")
    print("=" * 60)

    print()
    print("검색어:", QUERY)
    send_discord_message(
    f"🟢 네이버 쇼핑 알림 봇 테스트\n검색어: {QUERY}\n\n봇이 정상적으로 디스코드에 연결되었습니다."
)
    print("상품 정보 가져오는 중...")
    print()

    try:

        products = get_products()

        print()
        print("=" * 60)
        print("상품 수:", len(products))
        print("=" * 60)

        for i, product in enumerate(products, start=1):

            print()
            print(f"[{i}]")
            print("-" * 50)

            print("상품명:", product["name"])

            if product["price"] is not None:
                print(
                    "가격:",
                    f"{int(product['price']):,}원"
                )
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
