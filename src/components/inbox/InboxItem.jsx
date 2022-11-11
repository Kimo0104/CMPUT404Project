import TextPost from './TextPost'
import CommentPost from './CommentPost'
import LikePost from './LikePost'

export default function InboxItem(props) {
    if (props.item.type === "post") {
        return (
            <TextPost 
                authorId={props.authorId} 
                title={props.item.title} 
                source={props.item.source}
                origin={props.item.origin}
                description={props.item.description}
                contentType={props.item.contentType}
                content={props.item.content} 
                originalAuthor={props.item.originalAuthor}
                visibility={props.item.visibility}
                postId={props.item.id}
            />
        );
    } else if (props.item.type === "comment") {
        return (
            <CommentPost commenterAuthorId={props.item.author} commentPostId={props.item.post} comment={props.item.comment}/>
        );
    } else if (props.item.type === "like") {
        return (
            <LikePost summary={props.item.summary} context={props.item.context}/>
        );
    }
}