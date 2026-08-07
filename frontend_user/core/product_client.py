"""관리자 상품 조회용 FastAPI 클라이언트입니다."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BACKEND_URL = "http://127.0.0.1:8000"


class ProductAPIError(Exception):
    """상품 API 호출 중 발생한 오류입니다."""


def get_products() -> list[dict]:
    """등록된 전체 상품을 반환합니다."""
    request = Request(f"{BACKEND_URL}/product/getall", method="GET")

    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ProductAPIError(f"상품 조회 요청 실패: {error.code}") from error
    except URLError as error:
        raise ProductAPIError("백엔드 서버에 연결할 수 없습니다. FastAPI 실행 상태를 확인하세요.") from error
    except json.JSONDecodeError as error:
        raise ProductAPIError("백엔드가 상품 목록을 JSON 형식으로 반환하지 않았습니다.") from error

    if not payload.get("success"):
        raise ProductAPIError(payload.get("message", "상품 목록을 불러오지 못했습니다."))

    return payload.get("data", [])
