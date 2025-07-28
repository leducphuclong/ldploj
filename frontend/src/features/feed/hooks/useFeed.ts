import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getPosts, createPost } from '../../../api/feedApi';
import { type PostCreate } from '../../../types';

export const useGetPosts = () => {
  return useQuery({
    queryKey: ['posts'], 
    queryFn: getPosts,    
  });
};

export const useCreatePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newPost: PostCreate) => createPost(newPost),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
};