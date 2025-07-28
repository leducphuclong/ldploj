// frontend/src/api/feedApi.ts
import axios from 'axios';
import {type  Post,type  PostCreate } from '../types';

// The base URL is proxied by Vite, so we only need the path
const API_URL = '/api/v1/feed/';

export const getPosts = async (): Promise<Post[]> => {
  const response = await axios.get<Post[]>(API_URL);
  return response.data;
};

export const createPost = async (newPost: PostCreate): Promise<Post> => {
  const response = await axios.post<Post>(API_URL, newPost);
  return response.data;
};