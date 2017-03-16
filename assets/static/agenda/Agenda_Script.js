class EventDate extends React.Component {

    render()
    {
        var namestyle = {   marginTop: 0 + 'px',
                            marginBottom: 4 + 'px',};
        var remark = "";
        if (this.props.remark.length > 0)
            remark = (<p>{this.props.remark}</p>);


        return (
             <div className="AgendaBlock" >
                <h3 className="AgendaName">{this.props.name}</h3>
                <div className="AgendaInfo">
                    <div className="AgendaDate">{this.props.date}</div>
                    <div className="AgendaRemark">{remark}</div>
                </div>
             </div>
         );
    }
}