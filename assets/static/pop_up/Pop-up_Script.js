class PopUpController extends React.Component{
     constructor(props) {
        super(props);
        this.state = {title: '<EMPTY>', message: '<EMPTY>', visible: 'none', escapable: true};
     }

    render(){
        //var vis = this.state.visible;
        return (<div className="popup" style={{display: this.state.visible}}>
                    <div className="popup-background" onClick={() => this.closePopUp()}></div>
                    <div className="popup-Screen">
                        <div className="popup-Topbar">
                            <p className="popup-title">{this.state.title}</p>
                            <button className="popup-closebutton" onClick={() => this.closePopUp()}>x</button>
                        </div>
                        <div className="popup-Container">
                            {this.state.message}
                        </div>
                    </div>
                </div>);
    }

    ShowSimpleMessage(Title, Message)
    {
        var messageContent = (<div>
                <p>{Message}</p>
                <button onClick={() => this.closePopUp()}>Ok</button>
            </div>);

        this.setState({title: Title, message: messageContent, visible: 'initial'});
    }

    ShowCustomPopUp(Title, Content)
    {
        this.setState({title: Title, message: Content, visible: 'initial'});
        //document.getElementById('root').innerHTML = "Made PopUp with Content";
    }

    closePopUp()
    {
        /// TODO: insert remove content code

        // Clear the Pop-up and remove the pop-up
        this.setState({title: 'EMPTY', message: '', visible: 'none'});
    }

}



/*      THIS IS THE OUTER PART          */


var popUpController = ReactDOM.render(
    <PopUpController/>,
    document.getElementById('PopUpContainer')
);

function CreatePopUpMessage(Title, Message)
{
    popUpController.ShowSimpleMessage(Title, Message);
}

function CreatePopUpWithContent(Title, Content)
{
    //document.getElementById('root').innerHTML = "Make PopUp with Content";
    popUpController.ShowCustomPopUp(Title, Content);

}