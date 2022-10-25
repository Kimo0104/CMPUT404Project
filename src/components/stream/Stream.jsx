import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import { makeStyles } from '@material-ui/core';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import { getInbox } from '../../APIRequests';

const useStyles = makeStyles((theme) => ({
  dialogWrapper: {
    padding: theme.spacing(2),
    position: 'absolute',
    top: theme.spacing(5),
  },
  dialogTitle: {
    paddingRight: '0px',
  },
}));

export default function FormDialog(props) {
  //props requires authorId
  const classes = useStyles();

  const [orgName, setOrgName] = React.useState('');
  
  const handleInputChange = (event) => {
    setOrgName(event.target.value);
  };

  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleCreate = () => {
    // creates an organization
    // adds user to organization as an admin
    async function createNewOrg() {
        const output = await getInbox(props.authorId);
        console.log(output);
    }
    createNewOrg();

    setOpen(false);
  };

  return (
    <div style={{ display: 'flex' }}>
      <Button onClick={handleClickOpen} variant="outlined">Create Organization</Button>
      <Dialog open={open} onClose={handleClose} fullWidth={true} maxWidth={'md'}>
        <DialogTitle className={classes.dialogTitle}>Create New Organization</DialogTitle>
        <DialogContent>
          <Grid container rowSpacing={4} paddingBottom={10}>
              <Grid item xs = {12}>
                <div style={{display: "flex", alignItems: "center", justifyContent: "left"}}>
                  <Grid container>
                    <Grid item xs = {6}>
                        <TextField
                        autoFocus
                        onChange={handleInputChange}
                        margin="dense"
                        id="orgName"
                        label={"Organization Name"}
                        type="text"
                        variant="standard"
                        />
                    </Grid>
                  </Grid>
                </div>
              </Grid>
          </Grid>
          <Grid container rowSpacing={4} paddingBottom={10}>
              <Grid item xs = {12}>
                <DialogContentText align="left">
                    REPLACE THIS WITH PAYMENT COMPONENT
                </DialogContentText>
              </Grid>
          </Grid>
          <Grid container>
              <Grid item xs={12} position="absolute" right={20} bottom={8}>
                <DialogActions>
                    <Button onClick={handleClose} color="error" variant="outlined">
                        Cancel
                    </Button>
                    <Button onClick={handleCreate} color="success" variant="contained">
                        Create
                    </Button>
                </DialogActions>
              </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </div>
  );
}
