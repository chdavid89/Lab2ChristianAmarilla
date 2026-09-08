"""Pruebas de reglas, seguridad y adaptador HTTP del historial."""

import hashlib
import hmac
import json
from datetime import UTC, date, datetime, timedelta

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.repositories.historial_repo import TransactionRecord
from app.routers.historial import list_transactions
from app.schemas.historial import HistorialQueryParams
from app.security import _b64encode, _jwt_secret, current_merchant
from app.services.historial_service import HistorialError, HistorialService


def _credentials(claims: dict[str, object]) -> HTTPAuthorizationCredentials:
    header = _b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64encode(json.dumps(claims).encode())
    signed = f"{header}.{payload}".encode()
    signature = _b64encode(hmac.new(_jwt_secret, signed, hashlib.sha256).digest())
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=f"{header}.{payload}.{signature}")


def test_current_merchant_accepts_valid_non_expired_token() -> None:
    credentials = _credentials({"sub": "MCHT-00001", "exp": datetime.now(UTC).timestamp() + 60})

    assert current_merchant(credentials) == "MCHT-00001"


@pytest.mark.parametrize(
    "credentials",
    [
        None,
        _credentials({"sub": "MCHT-00001", "exp": 0}),
        HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid.token.value"),
        _credentials({"sub": ""}),
    ],
)
def test_current_merchant_rejects_invalid_tokens(
    credentials: HTTPAuthorizationCredentials | None,
) -> None:
    with pytest.raises(HTTPException) as error:
        current_merchant(credentials)

    assert error.value.status_code == 401


def test_service_filters_serializes_pan_and_paginates() -> None:
    service = HistorialService()
    query = HistorialQueryParams(estado="approved", page_size=1)

    result = service.listar("MCHT-00001", query)

    transaction = result["data"][0]
    assert isinstance(transaction, dict)
    assert transaction["pan_last4"] == "4242"
    assert "pan" not in transaction
    assert result["pagination"]["total_estimated"] == 1


def test_service_supports_next_and_previous_cursors() -> None:
    service = HistorialService()
    first_page = service.listar("MCHT-00001", HistorialQueryParams(page_size=1))
    next_cursor = first_page["pagination"]["next_cursor"]
    assert isinstance(next_cursor, str)

    second_page = service.listar(
        "MCHT-00001", HistorialQueryParams(page_size=1, cursor=next_cursor)
    )
    prev_cursor = second_page["pagination"]["prev_cursor"]
    assert isinstance(prev_cursor, str)
    assert second_page["data"][0]["id"] != first_page["data"][0]["id"]

    previous_page = service.listar(
        "MCHT-00001", HistorialQueryParams(page_size=1, cursor=prev_cursor)
    )
    assert previous_page["data"][0]["id"] == first_page["data"][0]["id"]


def test_service_rejects_old_date_and_invalid_cursor() -> None:
    service = HistorialService()
    old_date = date.today() - timedelta(days=91)

    with pytest.raises(HistorialError, match="90"):
        service.listar("MCHT-00001", HistorialQueryParams.model_construct(desde=old_date))
    with pytest.raises(HistorialError, match="Cursor"):
        service.listar("MCHT-00001", HistorialQueryParams(cursor="not-a-cursor"))


def test_historial_query_rejects_invalid_dates() -> None:
    with pytest.raises(ValueError, match="inválido"):
        HistorialQueryParams(desde=date.today(), hasta=date.today() - timedelta(days=1))
    with pytest.raises(ValueError, match="futuras"):
        HistorialQueryParams(desde=date.today() + timedelta(days=1))


def test_router_translates_validation_and_business_errors() -> None:
    service = HistorialService()

    with pytest.raises(HTTPException) as page_size_error:
        list_transactions("MCHT-00001", service, page_size=201)
    assert page_size_error.value.detail == "page_size máximo permitido: 200"

    with pytest.raises(HTTPException) as old_range_error:
        list_transactions("MCHT-00001", service, desde=date.today() - timedelta(days=91))
    assert old_range_error.value.status_code == 400


def test_service_handles_empty_merchant() -> None:
    service = HistorialService()

    assert service.list_transactions("MCHT-unknown", HistorialQueryParams())["data"] == []


def test_cursor_encoder_rejects_naive_datetime() -> None:
    record = TransactionRecord(
        id="txn-test",
        merchant_id="MCHT-test",
        amount_cents=100,
        currency="USD",
        created_at=datetime.now(),
        pan="4111111111111111",
        status="approved",
    )
    cursor = HistorialService._encode_cursor(record, "next")

    with pytest.raises(HistorialError, match="Cursor"):
        HistorialService._decode_cursor(cursor)
