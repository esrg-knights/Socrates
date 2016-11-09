import React from 'react';
import ApiService from '../service/ApiService';

export default class DinnerList extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      data: "Incoming"
    }
  }

  componentDidMount(){
    new ApiService().get("dinner").then(response => this.setState({
      data: response["results"][0]["relevant_date"]
    }));
  }

  render(){
    return(
      <div>
        <h1>Ik ben profile</h1>
        <p>{this.state.data}</p>
      </div>
    )
  }
}