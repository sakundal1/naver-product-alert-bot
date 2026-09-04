from playwright.sync_api import sync_playwright

URL = "https://search.shopping.naver.com/search/all?query=%EB%A6%AC%ED%94%84%ED%8A%B8%EB%B0%94%EC%9A%B4%EB%93%9C&sort=date&pagingIndex=1&pagingSize=40&productSet=total&viewType=list"

SEARCH_WORD = "리프트바운드"


def main():
    print("=" * 60)
    print("네이버 가격비교 상품 추출 테스트")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={
                "width": 1920,
                "height": 1080
            },
            locale="ko-KR"
        )

        print("\n[1] 네이버 접속 중...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(7000)

        print("[2] 페이지 로딩 완료")
        print("페이지 제목:", page.title())

        # 리프트바운드라는 글자가 들어간 링크 찾기
        links = page.locator("a")

        found = []

        for i in range(links.count()):
            try:
                link = links.nth(i)

                text = link.inner_text(timeout=1000).strip()
                href = link.get_attribute("href")

                if not text:
                    continue

                if SEARCH_WORD.lower() not in text.lower():
                    continue

                if not href:
                    continue

                # 상품 링크 주변의 텍스트 확인
                parent_text = ""

                try:
                    parent_text = link.locator(
                        "xpath=../../.."
                    ).inner_text(timeout=1000).strip()
                except:
                    pass

                found.append({
                    "title": text,
                    "href": href,
                    "parent_text": parent_text
                })

            except:
                continue

        print("\n" + "=" * 60)
        print(f"검색어 '{SEARCH_WORD}' 관련 링크 발견: {len(found)}개")
        print("=" * 60)

        for number, item in enumerate(found[:40], start=1):

            print(f"\n--- 상품 후보 {number} ---")
            print("상품명:", item["title"])
            print("URL:", item["href"])

            if item["parent_text"]:
                print("주변 정보:")
                print(item["parent_text"][:1000])

        print("\n" + "=" * 60)
        print("테스트 완료")
        print("=" * 60)

        browser.close()


if __name__ == "__main__":
    main()
