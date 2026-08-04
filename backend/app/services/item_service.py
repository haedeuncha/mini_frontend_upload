# item_service.py
from app.schemas.item_schema import ItemCreate, ItemPublic
from app.core.supabase_client import get_supabase
from zoneinfo import ZoneInfo
from datetime import datetime

# 1. 입력
def item_create(item: ItemCreate) -> ItemPublic | None:
    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    result = (
        supabase.table("items")
         .insert(
            {
                "name": item.name,
                "price": item.price,
                "desc": item.desc,
                "image_url": item.image_url,
                "image_filename": item.image_filename,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }
        )
        .execute()
    )
    if not result.data:
        return None
    return ItemPublic.model_validate(result.data[0])
