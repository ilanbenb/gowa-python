from __future__ import annotations

from typing import Optional

from ..models import (
    MessageSendResponse,
    SendAudioRequest,
    SendChatPresenceRequest,
    SendContactRequest,
    SendFileRequest,
    SendImageRequest,
    SendLinkRequest,
    SendLocationRequest,
    SendMessageRequest,
    SendPollRequest,
    SendPresenceRequest,
    SendStickerRequest,
    SendVideoRequest,
)
from ..protocols import GoWaClientProtocol


class SendMixin(GoWaClientProtocol):
    @staticmethod
    def _validate_binary_or_url(
        binary_content: bytes | None,
        media_url: str | None,
        *,
        binary_name: str,
        url_name: str,
    ) -> None:
        has_binary = binary_content is not None
        has_url = bool(media_url)
        if has_binary == has_url:
            raise ValueError(f"Provide exactly one of `{binary_name}` or `{url_name}`.")

    async def send_message(
        self, request: SendMessageRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post("/send/message", json=request, device_id=device_id)
        return MessageSendResponse.model_validate_json(response.content)

    async def send_image(
        self,
        request: SendImageRequest,
        image: bytes | None = None,
        *,
        filename: str = "image.jpg",
        device_id: Optional[str] = None,
    ) -> MessageSendResponse:
        self._validate_binary_or_url(
            image,
            request.image_url,
            binary_name="image",
            url_name="request.image_url",
        )
        response = await self._post(
            "/send/image",
            data=request,
            files={"image": (filename, image)} if image is not None else None,
            device_id=device_id,
        )
        return MessageSendResponse.model_validate_json(response.content)

    async def send_audio(
        self,
        request: SendAudioRequest,
        audio: bytes | None = None,
        *,
        filename: str = "audio.ogg",
        device_id: Optional[str] = None,
    ) -> MessageSendResponse:
        self._validate_binary_or_url(
            audio,
            request.audio_url,
            binary_name="audio",
            url_name="request.audio_url",
        )
        response = await self._post(
            "/send/audio",
            data=request,
            files={"audio": (filename, audio)} if audio is not None else None,
            device_id=device_id,
        )
        return MessageSendResponse.model_validate_json(response.content)

    async def send_file(
        self,
        request: SendFileRequest,
        file: bytes,
        *,
        filename: str = "file",
        device_id: Optional[str] = None,
    ) -> MessageSendResponse:
        response = await self._post(
            "/send/file",
            data=request,
            files={"file": (filename, file)},
            device_id=device_id,
        )
        return MessageSendResponse.model_validate_json(response.content)

    async def send_sticker(
        self,
        request: SendStickerRequest,
        sticker: bytes | None = None,
        *,
        filename: str = "sticker.webp",
        device_id: Optional[str] = None,
    ) -> MessageSendResponse:
        self._validate_binary_or_url(
            sticker,
            request.sticker_url,
            binary_name="sticker",
            url_name="request.sticker_url",
        )
        response = await self._post(
            "/send/sticker",
            data=request,
            files={"sticker": (filename, sticker)} if sticker is not None else None,
            device_id=device_id,
        )
        return MessageSendResponse.model_validate_json(response.content)

    async def send_video(
        self,
        request: SendVideoRequest,
        video: bytes | None = None,
        *,
        filename: str = "video.mp4",
        device_id: Optional[str] = None,
    ) -> MessageSendResponse:
        self._validate_binary_or_url(
            video,
            request.video_url,
            binary_name="video",
            url_name="request.video_url",
        )
        response = await self._post(
            "/send/video",
            data=request,
            files={"video": (filename, video)} if video is not None else None,
            device_id=device_id,
        )
        return MessageSendResponse.model_validate_json(response.content)

    async def send_contact(
        self, request: SendContactRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post("/send/contact", json=request, device_id=device_id)
        return MessageSendResponse.model_validate_json(response.content)

    async def send_link(
        self, request: SendLinkRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post("/send/link", json=request, device_id=device_id)
        return MessageSendResponse.model_validate_json(response.content)

    async def send_location(
        self, request: SendLocationRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post("/send/location", json=request, device_id=device_id)
        return MessageSendResponse.model_validate_json(response.content)

    async def send_poll(
        self, request: SendPollRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post("/send/poll", json=request, device_id=device_id)
        return MessageSendResponse.model_validate_json(response.content)

    async def send_presence(
        self, request: SendPresenceRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post("/send/presence", json=request, device_id=device_id)
        return MessageSendResponse.model_validate_json(response.content)

    async def send_chat_presence(
        self, request: SendChatPresenceRequest, *, device_id: Optional[str] = None
    ) -> MessageSendResponse:
        response = await self._post(
            "/send/chat-presence", json=request, device_id=device_id
        )
        return MessageSendResponse.model_validate_json(response.content)
