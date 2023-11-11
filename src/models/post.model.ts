export interface Post {
  postId: string
  subreddit: string
  topics: string[]
  title: string
  text: string
  sentiment?: string
}
