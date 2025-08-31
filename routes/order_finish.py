from camlib import response
from camlib.shutterfly import ShutterflyClient
from camlib.photobox import PhotoboxClient
import config
import logging

@response()
def notice_order_finish(request):
    error_items = []
    messages = []
    
    try:
        if config.use_shutterfly:
            shutterfly = ShutterflyClient(config.shutterfly_api_key, config.shutterfly_api_secret)
            shutterfly.create_order(request.json["items"])
            messages.append("Order sent to Shutterfly")
    except Exception as e:
        logging.error(f"Shutterfly error: {str(e)}")
        error_items.append(1)
        messages.append("Shutterfly order failed")
    
    try:
        if config.use_photobox:
            photobox = PhotoboxClient(config.photobox_client_id, config.photobox_client_secret)
            photobox.create_order(
                product_id=request.json["product_id"],
                image_id=request.json["image_id"]
            )
            messages.append("Order sent to Photobox")
    except Exception as e:
        logging.error(f"Photobox error: {str(e)}")
        error_items.append(2)
        messages.append("Photobox order failed")
    
    return {
        "errorItems": error_items if error_items else [0],
        "available": 0,
        "fixOrderText": "Order processing completed",
        "messageBoardText": ". ".join(messages) if messages else "Order processed successfully"
    }
