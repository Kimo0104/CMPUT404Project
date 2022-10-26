import axios from 'axios';
export const SERVER_URL = process.env.SERVER_URL || "http://localhost:8000"


export const getPost  = async (authorId, postId) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.get(`${path}`,{params: {authorId: authorId, postId: postId} });
    return response.data.result;
};

export const getInbox = async(authorId, page, size) => {
    const path = SERVER_URL + `/authors/${authorId}/inbox?page=${page}&size=${size}`;
    const response = await axios.get(path);
    return response.data;
};

export const createPostLike = async(likerId, postId) => {
    const path = SERVER_URL + `/authors/1/posts/${postId}/likes/${likerId}`;
    const response = await axios.post(path);
    return response.data;
};

export const deletePostLike = async(likerId, postId) => {
    const path = SERVER_URL + `/authors/1/posts/${postId}/likes/${likerId}`;
    const response = await axios.delete(path);
    return response.data;
};

export const getAuthorPostLike = async(authorId, postId) => {
    const path = SERVER_URL + `/authors/1/posts/${postId}/liked/${authorId}`;
    const response = await axios.get(path);
    return response.data;
};

export const getAuthor = async(authorId) => {
    const path = SERVER_URL + `/authors/${authorId}`;
    const response = await axios.get(path);
    return response.data;
};

export const createPost = async (authorId, postId, data) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.put(`${path}`, null,  {params: data});
    return response.data.result;
}
