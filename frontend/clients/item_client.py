from typing import Any

from core.api_client import request

def create_item(name:str, price:int, desc:str, image: Any = None):
    """  로그인 진행 ID와 PWD 입력 하면 사용자 정보 리턴"""

    return request(
                    "POST", 
                    f"/item/create", 
                    json={"name":name, "price":price, "desc":desc},
                    files={"image": image} if image else None
                   )
