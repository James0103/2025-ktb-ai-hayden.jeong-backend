/**
 * User 모델 클래스
 * 사용자 정보를 관리하는 클래스
 */
export class User {
  constructor({
    id = null,
    nickname = '',
    email = '',
    profile_photo = null,
    created_at = null,
    updated_at = null
  } = {}) {
    this.id = id
    this.nickname = nickname
    this.email = email
    this.profilePhoto = profile_photo
    this.createdAt = created_at
    this.updatedAt = updated_at
  }

  /**
   * 서버 응답을 User 객체로 변환
   */
  static fromJSON(data) {
    return new User({
      id: data.id,
      nickname: data.nickname,
      email: data.email,
      profile_photo: data.profile_photo || null,
      created_at: data.created_at ? new Date(data.created_at) : null,
      updated_at: data.updated_at ? new Date(data.updated_at) : null
    })
  }

  /**
   * User 객체를 JSON으로 변환 (API 전송용)
   */
  toJSON() {
    return {
      id: this.id,
      nickname: this.nickname,
      email: this.email,
      profilePhoto: this.profilePhoto,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    }
  }

  /**
   * 사용자명의 첫 글자 반환 (프로필 아바타용)
   */
  getInitial() {
    return this.email?.charAt(0).toUpperCase() || '?'
  }

  /**
   * 사용자 프로필이 완성되었는지 확인
   */
  isComplete() {
    return !!(this.id && this.nickname && this.email)
  }
}
