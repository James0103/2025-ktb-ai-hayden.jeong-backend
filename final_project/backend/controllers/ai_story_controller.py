import os
from typing import List
from models import PostCreate, PostUpdate, PostResponse, MainStoryGenerate, RelayStoryGenerate
from sqlalchemy.orm import Session
from db.models import PostDB
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

class AIController:
  """
  게시물(릴레이 스토리) 관리 관련 비즈니스 로직을 담당합니다.
  """

  @staticmethod
  async def generate_main_story(story_info: MainStoryGenerate) -> str:
    title = story_info.title
    if story_info.content is not None:
      content = story_info.content
    genre = story_info.genre
    next_story_count = story_info.next_story_count

    response = client.models.generate_content(
      model="gemini-2.5-flash", 
      contents=f"{title}와 {content}를 주제로 한 30자 내외의 {genre} 이야기를 작성해줘. 전체 이야기의 흐름은 앞으로 {next_story_count} 만큼의 글로 작성될거고 이 글은 전체 내용의 앞 부분이에요",
      config=genai.types.GenerateContentConfig(
        system_instruction="당신은 유능한 작가입니다. 특히 잘쓰는 부분은 글의 시작 부분입니다."
      )
    )
    
    return response.text

  @staticmethod
  async def generate_relay_story(story_info: RelayStoryGenerate) -> str:
    title = story_info.title
    content_story = story_info.content_story
    genre = story_info.genre
    next_story_count = story_info.next_story_count
    prev_story_count = story_info.prev_story_count

    response = client.models.generate_content(
      model="gemini-2.5-flash", 
      contents=f"f{title} {content_story}에 이어서 30자 내외의 글을 작성해줘.{genre}를 기반으로 하고, 전체 스토리 흐름의 {prev_story_count/next_story_count}% 정도 진행된 글이에요.",
      config=genai.types.GenerateContentConfig(
        system_instruction="당신은 유능한 작가입니다. 특히 잘쓰는 부분은 글의 시작 부분입니다."
      )
    )
    
    return response.text