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

export const checkFollowStatus = async (authorId, foreignAuthorId) => {
    // 0 -> Not following
    // 1 -> Requested to followed
    // 2 -> Following
    const followPath = SERVER_URL + `/authors/${foreignAuthorId}/followers/${authorId}`
    const followResponse = await axios.get(`${followPath}`);

    const followRequestPath = SERVER_URL + `/authors/${foreignAuthorId}/followRequest/${authorId}`
    const followRequestResponse = await axios.get(`${followRequestPath}`);

    let followStatus = -1
    if (followResponse.data.id !== "") {
        followStatus = 2
    }
    else {
        if (followRequestResponse.data.id !== "") {
            followStatus = 1
        }
        else {
            followStatus = 0
        }
    }
    return followStatus
}

export const requestToFollow = async (authorId, foreignAuthorId) => {
    const path = SERVER_URL + `/authors/${authorId}/followers/${foreignAuthorId}`
    const response = await axios.post(`${path}`);

    console.log(response)
    return response.status
}

export const removeFollower = async (authorId, foreignAuthorId) => {
    const path = SERVER_URL + `/authors/${foreignAuthorId}/followers/${authorId}`
    const response = await axios.delete(`${path}`);

    console.log(response)
    return response.status
}