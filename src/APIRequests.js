import axios from 'axios';
export const SERVER_URL = process.env.SERVER_URL || "http://localhost:8000"


export const getPost  = async (authorId, postId) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.get(`${path}`);
    return response.data;
};

export const getPublicPosts = async (authorId, page, size) => {
    const path = SERVER_URL + `/authors/${authorId}/posts`;
    const response = await axios.get(path, {params: {page: page, size: size}});
    return response.data;
}

export const getInbox = async(authorId, page, size) => {
    const path = SERVER_URL + `/authors/${authorId}/inbox`;
    const response = await axios.get(path, {params: {page: page, size: size}});
    return response.data;
};

export const sendPublicInbox = async(authorId, postId) => {
    const path = SERVER_URL + `/inbox/public/${authorId}/${postId}`;
    const response = await axios.post(path);
    return response.data;
};

export const sendFriendInbox = async(authorId, postId) => {
    const path = SERVER_URL + `/inbox/friend/${authorId}/${postId}`;
    const response = await axios.post(path);
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

export const createPost = async (authorId, data) => {
    const path = SERVER_URL + `/authors/${authorId}/posts`
    const response = await axios.put(`${path}`,data);
    return response.data;
}

export const searchForAuthors = async (query, page, size) => {
    let path = SERVER_URL + `/find?query=${query}`
    if (page !== null) {
        path += `&page=${page}`;
    }
    if (size !== null) {
        path += `&size=${size}`;
    }

    const response = await axios.get(path);
    return response.data;
}

export const modifyAuthor = async (authorId, newGithub, newProfileImage) => {
    const path = SERVER_URL + `/authors/${authorId}`;

    const data = {
        "github": newGithub,
        "profileImage": newProfileImage
    }

    axios.post(path, data);

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
    return response.status
}

export const removeFollower = async (authorId, foreignAuthorId) => {
    const path = SERVER_URL + `/authors/${foreignAuthorId}/followers/${authorId}`
    const response = await axios.delete(`${path}`);
    return response.status
}

export const getFollowRequests = async (authorId) => {
    const path = SERVER_URL + `/authors/${authorId}/followRequest`
    const response = await axios.get(`${path}`);
    return response.data
}

export const addFollower = async (authorId, foreignAuthorId) => {
    const path = SERVER_URL + `/authors/${authorId}/followers/${foreignAuthorId}`
    const response = await axios.put(`${path}`);
    return response.status
}

export const removeFollowRequest = async (authorId, foreignAuthorId) => {
    const path = SERVER_URL + `/authors/${authorId}/followRequest/${foreignAuthorId}`
    const response = await axios.delete(`${path}`);
    return response.status
}

export const createUser = async (data) => {
    const path = SERVER_URL + `/users`
    const response = await axios.post(`${path}`, data);
    return response.data.result;
}

export const loginUser = async (data) => {
    const path = SERVER_URL + `/users`
    const response = await axios.put(`${path}`, data);
    return response.data;
}


