from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import utils
from typing import Any, Coroutine, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

class action_save_name(Action):
    def name(self) -> Text:
        return 'action_save_name'

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionRecommendShoes(Action):

    def name(self) -> Text:
        return "action_recommend_shoes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question = utils.no_accent_vietnamese((tracker.latest_message)['text'])
        brands = utils.parse_brand_from_question(question)
        if len(brands) == 0:
            dispatcher.utter_message(
                text=f"Dạ cửa hàng đang bán 3 nhãn hiệu thể thao là Adidas, Nike và Puma. Anh/ chị muốn chọn giày nhãn hiệu nào ạ?")
            return []

        size = utils.parse_size_from_question(question)
        if size is not None:
            if int(size) < 36 or int(size) > 44:
                dispatcher.utter_message(
                    text=f"Dạ sản phẩm ở cửa hàng chỉ còn size 36 - 44, anh chị có muốn đổi qua size khác không ạ?")
                return []

        price_range = utils.parse_price_from_question(question)
        recommend_shoes_list = utils.get_recommend_product(brands, price_range, 1)
        dispatcher.utter_message(text=f"Dạ shop gửi anh chị tham khảo mẫu: \nNhãn hiệu: {recommend_shoes_list[0]['brand']}\nSản phẩm: {recommend_shoes_list[0]['name']}\nGiá ưu đãi: {recommend_shoes_list[0]['price']}\nimg:{recommend_shoes_list[0]['image_src']}\n\nMẫu này đang hot, anh chị có muốn đặt hàng không ạ?")
        return []


class ActionHelloWorld(Action):
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cust_name = next(tracker.get_latest_entity_values("cust_name"), None)
        return [SlotSet('cust_name', cust_name)]