
import integ_auto as ia
import naver_shopping as ns
import os
import json


def main():

    filepath = os.path.join(os.path.expanduser(
        '~'), ".ns", "config.json")

    with open(filepath, 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    driver = ia.Automatic.create_edge_driver()
    auto = ia.Automatic(driver)

    # 0. go home
    ns.go_home(auto)

    # 1. login
    ns.login(auto, config['id'], config['pw'])

    # 2. Go to detail page.
    ps = ns.get_purchasable_products(auto, "포켓몬빵")
    if not ps:
        print("No products")
        return

    # Go to the detail page of first product.
    ps[0].click()

    # 3. Buy button
    ns.buy_item_in_detail_page(auto)

    # 5. naver pay
    ns.naver_payment(auto, config['pin'])


if __name__ == "__main__":
    main()
