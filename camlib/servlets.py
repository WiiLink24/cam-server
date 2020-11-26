# TODO: Run black
class WPOperationServlet:
    def __init__(
        self,
        status,
        erroritems,
        itemcodes,
        itemnames,
        sizes,
        imagecounts,
        prices,
        imagecountdisps,
        priceunits,
        deliveries,
    ):
        self.status = status
        self.erroritems = erroritems
        self.itemcodes = itemcodes
        self.itemnames = itemnames
        self.sizes = sizes
        self.imagecounts = imagecounts
        self.prices = prices
        self.imagecountdisps = imagecountdisps
        self.priceunits = priceunits
        self.deliveries = deliveries

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
