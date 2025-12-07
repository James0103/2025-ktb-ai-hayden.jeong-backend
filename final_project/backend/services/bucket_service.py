import os, boto3
from fastapi import UploadFile, HTTPException
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

class S3Service:
  def __init__(self):
    self.s3_client = boto3.client(
      's3',
      endpoint_url=os.getenv('BUCKET_ENDPOINT'),  # Railway S3 엔드포인트
      aws_access_key_id=os.getenv('BUCKET_ACCESS_KEY_ID'),
      aws_secret_access_key=os.getenv('BUCKET_SECRET_ACCESS_KEY'),
      region_name='auto'
    )
    self.bucket_name = os.getenv('BUCKET_NAME')

  @staticmethod
  async def upload_profile_photo(file: UploadFile) -> str:
    s3 = S3Service()

    # 1️⃣ 파일 읽기
    file_content = await file.read()

    # 2️⃣ 고유한 파일명 생성 (중복 방지)
    file_extension = file.filename.split('.')[-1]
    file_key = f"profiles/{uuid.uuid4()}_{datetime.now().timestamp()}.{file_extension}"

    # 3️⃣ S3에 Public 권한으로 업로드
    try:
      s3.s3_client.put_object(
        Bucket=s3.bucket_name,
        Key=file_key,
        Body=file_content,
        ContentType=file.content_type,
        ACL='public-read'  # ✅ Public 읽기 권한 추가
      )
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"S3 업로드 실패: {str(e)}")

    # 4️⃣ Presigned URL 생성 (최대 90일)
    # Railway Storage의 Presigned URL은 최대 90일(7776000초) 지원
    try:
      presigned_url = s3.s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': s3.bucket_name, 'Key': file_key},
        ExpiresIn=7776000  # 90일 (초 단위)
      )
      return presigned_url
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Presigned URL 생성 실패: {str(e)}")

  @staticmethod
  async def delete_profile_photo(profile_photo_url: str) -> bool:
    if not profile_photo_url:
      return False

    s3 = S3Service()

    try:
      if profile_photo_url.startswith('http'):
        # URL에서 경로 부분만 추출
        file_key = profile_photo_url.split(s3.bucket_name + '/')[-1].split('?')[0]
      else:
        file_key = profile_photo_url

      # S3에서 파일 삭제
      s3.s3_client.delete_object(
        Bucket=s3.bucket_name,
        Key=file_key
      )
      return True
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"S3 삭제 실패: {str(e)}")
