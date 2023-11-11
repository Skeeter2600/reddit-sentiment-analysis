import type { Topic } from './topic.model'

export interface User {
  email: String
  topics: Topic[]
}
