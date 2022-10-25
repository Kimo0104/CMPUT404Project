import axios from 'axios';
export const SERVER_URL = process.env.SERVER_URL || "http://localhost:8000"


export const getPost  = async (authorId, postId) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.get(`${path}`,{params: {authorId: authorId, postId: postId} });
    return response.data.result;
};

export const createPost = async (authorId, postId, data) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.put(`${path}`, null,  {params: data});
    return response.data.result;
}