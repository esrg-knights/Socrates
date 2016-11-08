import React from 'react';/(?P<pk>[^/.]+)/$ [name='user-detail']
^api/ ^ ^user/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='user-detail']
^api/ ^auth$
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