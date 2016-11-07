import React from 'react';
import ApiService from '../service/ApiService';

export default class Profile extends React.Component{
  constructor(props){
    super(props);
  }

  componentDidMount(){
    new ApiService().get("dinner").then(response => console.log(response));
  }

  render(){
    return(
      <div>
        <h1>Ik ben profile</h1>
      </div>
    )
  }
}