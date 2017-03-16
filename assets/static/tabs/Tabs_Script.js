class TabContainer extends React.Component {

    constructor(props) {
        super(props);

        // Set the state
        this.state = {selected: 0};
    }

    tabClicked(e){
        var text = e.currentTarget.innerHTML;
        for(var i = 0; i < this.props.tabTitles.length; i++)
        {
            if (text == this.props.tabTitles[i])
            {
                if (i != this.state.selected){
                    this.setState({selected: i});
                }
                return;
            }
        }

        //this.setState({selected: i});
    }

    renderNavigation() {

        var titleBoxes = [];
        var classDesc;
        for(var i = 0; i < this.props.tabTitles.length; i++)
        {
            var t = i;
            if (this.state.selected == i)
                classDesc = "TabBox selected";
            else
                classDesc = "TabBox";

            titleBoxes.push(
                <div key={i} className={classDesc} onClick={(e) => this.tabClicked(e)}>
                    {this.props.tabTitles[i]}
                </div>
                );
        }

        return(
            <div className="TabHeader">
                {titleBoxes}
            </div>
        );
    }

    render()
    {
        return(
            <div className={this.props.class}>
                {this.renderNavigation()}
                <div className="TabHeaderLine"/>
                <div className="TabContent">
                    {this.props.tabContent[this.state.selected]}
                </div>
            </div>
        );
    }
}