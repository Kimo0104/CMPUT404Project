export const SERVER_URL = process.env.REACT_APP_SERVER_URL || "http://localhost:8000";
export const TEAM14_URL = "http://localhost:5900/"
//export const TEAM14_URL = "https://social-distribution-14degrees.herokuapp.com/"
export const TEAM14_CONFIG = {
    auth: {username: 'team13', password: 'kareem'}, 
    headers: {"Content-Type": "application/json"}
};
export const TEAM12_URL = "https://true-friends-404.herokuapp.com";
export const TEAM12_CONFIG = {
    headers: {
        Authorization: "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NDQxOTA4LCJpYXQiOjE2Njk4MDE5MDgsImp0aSI6IjIxMjYzYTFjMmY0YTQwMTViNmJkMjllNGViMTVhZTAyIiwidXNlcl9lbWFpbCI6InRlYW0xM0BtYWlsLmNvbSJ9.UiyWRyd4RUbE6GZALe-HkuegXhJrE_ufx5hNoAeIArk",
        "Content-Type": "application/json"
    }
}
export const TEAM19_URL = "https://social-distribution-404.herokuapp.com";
export const TEAM19_CONFIG = {
    auth: {username: 'Admin13', password: 'password'}, 
    headers: {"Content-Type": "application/json",}
};

/*
Defines a transformation from a team 14 author object
to a local author object.
*/
export const Team14AuthorToLocalAuthor = (author) => {
    let transformed = {
        id: author.id,
        type: "author",
        host: TEAM14_URL,
        displayName: author.display_name,
        url: author.url,
        github: author.github_handle,
        accepted: true,
        profileImage: author.profile_image
    }
    return transformed
}
/*
Returns the body for sending a follow request to a team 14 author
*/
export const Team14FollowRequestBody = (author, foreignAuthor) => {
    let body = {
        "type" : "follow",
        "sender" : {
            "url": SERVER_URL + `/authors/${author}`,
            "id": author
        },
        "receiver" : {
            "url": TEAM14_URL + `api/authors/${foreignAuthor}`,
            "id": foreignAuthor
        }   
    }
    return body
}