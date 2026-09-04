from playwright.sync_api import sync_playwright

URL = "https://search.shopping.naver.com/search/all?query=%EB%A6%AC%ED%94%84%ED%8A%B8%EB%B0%94%EC%9A%B4%EB%93%9C&sort=date&pagingIndex=1&pagingSize=40&productSet=total&viewType=list"

def main():
    print("=" * 60)
    print("네이버 자동 접속 테스트")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1920,
                "height": 1080
            },
            locale="ko-KR",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/150.0.0.0 Safari/537.36"
            )
        )

        print("\n[1] 네이버 접속 중...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("[2] 페이지 로딩 완료")

        page.wait_for_timeout(10000)

        print("\n페이지 제목:")
        print(page.title())

        print("\n현재 URL:")
        print(page.url)

        body_text = page.locator("body").inner_text()

        print("\n" + "=" * 60)
        print("페이지에서 읽은 텍스트")
        print("=" * 60)

        print(body_text[:10000])

        print("\n" + "=" * 60)
        print("리프트바운드 포함 여부")
        print("=" * 60)

        if "리프트바운드" in body_text:
            print("✅ 리프트바운드가 페이지에 존재합니다.")
        else:
            print("❌ 리프트바운드가 페이지에 없습니다.")

        print("\n페이지 HTML 길이:", len(page.content()))

        browser.close()

    print("\n테스트 완료!")


if __name__ == "__main__":
    main()
