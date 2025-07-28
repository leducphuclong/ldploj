export interface Post {
  id: number;
  title: string;
  content: string;
}

export type PostCreate = Omit<Post, 'id'>;