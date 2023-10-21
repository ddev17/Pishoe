from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions import utils
from rasa_sdk.events import SlotSet


class ActionRecommendSpecialShoes(Action):

    def name(self) -> Text:
        return "action_recommend_special_shoes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question = utils.no_accent_vietnamese((tracker.latest_message)['text'])
        brands = utils.parse_brand_from_question(question)
        cust_name = tracker.get_slot('cust_name')
        if cust_name == None:
            cust_name = ""
        if len(brands) == 0:
            dispatcher.utter_message(
                text=f"Dạ cửa hàng đang bán 3 nhãn hiệu thể thao là Adidas, Nike và Puma. Bạn {cust_name} muốn chọn giày nhãn hiệu nào ạ?")
            return []

        size = utils.parse_size_from_question(question)
        if size is not None:
            if int(size) < 36 or int(size) > 44:
                dispatcher.utter_message(
                    text=f"Dạ sản phẩm ở cửa hàng chỉ còn size từ 36 đến 44 ạ")
                return []

        price_range = utils.parse_price_from_question(question)
        # recommend_shoes_list = utils.get_recommend_product(1)
        recommend_shoes_list = utils.get_recommend_special_product(brands, price_range)
        if (len(recommend_shoes_list)):
            dispatcher.utter_message(
                text=f"Dạ shop gửi bạn {cust_name} tham khảo mẫu: \nNhãn hiệu: {recommend_shoes_list[0]['brand']}\nSản phẩm: {recommend_shoes_list[0]['name']}\nGiá ưu đãi: {recommend_shoes_list[0]['price']}\n\nMẫu này đang hot, anh chị có muốn đặt hàng không ạ?",
                image=recommend_shoes_list[0]['image_src'],
            )
        else:
            dispatcher.utter_message(
                text=f"Dạ hiện tại shop không có sản phẩm nào phù hợp với yêu cầu, bạn {cust_name} có thể tham khảo mẫu này đang hot bên shop ạ.")
            recommend_shoes_list = utils.get_recommend_product(1)
            dispatcher.utter_message(
                text=f"Nhãn hiệu: {recommend_shoes_list[0]['brand']}\nSản phẩm: {recommend_shoes_list[0]['name']}\nGiá ưu đãi: {recommend_shoes_list[0]['price']}\n\nMẫu này đang hot, anh chị có muốn đặt hàng không ạ?",
                image=recommend_shoes_list[0]['image_src'])
        return []


class ActionRecommendShoes(Action):

    def name(self) -> Text:
        return "action_recommend_shoes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        brands = ["adidas", "nike", "puma"]
        recommend_shoes_list = utils.get_recommend_product(1)
        # recommend_shoes_list = utils.get_recommend_product(1, brands, price_range, 1)
        if (len(recommend_shoes_list)):
            dispatcher.utter_message(
                text=f"Dạ shop gửi anh chị tham khảo mẫu: \nNhãn hiệu: {recommend_shoes_list[0]['brand']}\nSản phẩm: {recommend_shoes_list[0]['name']}\nGiá ưu đãi: {recommend_shoes_list[0]['price']}\n\nMẫu này đang hot, anh chị có muốn đặt hàng không ạ?",
                image=recommend_shoes_list[0]['image_src'])
        else:
            dispatcher.utter_message(
                text="Dạ hiện tại shop không có sản phẩm nào phù hợp với yêu cầu, anh chị có thể tham khảo mẫu này đang hot bên shop ạ.")
            recommend_shoes_list = utils.get_recommend_product(1)
            dispatcher.utter_message(
                text=f"Nhãn hiệu: {recommend_shoes_list[0]['brand']}\nSản phẩm: {recommend_shoes_list[0]['name']}\nGiá ưu đãi: {recommend_shoes_list[0]['price']}\n\nMẫu này đang hot, anh chị có muốn đặt hàng không ạ?",
                image=recommend_shoes_list[0]['image_src'])
        return []

class ActionSaveInfomationCustomer:

    def name(self) -> Text:
        return "action_save_info_customer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=f"Dạ shop cảm ơn quý khách đã quan tâm sản phẩm, nhân viên của shop sẽ sớm liên hệ, chúc bạn 1 ngày tốt lành")
        return []

class ActionValidInfoCustomer:

    def name(self) -> Text:
        return "action_valid_info_customer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        dispatcher.utter_message(
            text=f"Dạ shop cảm ơn quý khách đã quan tâm sản phẩm, nhân viên của shop sẽ sớm liên hệ, chúc bạn 1 ngày tốt lành")
        return []
    
class ActionSaveCustName(Action):
    def name(self) -> Text:
        return "action_save_cust_name"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cust_name = next(tracker.get_latest_entity_values("cust_name"), None)
        if cust_name == None:
            dispatcher.utter_message(text = f"Dạ vâng, tôi có thể giúp gì cho bạn.")
            return [SlotSet("cust_name", "anh/chị")]
        else:
            dispatcher.utter_message(text = f"Xin chào {cust_name}, tôi có thể giúp gì cho bạn.")
        return [SlotSet("cust_name", cust_name)]

class ValidateOrderInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_info_form"
    def validate_cust_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cust_name value."""
        if isinstance(slot_value, str):
            # validation succeeded, capitalize the value of the "location" slot
            return {"cust_name": slot_value}
        else:
            return {"cust_name": None}

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone_number value."""
        if len(slot_value) > 9 and len(slot_value) < 12:
            dispatcher.utter_message(
                text=f"Dạ cảm ơn quý khách, shop đã xác nhận đơn hàng với số điện thoại: {slot_value}")
            return {"phone_number": slot_value.capitalize()}
        else:
            dispatcher.utter_message(text = f"Dạ quý khách vui lòng nhập đúng số điện thoại để nhân viên shop xác nhận đơn hàng ạ")
            return {"phone_number": None}
