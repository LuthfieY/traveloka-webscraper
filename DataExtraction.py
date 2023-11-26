from datetime import datetime, timezone
from DatastoreUtils import to_date, currency_to_integer, put_entity, create_entity

def extract_hotel_data(url, page_content, client):
    hotel_data = create_entity(client, "Hotel")

    overview = page_content.find(
        "div", class_="css-1dbjc4n r-obd0qt r-18u37iz r-ml3lyg r-tskmnb"
    )
    name = overview.find(
        "h1",
        class_="css-4rbku5 css-901oao css-cens5h r-cwxd7f r-t1w4ow r-1ui5ee8 r-b88u0q r-nwxazl r-fdjqy7",
    )
    if name:
        hotel_data["name"] = name.text
    starting_price = overview.find(
        "div", class_="css-901oao r-t1w4ow r-1x35g6 r-b88u0q r-vrz42v r-fdjqy7"
    )
    if starting_price:
        hotel_data["starting_price"] = currency_to_integer(starting_price.text)
    address = overview.find(
        "div",
        class_="css-901oao css-cens5h r-cwxd7f r-13awgt0 r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
    )
    if address:
        hotel_data["address"] = address.text[:-10]
    overview = page_content.find("div", class_="css-1dbjc4n r-18u37iz r-f4gmv6")
    about = overview.find(
        "div",
        style="font-family:MuseoSans,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol;font-size:14px;line-height:20px;max-height:80px;overflow:hidden",
    )
    if not about:
        about = overview.find(
            "div",
            style="font-family:MuseoSans,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol;font-size:14px;line-height:20px;max-height:40px;overflow:hidden",
        )
    if about:
        hotel_data["about"] = about.text.replace("\n", "")
    facilities_parent = page_content.find(
        "div", class_="css-1dbjc4n r-18u37iz r-f4gmv6 r-1ly5jyq"
    )
    if not facilities_parent:
        facilities_parent = page_content.find(
            "div", class_="css-1dbjc4n r-18u37iz r-1w6e6rj r-1fdih9r r-5oul0u"
        )
    facilities = facilities_parent.find_all(
        "div",
        class_="css-901oao r-cwxd7f r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
    )
    if facilities:
        hotel_data["main_facilities"] = []
        for facility in facilities:
            hotel_data["main_facilities"].append(facility.text)
    rating = page_content.find(
        "div",
        class_="css-901oao r-jwli3a r-t1w4ow r-s67bdx r-b88u0q r-10cxs7j r-q4m81j",
    )
    if rating:
        hotel_data["rating"] = float(rating.text)
    image = page_content.find("div", class_="css-1dbjc4n r-18u37iz r-n9chd3").find(
        "img"
    )
    if image:
        hotel_data["image"] = image["src"]
    hotel_data["scraped_at"] = datetime.now(timezone.utc)
    hotel_data["url"] = url

    put_entity(client, hotel_data)
    return hotel_data


def extract_review_data(page_content, client, hotel_data):
    reviews = page_content.find_all(
        "div",
        class_="css-1dbjc4n r-14lw9ot r-h1746q r-kdyh1x r-d045u9 r-18u37iz r-1fdih9r r-1udh08x r-d23pfw",
    )
    for review in reviews:
        review_data = create_entity(client, "Review")
        left_bar = review.find("div", class_="css-1dbjc4n r-b83rso r-1ssbvtb")
        main_content = review.find(
            "div", class_="css-1dbjc4n r-1habvwh r-13awgt0 r-1ssbvtb"
        )
        review_data["hotel_id"] = hotel_data.key
        reply = main_content.find(
            "div",
            class_="css-1dbjc4n r-1habvwh r-1ihkh82 r-h1746q r-kdyh1x r-1phboty r-rs99b7 r-1ssbvtb r-1udh08x r-ymttw5 r-1f1sjgu",
        )
        username = left_bar.find(
            "div",
            class_="css-901oao r-cwxd7f r-t1w4ow r-ubezar r-b88u0q r-135wba7 r-fdjqy7",
        )
        if username:
            review_data["username"] = username.text
        review_content = main_content.find(
            "div",
            class_="css-901oao css-cens5h r-cwxd7f r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
        )
        if review_content:
            review_data["review_content"] = review_content.text
        rating = main_content.find(
            "div",
            class_="css-901oao r-1i6uqv8 r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
        )
        if rating:
            review_data["rating"] = float(rating.text)
        category = left_bar.find(
            "div",
            class_="css-901oao r-cwxd7f r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
        )
        if category:
            review_data["category"] = category.text
        review_date = main_content.find_all(
            "div",
            class_="css-901oao r-1ud240a r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
        )[1]
        if review_date:
            review_data["review_date"] = to_date(review_date.text)
        images = main_content.find_all("img", class_="r-kdyh1x")
        if images:
            review_data["images"] = []
            for image in images:
                review_data["images"].append(image["src"])
        if reply:
            reply_content = reply.find(
                "div",
                class_="css-901oao css-cens5h r-cwxd7f r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
            )
            if not reply_content:
                reply_content = reply.find(
                    "div",
                    class_="css-901oao r-cwxd7f r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7",
                )
            review_data["reply_content"] = reply_content.text
            reply_date = reply.find(
                "div",
                class_="css-901oao r-1ud240a r-t1w4ow r-1b43r93 r-b88u0q r-rjixqe r-fdjqy7",
            )
            review_data["reply_date"] = to_date(reply_date.text)
        review_data["scraped_at"] = datetime.now(timezone.utc)

        put_entity(client, review_data)

def get_total_page(page_content):
    page_nums = page_content.find_all(
        "div",
        class_="css-901oao css-bfa6kz r-1i6uqv8 r-t1w4ow r-cygvgh r-b88u0q r-1iukymi r-q4m81j",
    )
    if len(page_nums) == 0:
        return 1
    total_page = page_nums[-1]
    return int(total_page.text)