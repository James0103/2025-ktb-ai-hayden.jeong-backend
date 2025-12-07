/**
 * Post 모델 클래스
 * 게시물 정보를 관리하는 클래스
 */
export class Post {
  constructor({
    id = null,
    title = '',
    content = '',
    nickname = '',
    genre = '',
    user_id = null,
    next_story_count = 0,
    created_at = null,
    updated_at = null,
    comments = []
  } = {}) {
    this.id = id
    this.title = title
    this.content = content
    this.nickname = nickname
    this.genre = genre
    this.user_id = user_id
    this.next_story_count = next_story_count
    this.created_at = created_at
    this.updated_at = updated_at
    this.comments = comments
  }

  /**
   * 서버 응답을 Post 객체로 변환
   */
  static fromJSON(data) {
    return new Post({
      id: data.id,
      title: data.title,
      content: data.content,
      nickname: data.nickname,
      genre: data.genre,
      user_id: data.user_id,
      next_story_count: data.next_story_count || 0,
      created_at: data.created_at,
      updated_at: data.updated_at,
      comments: (data.comments || []).map(comment => ({
        id: comment.id,
        content: comment.content,
        nickname: comment.nickname,
        user_id: comment.user_id,
        created_at: comment.created_at,
        updated_at: comment.updated_at
      }))
    })
  }

  /**
   * Post 객체를 JSON으로 변환 (API 전송용)
   */
  toJSON() {
    return {
      id: this.id,
      title: this.title,
      content: this.content,
      nickname: this.nickname,
      genre: this.genre,
      user_id: this.user_id,
      next_story_count: this.next_story_count,
      created_at: this.created_at,
      updated_at: this.updated_at,
      comments: this.comments
    }
  }

  /**
   * 게시물이 유효한지 확인
   */
  isValid() {
    return !!(this.title && this.content)
  }

  /**
   * 남은 이야기 갯수 반환
   */
  getRemainingStories() {
    return this.next_story_count > 0
      ? this.next_story_count - this.comments.length
      : this.comments.length
  }

  /**
   * 이야기가 완성되었는지 확인
   */
  isComplete() {
    return this.next_story_count > 0 && this.comments.length >= this.next_story_count
  }
}
