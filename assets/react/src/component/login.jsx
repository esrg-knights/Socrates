import * as React from "react";
import {Binder} from "react-binding";
import {AuthService} from "../service/AuthService";
import authStore from "../stores/AuthStore";
import { hashHistory } from 'react-router';

export default class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: '',
            password: ''
        };

        if(!authStore.getState().length != 0){
            hashHistory.push('profile');
        }

        this.subscription = authStore.subscribe(() => {
            console.log(authStore.getState());
            if (localStorage.getItem("jwt") != "") {
                hashHistory.push('profile');
            }
        });

        this.login = this.login.bind(this);
    }

    login(e) {
        e.preventDefault();

        console.log(this.state);

        new AuthService().login(this.state.user, this.state.password);
    }

    render() {
        return (
            <div>
                <form role="form">

                    <input type="text" valueLink={Binder.bindToState(this, 'user')} placeholder="Username"/>
                    <input type="password" valueLink={Binder.bindToState(this, 'password')} placeholder="Password"/>
                    <button type="submit" onClick={this.login}>Submit</button>
                </form>
            </div>
        )
    }
}