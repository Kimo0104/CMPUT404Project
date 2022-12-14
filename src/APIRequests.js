import axios from 'axios';
import {SERVER_URL,
    TEAM12_URL,
    TEAM12_CONFIG,
    TEAM19_URL,
    TEAM19_CONFIG,
    TEAM14_URL, 
    TEAM14_CONFIG, 
    Team14AuthorToLocalAuthor,
    Team14FollowRequestBody
} from './interactionUtils'


export const setAuthorizationHeader = async () => {
    if (localStorage.getItem("token")) {
        axios.defaults.headers.common = {'Authorization': `Bearer ${JSON.parse(localStorage.getItem("token")).jwt}`}
    }
}

if (localStorage.getItem("token")) {
    axios.defaults.headers.common = {'Authorization': `Bearer ${JSON.parse(localStorage.getItem("token")).jwt}`}
}

export const getPost  = async (authorId, postId) => {
    const path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.get(`${path}`);
    return response.data;
};

export const getPosts = async (authorId, page, size, visibility = "PUBLIC") => {
    const path = SERVER_URL + `/authors/${authorId}/posts`;
    const response = await axios.get(path, {params: {visibility: visibility, page: page, size: size}});
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

export const deleteInbox = async(authorId) => {
    const path = SERVER_URL + `/authors/${authorId}/inbox`;
    const response = await axios.delete(path);
    return response.data;
};

export const createPostLike = async(likerId, postId) => {
    let path = SERVER_URL + `/authors/1/posts/${postId}/likes/${likerId}`;
    const response = await axios.post(path);

    let liker = await getAuthor(likerId);
    if (liker === "Author does not exist") { return liker; }
    let post = (await axios.get(SERVER_URL + `/authors/1/posts/${postId}`)).data;

    // TEAM 12
    // ALWAYS send
    path = TEAM12_URL + `/authors/${likerId}/${liker.displayName}/posts/${postId}/likes/`;
    axios.post(path, {}, TEAM12_CONFIG);

    // TEAM 19
    // Only send if poster is from team 19
    if (post && post.author.host === TEAM19_URL) {
        let data19 = {};
        data19.context = SERVER_URL;
        data19.summary = `${liker.displayName} liked your post`;
        data19.author = liker;
        data19.author.github = undefined;
        data19.object = TEAM19_URL + `/authors/${post.author.id}/posts/${postId}`;
        path = TEAM19_URL + `/authors/${post.author.id}/inbox/likes`;
        axios.post(path, data19, TEAM19_CONFIG);
    }

    return response.data;
};

export const createCommentLike = async(likerId, commentId) => {
    let path = SERVER_URL + `/authors/1/posts/1/comments/${commentId}/likes/${likerId}`;
    const response = await axios.post(path);

    let liker = await getAuthor(likerId);
    if (liker === "Author does not exist") { return liker; }
    let comment = (await axios.get(SERVER_URL + `/authors/1/posts/1/comments/${commentId}`)).data;
    let post = (await axios.get(SERVER_URL + `/authors/1/posts/${comment.post.id}`)).data;

    // TEAM 12
    // only create if commenter is from team 12 or team 13
    if (comment && (comment.author.host === TEAM12_URL || comment.author.host === SERVER_URL)) {
        path = TEAM12_URL + `/authors/${likerId}/${liker.displayName}/comments/${commentId}/likes/`;
        axios.post(path, {}, TEAM12_CONFIG);
    }

    // TEAM 19
    // ONLY send if author of comment is from TEAM 19
    if (comment && comment.author.host == TEAM19_URL) {
        let data19 = {};
        data19.context = SERVER_URL;
        data19.summary = `${liker.displayName} liked your post`;
        data19.author = liker;
        data19.author.github = undefined;
        data19.object = TEAM19_URL + `/authors/${post.author.id}/posts/${post.id}/coments/${comment.id}`;
        path = TEAM19_URL + `/authors/${comment.author.id}/inbox/likes`;
        axios.post(path, data19, TEAM19_CONFIG);
        return response.data;
    }
};

export const deletePostLike = async(likerId, postId) => {
    let path = SERVER_URL + `/authors/1/posts/${postId}/likes/${likerId}`;
    const response = await axios.delete(path);

    let liker = await getAuthor(likerId);
    if (liker === "Author does not exist") { return liker; }
    // let post = (await axios.get(SERVER_URL + `/authors/1/posts/${postId}`)).data;

    // TEAM 12
    path = TEAM12_URL + `/authors/${likerId}/${liker.displayName}/posts/${postId}/likes/`;
    axios.post(path, {}, TEAM12_CONFIG);

    // TEAM 19 has no logic for this

    return response.data;
};

export const deleteCommentLike = async(likerId, commentId) => {
    let path = SERVER_URL + `/authors/1/posts/1/comments/${commentId}/likes/${likerId}`;
    const response = await axios.delete(path);

    let liker = await getAuthor(likerId);
    if (liker === "Author does not exist") { return liker; }
    let comment = (await axios.get(SERVER_URL + `/authors/1/posts/1/comments/${commentId}`)).data;

    // TEAM 12
    // only delete if commenter is from team 12 or team 13
    if (comment && (comment.author.host === TEAM12_URL || comment.author.host === SERVER_URL)) {
        path = TEAM12_URL + `/comments/${commentId}/likes/`;
        axios.post(path, {}, TEAM12_CONFIG);
    }

    // TEAM 19 not required

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
    let path = SERVER_URL + `/authors/${authorId}`;
    let response = await axios.get(path);
    if (response.data !== "") { return response.data; }

    var globalResponse = false;
    // TEAM 12
    path = TEAM12_URL + `/authors/${authorId}/`;
    await axios.get(path, TEAM12_CONFIG).then((response) => {
        if (!response.data.detail) { 
            response.data.displayName = response.data.username;
            response.data.type = "author";
            response.data.url = `${response.data.host}/authors/${authorId}/`;
            response.data.accepted = true;
            response.data.profileImage = response.data.profile_image;
            response.data.host = TEAM12_URL;
            globalResponse = response.data;
            return response.data 
        }
    }).catch((reason) => { console.clear(); });
    if (globalResponse) { return globalResponse; }

    // TEAM 19
    path = TEAM19_URL + `/authors/${authorId}`;
    await axios.get(path, TEAM19_CONFIG).then((response) => {
        if (response.data !== "Author matching query does not exist.") { 
            response.data.accepted = true;
            response.data.host = TEAM19_URL;
            response.data.id = response.data.id.split('/authors/')[1];
            globalResponse = response.data;
            return response.data; 
        }
    }).catch((reason) => { console.clear(); });

    // path = TEAM14_URL + `api/authors/${authorId}/   `
    // await axios.get(path, TEAM14_CONFIG).then((response) => {
    //     if (response.data !== "Author not found") { 
    //         globalResponse = Team14AuthorToLocalAuthor(response.data)
    //     }
    // }).catch((reason) => { console.clear(); });

    if (globalResponse) { return globalResponse; }

    return "Author not found";
};

export const createPost = async (authorId, data) => {
    let path = SERVER_URL + `/authors/${authorId}/posts`;
    const response = await axios.put(`${path}`,data);

    let author = await getAuthor(authorId);
    if (author === "Author does not exist") { return author; }
    let originalAuthor = author;
    if (data.originalAuthor !== authorId) {
        originalAuthor = await getAuthor(data.originalAuthor);
    }
    
    // TEAM 12
    path = TEAM12_URL + `/authors/${authorId}/${author.displayName}/posts/`;
    let data12 = {};
    data12.author = author.id;
    data12.original_author_id = originalAuthor.id;
    data12.original_author = originalAuthor.displayName;
    data12.original_author_host = originalAuthor.host;
    data12.title = data.title;
    if (!data12.title || data12.title === "") { data12.title = "image post"; }
    data12.id = response.data.id;
    data12.description = data.description;
    if (data.contentType === 'image') {
        data12.image_url = data.content;
    } else {
        data12.content = data.content;
    }
    if (data.visiblity == "UNLISTED") {
        data12.visibility = "PUBLIC";
        data12.unlisted = true;
    } else {
        data12.visibility = data.visibility;
        data12.unlisted = false;
    }
    axios.post(path, data12, TEAM12_CONFIG);

    // TEAM 19
    var inboxees = [];
    if (data.visibility === "PUBLIC") {
        inboxees = (await axios.get(SERVER_URL+`/authors/${authorId}/followers`)).data;
    } else if (data.visibility === "FRIENDS") {
        inboxees = (await axios.get(SERVER_URL+`/authors/${authorId}/friends`)).data;
    }
    if (inboxees.length > 0) {
        let data19 = {};
        data19.title = data.title;
        data19.id = response.data.id;
        data19.source = data.source;
        data19.origin = data.origin;
        data19.description = data.description;
        data19.contentType = data.contentType;
        data19.content = data.content;
        data19.author = {
            id: authorId,
            host: author.host,
            url: author.url,
            displayName: author.displayName,
            profileImage: author.profileImage
        };
        data19.categories = "[]";
        if (data.visiblity == "UNLISTED") {
            data19.visibility = "PUBLIC";
            data19.unlisted = true;
        } else {
            data19.visibility = data.visibility;
            data19.unlisted = false;
        }
        
        for (let inboxee of inboxees) {
            if (inboxee.followerObj.host === TEAM19_URL) {
                path = TEAM19_URL + `/authors/${inboxee.follower}/inbox/posts`
                axios.post(path, data19, TEAM19_CONFIG);
            }
        }
    }

    return response;
}

export const createComment = async (authorId, postId, data) => {
    let path = SERVER_URL + `/authors/${authorId}/posts/${postId}/comments`;
    const response = await axios.post(`${path}`,data);

    let author = await getAuthor(authorId);
    if (author === "Author does not exist") { return author; }
    let post = (await axios.get(SERVER_URL + `/authors/${authorId}/posts/${postId}`)).data;

    // TEAM 12
    // always send
    path = TEAM12_URL + `/authors/${authorId}/${author.displayName}/posts/${postId}/comments/`
    let data12 = {};
    data12.id = response.data.id;
    data12.comment = data.comment;
    data12.contentType = data.contentType;
    data12.author = authorId;
    data12.post = postId;
    axios.post(path, data12, TEAM12_CONFIG);

    // TEAM 19
    // Only send comment if author of post is a team 19 author
    if (post && post.author.host === TEAM19_URL) {
        let data19 = {};
        data19.author = author;
        data19.author.github = undefined;
        data19.comment = data.comment;
        data19.post = postId;
        data19.contentType = data.contentType;
        data19.published = new Date();
        path = TEAM19_URL + `/authors/${post.author.id}/inbox/comments`;
        axios.post(path, data19, TEAM19_CONFIG);
    }

    return response.data;
}

export const searchForAuthors = async (query, page, size) => {
    let path = SERVER_URL + `/find?query=${query}`
    if (page !== null) {
        path += `&page=${page}`;
    }
    if (size !== null) {
        //path += `&size=${size}`;
        path += `&size=${1000000}`;
    }
    const response = await axios.get(path);

    // TEAM 12
    path = TEAM12_URL + `/authors/`;
    let team12 = (await axios.get(path, TEAM12_CONFIG)).data;
    for (let author of team12) {
        if (author.username.includes(query)) { 
            author.type = "author";
            author.displayName = author.username;
            author.github = null;
            author.accepted = author.is_active;
            author.profileImage = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg";
            response.data.authorsPage.push(author);
        }
    }

    // TEAM 19
    path = TEAM19_URL + `/authors`;
    let team19 = (await axios.get(path, TEAM19_CONFIG)).data;
    for (let author of team19.items) {
        if (author.displayName.includes(query)) {
            author.accepted = true;
            author.id = author.id.split('/authors/')[1];
            response.data.authorsPage.push(author);
        }
    }

    // path = TEAM14_URL + `api/authors/`
    // if (page!== null){
    //     path += `?page=${page}`
    //     if (size!== null) path += `&size=${size}`
    // } 
    // const team14Authors = (await axios.get(path, TEAM14_CONFIG)).data
    // for (const author of team14Authors.results)
    //     if (author.display_name.includes(query)) response.data.authorsPage.push(Team14AuthorToLocalAuthor(author))

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
    // authorId is the follower
    // foreignAuthorId is the followed
    let foreignAuthor = await getAuthor(foreignAuthorId);
    if (foreignAuthor === "Author does not exist") { return foreignAuthor; }
    let path = SERVER_URL + `/authors/${authorId}/followers/${foreignAuthorId}`
    let data = {
        foreignAuthor: {
            id: foreignAuthorId,
            displayName: foreignAuthor.displayName,
            host: foreignAuthor.host
        }
    };
    const response = await axios.post(`${path}`, data);

    let author = await getAuthor(authorId);
    if (author === "Author does not exist") { return author; }
    if (foreignAuthor.host === TEAM12_URL) {
        // TEAM 12
        let path = TEAM12_URL + `/friendrequest/from_external/13/${authorId}/${author.displayName}/send/${foreignAuthorId}/`;
        axios.post(path, {}, TEAM12_CONFIG);
    } else if (foreignAuthor.host === TEAM19_URL) {
        // TEAM 19
        let path = TEAM19_URL + `/authors/${foreignAuthorId}/inbox/follows`;
        let data19 = {};
        data19.summary = `${author.displayName} wants to follow you`;
        data19.actor = {
            id: authorId,
            host: SERVER_URL,
            url: `${SERVER_URL}/authors/${authorId}`,
            displayName: author.displayName,
            profileImage: author.profileImage
        }
        axios.post(path, data19, TEAM19_CONFIG);
    }
    else if (foreignAuthor.host === TEAM14_URL){
        // let path = TEAM14_URL + `api/authors/${foreignAuthorId}/inbox/`
        // let body = Team14FollowRequestBody(authorId, foreignAuthorId)
        // axios.post(path, body, TEAM14_CONFIG)
    }

    return response.data;
}

export const removeFollower = async (authorId, foreignAuthorId) => {
    // authorId is the follower
    // foreignAuthorId is the followee

    let foreignAuthor = await getAuthor(foreignAuthorId);
    if (foreignAuthor === "Author does not exist") { return foreignAuthor; }
    
    let path = SERVER_URL + `/authors/${foreignAuthorId}/followers/${authorId}`;
    const response = await axios.delete(`${path}`);

    if (foreignAuthor.host === TEAM12_URL) {
        // TEAM 12
        path = TEAM12_URL + `/${authorId}/unfollow/${foreignAuthorId}/`
        axios.post(path, {}, TEAM12_CONFIG);
    } else if (foreignAuthor.host === TEAM19_URL) {
        // TEAM 19 has no logic required
        path = TEAM19_URL + `/authors/${foreignAuthorId}/followers/${authorId}`
        axios.delete(path, TEAM19_CONFIG);
    }
    return response.data;
}

export const getFollowRequests = async (authorId) => {
    const path = SERVER_URL + `/authors/${authorId}/followRequest`
    const response = await axios.get(`${path}`);
    return response.data
}

export const addFollower = async (authorId, foreignAuthorId) => {
    // authorid = followed
    // foreignAuthorId = follower
    let path = SERVER_URL + `/authors/${authorId}/followers/${foreignAuthorId}`
    const response = await axios.put(`${path}`);

    let foreignAuthor = await getAuthor(foreignAuthorId);
    if (foreignAuthor === "Author does not exist") { return foreignAuthor; }

    if (foreignAuthor.host === TEAM12_URL) {
        // TEAM 12
        let path = TEAM12_URL + `/friendrequest/accept_external/sender/${foreignAuthorId}/recipient/${authorId}/`
        axios.post(path, {}, TEAM12_CONFIG);
    } else if (foreignAuthor.host === TEAM19_URL) {
        // TEAM 19 has no logic required
    }

    return response.data;
}

export const removeFollowRequest = async (authorId, foreignAuthorId) => {  
    // authorId is the followee
    // foreignAuthorId is the follower  
    const path = SERVER_URL + `/authors/${authorId}/followRequest/${foreignAuthorId}`
    const response = await axios.delete(`${path}`);
 
    let foreignAuthor = await getAuthor(foreignAuthorId);
    if (foreignAuthor === "Author does not exist") { return foreignAuthor; }

    if (foreignAuthor.host === TEAM12_URL) {
        // TEAM 12
        path = TEAM12_URL + `/friendrequest/reject_external/sender/${foreignAuthorId}/recipient/${authorId}/`
        axios.post(path, {}, TEAM12_CONFIG);
    } else if (foreignAuthor.host === TEAM19_URL) {
        // TEAM 19 has no logic required

    }

    return response.data;
}

export const createUser = async (data) => {
    const path = SERVER_URL + `/users`
    const response = await axios.post(`${path}`, data);
    return response.data;
}

export const loginUser = async (data) => {
    const path = SERVER_URL + `/users`
    data.withCredentials = true;
    const response = await axios.put(`${path}`, data).catch((error) => {
        alert("The username or password you entered are incorrect.")
        return {
            status: error.response.status
        }
    });

    if (response.status < 400) {
        return response.data;
    } else {
        return false;
    }
}

export const authUser = async (data) => {
    const path = SERVER_URL + `/users/auth`
    const response = await axios.post(`${path}`, data);
    return response.data;
}

export const deletePost = async(authorId, postId) => {
    let path = SERVER_URL + `/authors/${authorId}/posts/${postId}`
    const response = await axios.delete(path);

    // TEAM 12
    path = TEAM12_URL + `/posts/${postId}/`;
    axios.delete(path, TEAM12_CONFIG);

    // TEAM 19 has no logic required for this
    return response.data;
};

export const modifyPost = async (authorId, postId, data) => {
    let path = SERVER_URL + `/authors/${authorId}/posts/${postId}`;
    axios.post(path, data);

    // TEAM 12
    path = TEAM12_URL + `/posts/${postId}/`;
    let data12 = {};
    data12.title = data.title;
    data12.content = data.content;
    data12.description = data.description;
    data12.contentType = data.contentType;
    axios.put(path, data12, TEAM12_CONFIG);

    // TEAM 19 has no logic required for this
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

export const getGithubEvents = async (github) => {
    let githubUsername = github.split(".com/")[1];
    if (!githubUsername) { githubUsername = github; }
    const path = `https://api.github.com/users/${githubUsername}/events`;
    let response = await axios.get(path, {headers: {Authorization: ""}});
    return response.data;
}
