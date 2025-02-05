from .exemption_response import get_exemption_information
from .fix_item_information import fix_item_information
from .fix_order_information import fix_order_information
from .get_image_id import get_image_id
from .get_item_information import get_item_information
from .get_order_id import get_order_id
from .get_service_information import get_service_information
from .order_finish import notice_order_finish
from .order_id_available import order_id_available
from .update_order_information import update_order_information
from .get_assets import get_assets

action_list = {
    "getItemInformation": get_item_information,
    "fixItemInformation": fix_item_information,
    "getExemptionInformation": get_exemption_information,
    "getOrderID": get_order_id,
    "noticeOrderFinish": notice_order_finish,
    "isAvailableOrderID": order_id_available,
    "updateOrderInformation": update_order_information,
    "fixOrderInformation": fix_order_information,
    "getAssets": get_assets,
}

file_action_list = {
    "getImageID": get_image_id,
    "getServiceInformation": get_service_information,
}
