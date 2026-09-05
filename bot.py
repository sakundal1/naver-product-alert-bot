import requests
import re
import os
import json


# ============================================================
# 설정
# ============================================================

QUERIES = [
    "리프트바운드",
    "디지몬 카드",
    "원피스 카드",
]

PRICE_LIMITS = {
    "리프트바운드": 130000,
    "디지몬 카드": 55000,
    "원피스 카드": 55000,
}

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

NAVER_URL = "https://ns-portal.shopping.naver.com/api/v2/shopping-paged-slot"


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

SEEN_FILE = "seen_products.json"


# ============================================================
# 상품명 정리
# ============================================================

def clean_product_name(name):

    if not name:
        return ""

    name = re.sub(r"<mark>", "", name)
    name = re.sub(r"</mark>", "", name)

    return name


# ============================================================
# 기존 상품 목록 불러오기
# ============================================================

def load_seen_products():

    if not os.path.exists(SEEN_FILE):
        return set()

    try:

        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return set(str(product_id) for product_id in data)

        return set()

    except Exception as e:

        print("⚠️ 기존 상품 목록을 읽는 중 오류:", e)

        return set()


# ============================================================
# 확인한 상품 ID 저장
# ============================================================

def save_seen_products(seen_products):

    with open(SEEN_FILE, "w", encoding="utf-8") as f:

        json.dump(
            sorted(list(seen_products)),
            f,
            ensure_ascii=False,
            indent=2
        )


# ============================================================
# 디스코드 메시지 전송
# ============================================================

def send_discord_message(message):

    if not DISCORD_WEBHOOK_URL:

        print("❌ DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")

        return False

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={
            "content": message
        },
        timeout=30
    )

    print("디스코드 응답 코드:", response.status_code)

    response.raise_for_status()

    return True


# ============================================================
# 네이버 상품 가져오기
# ============================================================

def get_products(query):

    params = {
        "query": query,
        "source": "shp_gui",
    }

    response = requests.get(
        NAVER_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    print("HTTP 상태 코드:", response.status_code)

    response.raise_for_status()

    data = response.json()

    products = []

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

        product_benefit = product.get(
            "productBenefit",
            {}
        )

        product_id = None

        if isinstance(product_benefit, dict):

            product_id = product_benefit.get(
                "productId"
            )

        if product_id is None:

            product_id = product.get(
                "channelProductId"
            )

        if product_id is None:
            continue

        product_url_data = product.get(
            "productUrl",
            {}
        )

        product_url = None

        if isinstance(product_url_data, dict):

            product_url = product_url_data.get(
                "pcUrl"
            )

        product_name = clean_product_name(
            product_name
        )

        sale_price = product.get(
            "salePrice"
        )

        mall_name = product.get(
            "mallName"
        )

        products.append({

            "product_id": str(product_id),

            "name": product_name,

            "price": sale_price,

            "mall": mall_name,

            "url": product_url,

            "query": query,

        })

    return products

    print("HTTP 상태 코드:", response.status_code)

    response.raise_for_status()

    data = response.json()

    products = []

    result_data = data.get("data", [])

    if not result_data:
        return products

    first_result = result_data[0]

    slots = first_result.get("slots", [])

    for slot in slots:

        product = slot.get("data", {})

        if not isinstance(product, dict):
            continue

        # ====================================================
        # 상품명
        # ====================================================

        product_name = product.get("productName")

        if not product_name:
            continue

        # ====================================================
        # 상품 ID
        # ====================================================

        product_benefit = product.get(
            "productBenefit",
            {}
        )

        product_id = None

        if isinstance(product_benefit, dict):

            product_id = product_benefit.get(
                "productId"
            )

        # productBenefit에 없으면 channelProductId 사용
        if product_id is None:

            product_id = product.get(
                "channelProductId"
            )

        if product_id is None:
            continue

        # ====================================================
        # 실제 상품 URL
        # ====================================================

        product_url_data = product.get(
            "productUrl",
            {}
        )

        product_url = None

        if isinstance(product_url_data, dict):

            product_url = product_url_data.get(
                "pcUrl"
            )

        # ====================================================
        # 상품명 정리
        # ====================================================

        product_name = clean_product_name(
            product_name
        )

        # ====================================================
        # 가격
        # ====================================================

        sale_price = product.get(
            "salePrice"
        )

        # ====================================================
        # 판매처
        # ====================================================

        mall_name = product.get(
            "mallName"
        )

        products.append({

            "product_id": str(product_id),

            "name": product_name,

            "price": sale_price,

            "mall": mall_name,

            "url": product_url,

        })

    return products


# ============================================================
# 디스코드 상품 알림
# ============================================================

def send_product_alert(product):

    name = product["name"]

    price = product["price"]

    mall = product["mall"]

    url = product["url"]

    if price is not None:

        price_text = f"{int(price):,}원"

    else:

        price_text = "가격 확인 불가"

    message = (
        "🚨 **네이버 쇼핑 새 상품 발견!**\n\n"
        f"🔎 검색어: `{product['query']}`\n\n"
        f"📦 **상품명**\n"
        f"{name}\n\n"
       price_limit = PRICE_LIMITS.get(product["query"])

if price_limit is not None:
    limit_text = f"{int(price_limit):,}원 이하"
else:
    limit_text = "제한 없음"

message = (
    "🚨 **네이버 쇼핑 새 상품 발견!**\n\n"
    f"🔎 검색어: `{product['query']}`\n\n"
    f"📦 **상품명**\n"
    f"{name}\n\n"
    f"💰 **가격:** {price_text}\n"
    f"🎯 **알림 기준:** {limit_text}\n"
    f"🏪 **판매처:** {mall}\n\n"
)
    )

    if url:

        message += (
            f"🔗 **상품 바로가기:** {url}"
        )

    else:

        message += (
            "🔗 상품 URL 확인 불가"
        )

    return send_discord_message(
        message
    )


# ============================================================
# 메인
# ============================================================

def main():

    print("=" * 60)
    print("네이버 쇼핑 상품 모니터")
    print("=" * 60)

    print()

    seen_products = load_seen_products()

    print(
        "기존에 확인한 상품 수:",
        len(seen_products)
    )

    print()

    all_products = []

    # ========================================================
    # 여러 검색어 검색
    # ========================================================

    for query in QUERIES:

        print("=" * 60)
        print("검색어:", query)
        print("=" * 60)

        try:

            products = get_products(query)

            print(
                "현재 상품 수:",
                len(products)
            )

            all_products.extend(products)

        except Exception as e:

            print(
                "❌ 상품 가져오기 실패:",
                query,
                type(e).__name__,
                e
            )

   # ========================================================
# 새 상품 찾기 + 가격 조건 확인
# ========================================================

new_products = []

current_product_ids = set()

for product in all_products:

    product_id = product["product_id"]

    query = product["query"]

    # 검색어별 가격 제한
    price_limit = PRICE_LIMITS.get(query)

    # 현재 상품 가격
    price = product["price"]

    # 검색어 + 상품 ID로 상품 구분
    seen_key = (
        query
        + "|"
        + product_id
    )

    # ====================================================
    # 가격 조건 확인
    # ====================================================

    if price is None:

        print(
            "⚠️ 가격 확인 불가:",
            product["name"]
        )

        continue

    # 가격 제한이 설정되어 있고
    # 기준보다 비싸면 알림하지 않음
    if price_limit is not None and price > price_limit:

        print(
            "💰 가격 초과:",
            product["name"],
            f"({int(price):,}원)",
            f"→ 기준 {int(price_limit):,}원"
        )

        continue

    # ====================================================
    # 가격 조건을 만족한 상품만 확인 목록에 저장
    # ====================================================

    current_product_ids.add(
        seen_key
    )

    # 아직 알림하지 않은 상품이면 새 상품
    if seen_key not in seen_products:

        new_products.append(
            product
        )

    print()

    print("=" * 60)
    print(
        "전체 검색 상품 수:",
        len(all_products)
    )

    print(
        "새 상품 수:",
        len(new_products)
    )

    print("=" * 60)

    # ========================================================
    # 첫 실행
    # ========================================================

    if len(seen_products) == 0:

        print()

        print(
            "ℹ️ 첫 실행입니다."
        )

        print(
            "현재 상품을 기준 목록으로 저장합니다."
        )

        print(
            "첫 실행에서는 디스코드 알림을 보내지 않습니다."
        )

        print()

        save_seen_products(
            current_product_ids
        )

        return

    # ========================================================
    # 새 상품 디스코드 알림
    # ========================================================

    if new_products:

        print()

        print(
            "🚨 새로운 상품을 발견했습니다!"
        )

        print()

        for product in new_products:

            print(
                "알림 전송:",
                product["name"]
            )

            try:

                send_product_alert(
                    product
                )

                print(
                    "✅ 디스코드 알림 전송 성공"
                )

            except Exception as e:

                print(
                    "❌ 디스코드 알림 전송 실패:",
                    e
                )

    else:

        print()

        print(
            "현재 새로운 상품이 없습니다."
        )

    # ========================================================
    # 현재 상품을 확인 목록에 추가
    # ========================================================

    seen_products.update(
        current_product_ids
    )

    save_seen_products(
        seen_products
    )

    print()

    print(
        "현재 저장된 상품 수:",
        len(seen_products)
    )

    print()

    print("=" * 60)

    print(
        "✅ 모니터링 완료"
    )

    print("=" * 60)


# ============================================================
# 실행
# ============================================================

if __name__ == "__main__":

    main()
