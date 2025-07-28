import { useGetPosts } from '../hooks/useFeed';
import {type Post } from '../../../types';

const PostCard = ({ post }: { post: Post }) => (
  <div className="post-card">
    <h3>{post.title}</h3>
    <p>{post.content}</p>
  </div>
);

export const PostList = () => {
  const { data: posts, isLoading, isError, error } = useGetPosts();

  if (isLoading) {
    return <div>Loading posts...</div>;
  }

  if (isError) {
    return <div className="error">Error fetching posts: {error.message}</div>;
  }

  return (
    <div className="post-list">
      <h2>Feed</h2>
      {posts && posts.length > 0 ? (
        posts.map((post) => <PostCard key={post.id} post={post} />).reverse() // Show newest first
      ) : (
        <p>No posts yet. Be the first to create one!</p>
      )}
    </div>
  );    
};