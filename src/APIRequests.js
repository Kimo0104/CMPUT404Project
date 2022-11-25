import axios from 'axios';
//import React from 'react';

export const SERVER_URL = process.env.REACT_APP_SERVER_URL || "http://localhost:8000"

if (localStorage.getItem("token")) {
    axios.defaults.headers.common = {'Authorization': `Bearer ${JSON.parse(localStorage.getItem("token")).jwt}`}
    console.log(localStorage.getItem("token"));
}

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

export const createCommentLike = async(likerId, commentId) => {
    const path = SERVER_URL + `/authors/1/posts/1/comments/${commentId}/likes/${likerId}`;
    const response = await axios.post(path);
    return response.data;
};

export const deletePostLike = async(likerId, postId) => {
    const path = SERVER_URL + `/authors/1/posts/${postId}/likes/${likerId}`;
    const response = await axios.delete(path);
    return response.data;
};

export const deleteCommentLike = async(likerId, commentId) => {
    const path = SERVER_URL + `/authors/1/posts/1/comments/${commentId}/likes/${likerId}`;
    const response = await axios.delete(path);
    return response.data;
};

export const getAuthorPostLiked = async(authorId, postId) => {
    const path = SERVER_URL + `/authors/1/posts/${postId}/liked/${authorId}`;
    const response = await axios.get(path);
    return response.data;
};

export const getAuthorCommentLiked = async(authorId, commentId) => {
    const path = SERVER_URL + `/authors/1/posts/1/comments/${commentId}/liked/${authorId}`;
    const response = await axios.get(path);
    return response.data;
};

export const getPostLikes = async(postId) => {
    const path = SERVER_URL + `/authors/1/posts/${postId}/likes`;
    const response = await axios.get(path);
    return response.data;
};

export const getCommentLikes = async(commentId) => {
    const path = SERVER_URL + `/authors/1/posts/1/comments/${commentId}/likes`;
    const response = await axios.get(path);
    return response.data;
};

export const getAuthor = async(authorId) => {
    const path = SERVER_URL + `/authors/${authorId}`;
    const response = await axios.get(path);
    return response.data;
};

export const createPost = async (authorId, data) => {
    const path = SERVER_URL + `/authors/${authorId}/posts`;
    const response = await axios.put(`${path}`,data);
    return response.data;
}

export const createComment = async (authorId, postId, data) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}/comments`;
    const response = await axios.post(`${path}`,data);
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
    //console.log(GetAuthDetails());
    axios.post(path, data);//, {auth: GetAuthDetails()});

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
    return response.data;
}

export const loginUser = async (data) => {
    const path = SERVER_URL + `/users`
    data.withCredentials = true;
    const response = await axios.put(`${path}`, data);
    return response.data;
}

export const authUser = async (data) => {
    const path = SERVER_URL + `/users/auth`
    const response = await axios.post(`${path}`, data);
    return response.data;
}

export const deletePost = async(authorId, postId) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.delete(path);
    return response.data;
};

export const modifyPost = async (authorId, postId, data) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    axios.post(path, data);
}

export const uploadImage = async (referenceId, imageFile) => {
    const path = SERVER_URL + `/images/${referenceId}`;

    const reader = new FileReader();
    reader.onload = async (e) => {
        // https://stackoverflow.com/a/52311051
        let imageContent = e.currentTarget.result.replace(/^data:(.*,)?/, '');
        if ((imageContent.length % 4) > 0) {
          imageContent += '='.repeat(4 - (imageContent.length % 4));
        }

        const data = {"imageContent": imageContent};

        axios.post(path, data);
    };

    // https://stackoverflow.com/questions/10982712/convert-binary-data-to-base64-with-javascript
    reader.readAsDataURL(imageFile);
}

export const getImage = async (imageUrl) => {
    let response = await axios.get(imageUrl);
    return response.data;
}

export const getGithubEvents = async (githubUsername) => {
    const path = `https://api.github.com/users/${githubUsername}/events`;
    let response = await axios.get(path);
    return response.data;
}