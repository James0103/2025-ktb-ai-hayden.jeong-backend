/**
 * RelayStory 모델 클래스
 * 릴레이 스토리의 다음 이야기(댓글) 정보를 관리하는 클래스
 */
export class RelayStory {
  constructor({
    id = null,
    content = '',
    author = '',
    userId = null,
    postId = null,
    createdAt = null,
    updatedAt = null
  } = {}) {
    this.id = id
    this.content = content
    this.author = author
    this.userId = userId
    this.postId = postId
    this.createdAt = createdAt
    this.updatedAt = updatedAt
  }

  /**
   * 서버 응답을 RelayStory 객체로 변환
   */
  static fromJSON(data) {
    return new RelayStory({
      id: data.id,
      content: data.content,
      author: data.author,
      userId: data.userId,
      postId: data.postId,
      createdAt: data.createdAt,
      updatedAt: data.updatedAt
    })
  }

  /**
   * RelayStory 객체를 JSON으로 변환 (API 전송용)
   */
  toJSON() {
    return {
      id: this.id,
      content: this.content,
      author: this.author,
      userId: this.userId,
      postId: this.postId,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    }
  }

  /**
   * 다음 이야기가 유효한지 확인
   */
  isValid() {
    return !!(this.content && this.postId)
  }

  /**
   * 다음 이야기가 비어있는지 확인
   */
  isEmpty() {
    return !this.content || this.content.trim() === ''
  }

  /**
   * 내용 길이 반환
   */
  getContentLength() {
    return this.content.length
  }
}
