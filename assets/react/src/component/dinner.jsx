import React from "react";
import {DinnerService} from "../service/DinnerService";
import DinnerRow from "./dinnerRow";

export default class DinnerList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      data: {},
      participants: []
    }
  }

  componentDidMount() {
    new DinnerService().get().then(result => {
      result = result['results'][0];
      console.log(result.participations);
      this.setState({
        data: result,
        participants: result.participations
      })
    })
  }

  render() {
    return (
      <div>
        <h1>{this.state.data.relevant_date}</h1>
        {this.state.participants.map(function (object, i) {
          return <DinnerRow key={i} obj={object} />;
        })}
      </div>
    )
  }
}