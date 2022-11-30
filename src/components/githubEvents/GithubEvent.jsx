
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

export default function BasicCard(props) {
  // props contains item
  // which is a github event item
  if (!props.item.type || !props.item.repo || !props.item.created_at) { return; }

  const date = new Date(props.item.created_at);
  const dateString = `${date.getFullYear()}-${date.getMonth()+1}-${+date.getDate()<10 ? '0' : ''}${date.getDate()}`;
  return (
    <Card sx={{ minWidth: 275 }} style={{backgroundColor: "#FAF9F6"}}>
      <CardContent>
        <Typography sx={{ fontSize: 12 }} color="text.primary">
          {`You made a ${props.item.type} on repo "${props.item.repo.name}" on ${dateString}`}
        </Typography>
      </CardContent>
    </Card>
  );
}