import React, { useState } from 'react';
import { useCreatePost } from '../hooks/useFeed';

export const CreatePostForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  
  const createPostMutation = useCreatePost();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !content) return;

    createPostMutation.mutate(
      { title, content },
      {
        onSuccess: () => {
          setTitle('');
          setContent('');
        },
      }
    );
  };

  return (
    <form onSubmit={handleSubmit} className="post-form">
      <h2>Create a New Post</h2>
      <input
        type="text"
        placeholder="Post Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        disabled={createPostMutation.isPending}
      />
      <textarea
        placeholder="What's on your mind?"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        disabled={createPostMutation.isPending}
      />
      <button type="submit" disabled={createPostMutation.isPending}>
        {createPostMutation.isPending ? 'Submitting...' : 'Submit Post'}
      </button>
      {createPostMutation.isError && (
        <p className="error">Error: {createPostMutation.error.message}</p>
      )}
    </form>
  );
};