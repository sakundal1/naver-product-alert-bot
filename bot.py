from playwright.sync_api import sync_playwright

URL = "https://search.shopping.naver.com/search/all?query=%EB%A6%AC%ED%94%84%ED%8A%B8%EB%B0%94%EC%9A%B4%EB%93%9C&sort=date&pagingIndex=1&pagingSize=40&productSet=total&viewType=list"


def main():
    print("네이버 가격비교 페이지 접속을 시작합니다.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={
                "width": 1920,
                "height": 1080
            }
        )

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print("페이지 제목:", page.title())
        print("현재 URL:", page.url)

        browser.close()

    print("테스트 완료!")


if __name__ == "__main__":
    main()
