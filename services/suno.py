from schemas import CustomModeGenerateParam
from utils import (
    generate_music,
    get_upload_audio_s3_link,
    upload_audio,
    upload_audio_to_clip,
)


class SunoService:

    async def generate_music(self, file, input_text: str, token: str) -> str:
        """
        음악 생성
        """
        clip_id = await self.upload_file(file, token)
        data = CustomModeGenerateParam(
            # prompt="", # 이게 뭘까
            tags=input_text,
            continue_clip_id=clip_id,
        )
        resp = await generate_music(data.dict(), token)
        return resp

    async def upload_file(self, file, token: str) -> str:
        # s3 링크 가져오기
        s3_link = await get_upload_audio_s3_link(token)
        # s3에 파일 업로드
        await upload_audio(token, file, s3_link["url"], s3_link["fields"])
        clip_info = await upload_audio_to_clip(token, s3_link["id"])
        return clip_info["clip_info"]


suno_service = SunoService()
