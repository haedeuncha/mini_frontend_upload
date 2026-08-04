from typing import Any

from core.api_client import request

def client_item(name:str, price:int, desc:str, image :Any = None):
    """  상품 등록 """
    return request("POST", f"/items", json={"name":name, "price":price, "description":desc, "image":image})



