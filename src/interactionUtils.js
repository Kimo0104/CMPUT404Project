//const TEAM14_URL = "https://social-distribution-14degrees.herokuapp.com/"
export const TEAM14_URL = "http://localhost:5900/"
export const TEAM14_CONFIG = {
    auth: {username: 'team13', password: 'kareem'}, 
    headers: {"Content-Type": "application/json"}
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