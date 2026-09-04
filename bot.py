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


def main():
    print("=" * 60)
    print("네이버 쇼핑 공개 JSON 테스트")
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
        print(response.text[:3000])

        if response.status_code != 200:
            print("\n❌ 요청 실패")
            return

        try:
            data = response.json()
        except Exception:
            print("\n❌ JSON 응답이 아닙니다.")
            return

        print("\n✅ JSON 응답 확인!")

        print("\n데이터 구조:")
        print(json.dumps(data, ensure_ascii=False)[:5000])

        print("\n" + "=" * 60)
        print("✅ 1차 테스트 성공")
        print("=" * 60)

    except Exception as e:
        print("\n❌ 오류 발생")
        print(type(e).__name__, e)


if __name__ == "__main__":
    main()
