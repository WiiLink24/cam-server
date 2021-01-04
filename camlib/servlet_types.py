# TODO: Run black
class WPOperationServlet:
    def __init__(
        self,
        status,
        error_items,
        item_codes,
        item_price_codes,
        item_name,
        item_comment_1,
        item_comment_2,
        size,
        image_count,
        page_count,
        price,
        price_unit,
        delivery,
    ):
        self.status = status
        self.error_items = error_items
        self.item_codes = item_codes
        self.item_price_codes = item_price_codes
        self.item_name = item_name
        self.item_comment_1 = item_comment_1
        self.item_comment_2 = item_comment_2
        self.size = size
        self.image_count = image_count
        self.page_count = page_count
        self.price = price
        self.image_count_disp = image_count
        self.page_count_disp = page_count
        self.price_unit = price_unit
        self.delivery = delivery

    def tostring(self):
        # THIS IS BAD CODE
        out = """
statusCode={status}
latestClientVersion=0x02
        """
        for i in range(len(self.erroritems)):
            out = out.join(
                "\nerrorItems_{i}={item}".format(i=i, item=self.erroritems[i])
            )
        for i in range(len(self.itemcodes)):
            out = out.join("\nitemCode_{i}={item}".format(i=i, item=self.itemcodes[i]))
        # etc,. etc,. etc,.
        # Will do the rest later
