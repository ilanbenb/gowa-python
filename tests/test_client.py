from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
from pytest_httpx import HTTPXMock

from gowa_sdk import (
    ApiResponse,
    ChatMessagesParams,
    GoWaClient,
    SendChatPresenceRequest,
    SendImageRequest,
    SendMessageRequest,
    SendPresenceRequest,
)


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[GoWaClient, None]:
    sdk_client = GoWaClient(base_url="http://test-api")
    yield sdk_client
    await sdk_client.close()


@pytest.mark.asyncio
async def test_login(client: GoWaClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="http://test-api/app/login",
        json={
            "code": "200",
            "message": "Success",
            "results": {"qr_link": "test_qr", "qr_duration": 60},
        },
    )
    response = await client.login()
    assert isinstance(response, ApiResponse)
    assert response.code == "200"
    assert response.results is not None
    assert response.results.qr_link == "test_qr"


@pytest.mark.asyncio
async def test_send_message(client: GoWaClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="http://test-api/send/message",
        method="POST",
        json={
            "code": "200",
            "message": "Success",
            "results": {"message_id": "msg_123", "status": "SENT"},
        },
    )
    request = SendMessageRequest(phone="1234567890@s.whatsapp.net", message="Hello")
    response = await client.send_message(request)
    assert isinstance(response, ApiResponse)
    assert response.code == "200"
    assert response.results is not None
    assert response.results.message_id == "msg_123"


@pytest.mark.asyncio
async def test_send_presence_serializes_type_field(
    client: GoWaClient, httpx_mock: HTTPXMock
) -> None:
    captured: dict[str, object] = {}

    def callback(request: httpx.Request) -> httpx.Response:
        captured["json"] = json.loads(request.content.decode())
        return httpx.Response(
            200,
            json={
                "code": "200",
                "message": "Success",
                "results": {"message_id": "msg_presence", "status": "SENT"},
            },
        )

    httpx_mock.add_callback(callback, method="POST", url="http://test-api/send/presence")
    response = await client.send_presence(SendPresenceRequest(type="available"))
    assert response.code == "200"
    assert captured["json"] == {"type": "available"}


@pytest.mark.asyncio
async def test_send_chat_presence_payload(
    client: GoWaClient, httpx_mock: HTTPXMock
) -> None:
    captured: dict[str, object] = {}

    def callback(request: httpx.Request) -> httpx.Response:
        captured["json"] = json.loads(request.content.decode())
        return httpx.Response(
            200,
            json={
                "code": "200",
                "message": "Success",
                "results": {"message_id": "msg_chat_presence", "status": "SENT"},
            },
        )

    httpx_mock.add_callback(
        callback, method="POST", url="http://test-api/send/chat-presence"
    )
    response = await client.send_chat_presence(
        SendChatPresenceRequest(phone="1234567890@s.whatsapp.net", action="start")
    )
    assert response.code == "200"
    assert captured["json"] == {
        "phone": "1234567890@s.whatsapp.net",
        "action": "start",
    }


@pytest.mark.asyncio
async def test_download_message_media_includes_phone_query(
    client: GoWaClient, httpx_mock: HTTPXMock
) -> None:
    httpx_mock.add_response(
        url="http://test-api/message/msg_1/download?phone=1234567890@s.whatsapp.net",
        method="GET",
        content=b"media-bytes",
    )
    media = await client.download_message_media(
        "msg_1", phone="1234567890@s.whatsapp.net"
    )
    assert media == b"media-bytes"


@pytest.mark.asyncio
async def test_send_image_rejects_both_binary_and_url(client: GoWaClient) -> None:
    request = SendImageRequest(
        phone="1234567890@s.whatsapp.net",
        image_url="https://example.com/image.jpg",
    )
    with pytest.raises(ValueError, match="exactly one"):
        await client.send_image(request, image=b"image-bytes")


@pytest.mark.asyncio
async def test_send_image_rejects_missing_binary_and_url(client: GoWaClient) -> None:
    request = SendImageRequest(phone="1234567890@s.whatsapp.net")
    with pytest.raises(ValueError, match="exactly one"):
        await client.send_image(request)


@pytest.mark.asyncio
async def test_send_image_with_url_only(client: GoWaClient, httpx_mock: HTTPXMock) -> None:
    captured: dict[str, object] = {}

    def callback(request: httpx.Request) -> httpx.Response:
        captured["body"] = request.content
        return httpx.Response(
            200,
            json={
                "code": "200",
                "message": "Success",
                "results": {"message_id": "msg_image_url", "status": "SENT"},
            },
        )

    httpx_mock.add_callback(callback, method="POST", url="http://test-api/send/image")
    response = await client.send_image(
        SendImageRequest(
            phone="1234567890@s.whatsapp.net",
            image_url="https://example.com/image.jpg",
        )
    )
    assert response.code == "200"
    assert isinstance(captured["body"], (bytes, bytearray))
    assert b"image_url" in captured["body"]
    assert b"https%3A%2F%2Fexample.com%2Fimage.jpg" in captured["body"]


@pytest.mark.asyncio
async def test_get_chat_messages_uses_typed_query_params(
    client: GoWaClient, httpx_mock: HTTPXMock
) -> None:
    captured: dict[str, object] = {}

    def callback(request: httpx.Request) -> httpx.Response:
        captured["params"] = dict(request.url.params)
        return httpx.Response(
            200,
            json={"code": "200", "message": "Success", "results": {"data": []}},
        )

    httpx_mock.add_callback(callback, method="GET")
    await client.get_chat_messages(
        "1234567890@s.whatsapp.net",
        params=ChatMessagesParams(
            limit=10,
            search="hello",
            start_time=datetime(2026, 2, 6, 12, 0, 0, tzinfo=timezone.utc),
        ),
    )

    assert captured["params"] == {
        "limit": "10",
        "search": "hello",
        "start_time": "2026-02-06T12:00:00Z",
    }
