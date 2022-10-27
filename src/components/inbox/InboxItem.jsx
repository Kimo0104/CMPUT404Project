import TextPost from './TextPost'
import CommentPost from './CommentPost'
import LikePost from './LikePost'

export default function InboxItem(props) {
    if (props.item.type === "post") {
        return (
            <TextPost 
                authorId={props.authorId} 
                title={props.item.title} 
                content={props.item.content} 
                postAuthorId={props.item.author} 
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