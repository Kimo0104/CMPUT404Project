import { TransformRounded } from "@mui/icons-material";

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
    let transformed = {}
    transformed.id = author.id
    transformed.type = "author"
    transformed.host = TEAM14_URL
    transformed.displayName = author.display_name
    transformed.url = author.url
    transformed.github = author.github_handle
    transformed.accepted = true
    transformed.profileImage = author.profile_image
    return transformed
}