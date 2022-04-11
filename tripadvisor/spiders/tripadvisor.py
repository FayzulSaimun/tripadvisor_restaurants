from bs4 import BeautifulSoup
import scrapy


class TripSpider(scrapy.Spider):
    name = "tripadvisor"
    start_urls = [
        "https://www.tripadvisor.com.au/Restaurant_Review-g187457-d805520-Reviews-Arzak-San_Sebastian_Donostia_Province_of_Guipuzcoa_Basque_Country.html"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        # Identify all reviews element as List
        boxes = soup.find_all("div", class_="rev_wrap ui_columns is-multiline")

        if len(boxes) != 0:
            # all single page json data will store in this List
            print("Got Reviews")
            page_datas = []
            for box in boxes:
                # print(box)
                # sys.quit()
                # Single Datas Get from a Single Id
                try:
                    id_ = box.select_one('div[class="quote isNew"]>a').get("id")
                except Exception as e:
                    try:
                        id_ = box.select_one('div[class="quote"]>a').get("id")
                    except Exception as e:
                        # print(e)
                        id_ = "N/A"

                try:
                    author = box.select_one(
                        'div[class="info_text pointer_cursor"]>div'
                    ).text.strip()
                except Exception as e:
                    # print(e)
                    author = "N/A"

                try:
                    profile_picture = box.select_one(
                        'div[class="ui_avatar resp"]>img'
                    ).get("data-lazyurl")
                except Exception as e:
                    # print(e)
                    profile_picture = "N/A"

                try:
                    content_title = box.select_one(
                        'span[class="noQuotes"]'
                    ).text.strip()
                except Exception as e:
                    # print(e)
                    content_title = "N/A"

                try:
                    content = box.select_one('p[class="partial_entry"]').text.strip()
                    if content[-4:] == "More":
                        content = content[:-4]
                except Exception as e:
                    # print(e)
                    content = "N/A"

                try:
                    rating_text = "".join(
                        box.select_one(
                            'div[class="ui_column is-9"]>span[class*="ui_bubble_ratin"]'
                        ).get("class")
                    )
                    rating = rating_text[-2]
                except Exception as e:
                    # print(e)
                    rating = "N/A"

                try:
                    reviewed_at = (
                        box.select_one(
                            'div[class="ui_column is-9"]>span[class="ratingDate"]'
                        )
                        .text.replace("Reviewed ", "")
                        .strip()
                    )
                except Exception as e:
                    # print(e)
                    reviewed_at = "N/A"

                # Store Data as Dictonary
                yield {
                    "id_": id_,
                    "author": author,
                    "profile_picture": profile_picture,
                    "content_title": content_title,
                    "content": content,
                    "rating": rating,
                    "reviewed_at": reviewed_at,
                }
            next_page = response.css("a.next::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)


# run using next line

# scrapy crawl tripadvisor  -o reviews.json -t json
