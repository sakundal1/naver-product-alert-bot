import requests
import json

QUERY = "리프트바운드"

URL = "https://search.shopping.naver.com/api/search/all"

PARAMS = {
    "sort": "date",
    "pagingIndex": 1,
    "pagingSize": 40,
    "viewType": "list",
    "productSet": "total",
    "query": QUERY,
    "origQuery": QUERY,
    "adQuery": QUERY,
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


def main():
    print("=" * 60)
    print("네이버 쇼핑 API 테스트")
    print("=" * 60)

    print(f"\n검색어: {QUERY}")
    print("네이버 쇼핑 데이터 요청 중...")

    try:
        response = requests.get(
            URL,
            params=PARAMS,
            headers=HEADERS,
            timeout=30
        )

        print("\nHTTP 상태 코드:", response.status_code)
        print("응답 크기:", len(response.text))

        print("\n응답 앞부분:")
        print(response.text[:1000])

        if response.status_code != 200:
            print("\n❌ 요청 실패")
            return

        try:
            data = response.json()
        except Exception:
            print("\n❌ JSON 형식이 아닙니다.")
            return

        print("\n✅ JSON 응답 확인!")

        # 응답 구조 확인
        print("\n최상위 데이터:")
        print(data.keys())

        # 상품 데이터 찾기
        shopping_result = data.get("shoppingResult", {})

        products = shopping_result.get("products", [])

        print("\n상품 개수:", len(products))

        if not products:
            print("\n⚠️ 상품 데이터가 없습니다.")
            print("\n응답 구조를 확인하기 위해 JSON 일부를 출력합니다.")
            print(json.dumps(data, ensure_ascii=False)[:5000])
            return

        print("\n" + "=" * 60)
        print("상품 목록")
        print("=" * 60)

        for i, product in enumerate(products[:10], start=1):
            print(f"\n[{i}]")

            print("상품명:", product.get("productTitle"))
            print("가격:", product.get("price"))
            print("판매처:", product.get("mallName"))
            print("상품 ID:", product.get("productId"))
            print("상품 URL:", product.get("productUrl"))

        print("\n" + "=" * 60)
        print("✅ 테스트 완료")
        print("=" * 60)

    except Exception as e:
        print("\n❌ 오류 발생:")
        print(type(e).__name__, e)


if __name__ == "__main__":
    main()
