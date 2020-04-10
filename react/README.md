> To run the sample code provide you must also run the backend.
(An account has already been created, user: pc, password: 1234)
# React Redux
Redux in react is generally used for the purpose of creating a centralized `store` (similar to a "state") that holds the data that needs to be shared across multiple components and that would otherwise be very difficult to access through component prop drilling.

The **View** is basically your react components. The **Store** which includes your state, sends your state down to your component.
Inside your component you may have a button that you click or a form that needs to be submitted and that will fire off an action,  which will then **dispach** an action to the **store**. You then have these **reducers** which are pure functions that specify how the application state should change in response to that **action**, the **reducers** will then respond with that new state. 
**This new state gets sent down to the component and the component then reacts accordingly.**
![redux diagram](https://res.cloudinary.com/practicaldev/image/fetch/s--m5BdPzhS--/c_limit,f_auto,fl_progressive,q_66,w_880/https://i.imgur.com/riadAin.gif)
> To install react-redux:
> `npm install redux react-redux --save`

Check other usage docs here: [link](https://www.npmjs.com/package/redux-react-session)
# React-Redux (w/ Thunk) - Sessions
This document outlines the structural and functional aspects of a [Django and React Tutorial](www.youtube.com/watch?v=BxzO2M7QcZw).

 - Application **src** folder Structure
	 - components 
		 - Article.js
		 - Form.js
	- containers
		- ArticleDetailView.js
		- ArticleListView.js
		- Layout.js
		- Login.js
		- Signup.js
	- store
		- actions
			- actionTypes.js
			- auth.js
		- reducers
			- auth.js
		- utility.js => this is for the helper methods
	- App.js
	- index.js
	- routes.js
#### The Store Structure
The store is used to maintain the state for the entire application, it also holds the `actions` and the `reducers`. The `actions` are essentially functions that work as **events**, so they have very event like names such as "authStart ", their purpose is to return an **object** (that generally contain a `type` and maybe an extra field, typically called `payload`) that specifies what needs to be changed within the state, they can also return a `dispach => {...}`, within which you may also `dispach()` other actions. From my understanding, the `reducer` gets executed whenever an object is returned by an action, it then takes that object and returns the updated state.
> actionTypes.js
```jsx
export  const  AUTH_START = "AUTH_START";
export  const  AUTH_SUCCESS = "AUTH_SUCCESS";
export  const  AUTH_FAIL = "AUTH_FAIL";
export  const  AUTH_LOGOUT = "AUTH_LOGOUT";
```
##### Note: The actionTypes files exists as a separate file so that other javascript files can import it and use its variables rather than passing strings around, the reason why that is better is because if you pass a wrong string it won't throw an error but if you use the wrong var it will.
 >auth.js (from **actions**)
```jsx
import * as actionTypes from './actionTypes';
import axios from 'axios'


export const authStart = () => {
    return {
        type: actionTypes.AUTH_START
    }
}

export const authSuccess = token => {
    return {
        type: actionTypes.AUTH_SUCCESS,
        token: token
    }
}

export const authFail = error => {
    alert("Failed to Login")
    return {
        type: actionTypes.AUTH_FAIL,
        error: error
    }
}

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('expirationDate');
    return {
        type: actionTypes.AUTH_LOGOUT
    }
}

export const checkAuthTimeout = expirationTime => {
    return dispatch => {
        setTimeout(() => {
            dispatch(logout());
        }, expirationTime * 1000);
    }
}

export const authLogin = (username, password) => {
    return dispatch => {
        dispatch(authStart());
        axios.post('http://127.0.0.1:8000/rest-auth/login/', {
            username: username,
            password: password
        })
            .then(res => {
                const token = res.data.key;
                const expirationDate = new Date(new Date().getTime() + 3600 * 1000);
                localStorage.setItem('token', token);
                localStorage.setItem('expirationDate', expirationDate);
                dispatch(authSuccess(token));
                dispatch(checkAuthTimeout(10)); //10 seconds
            })
            .catch(err => {
                dispatch(authFail(err))
            })
    }
}

export const authSignup = (username, email, password1, password2) => {
    return dispatch => {
        dispatch(authStart());
        axios.post('http://127.0.0.1:8000/rest-auth/registration/', {
            username: username,
            email: email,
            password1: password1,
            password2: password2
        })
            .then(res => {
                const token = res.data.key;
                const expirationDate = new Date(new Date().getTime() + 3600 * 1000);
                localStorage.setItem('token', token);
                localStorage.setItem('expirationDate', expirationDate);
                dispatch(authSuccess(token));
                dispatch(checkAuthTimeout(10)); //10 seconds
            })
            .catch(err => {
                dispatch(authFail(err))
            })
    }
}

export const authCheckState = () => {
    return dispatch => {
        const token = localStorage.getItem('token');
        if (token === undefined) {
            dispatch(logout());
        } else {
            const expirationDate = new Date(localStorage.getItem('expirationDate'));
            if (expirationDate <= new Date()) {
                dispatch(logout());
            } else {
                dispatch(authSuccess(token));
                dispatch(checkAuthTimeout((expirationDate.getTime() - new Date().getTime()) / 1000));
            }
        }
    }
}
```
The actions above are typically useful for handling sessions, notice that when you call methods defined in actions, you must use `dispatch`. For implementation purposes, the reducer is not called directly, their only reference lies, in this example, in the **index.js**, which will be shown further down this document.
> auth.js (from **reducers**)
```jsx
import * as actionTypes from '../actions/actionTypes';
import { updateObject } from '../utility';

const initialState = {
    token: null,
    error: null,
    loading: false
}

const authStart = (state, action) => {
    return updateObject(state, {
        error: null,
        loading: true
    })
}

const authSuccess = (state, action) => {
    return updateObject(state, {
        token: action.token,
        error: null,
        loading: false
    })
}

const authFail = (state, action) => {
    return updateObject(state, {
        error: action.error,
        loading: false
    })
}

const authLogout = (state, action) => {
    return updateObject(state, {
        token: null,
    })
}

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case actionTypes.AUTH_START: return authStart(state, action);
        case actionTypes.AUTH_SUCCESS: return authSuccess(state, action);
        case actionTypes.AUTH_FAIL: return authFail(state, action);
        case actionTypes.AUTH_LOGOUT: return authLogout(state, action);
        default:
            return state;
    }
}

export default reducer;
```
>utility.js
```jsx
// this is just a helper funtion, this file can be used to hold these methods
export const updateObject = (oldObject, updatedProperties) => {
    return {
        ...oldObject,
        ...updatedProperties
    }
}
```
>index.js

To use a store in the children of a given parent component you must include the following boilerplate in this parent and use a `<Provider>` to encapsulate the children component or components in which you want to access the store, that holds all of the components that you want to be able to access the store, in this case, it was included in index.js.
```jsx
(...)
// BOILERPLATE
import reducer from './store/reducers/auth';
import {createStore, compose, applyMiddleware} from 'redux';
import {Provider} from 'react-redux';
import thunk from 'redux-thunk';

const composeEnhancer = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(reducer, composeEnhancer(
    applyMiddleware(thunk)
))

const app = (
    <Provider store={store}>
        <App/>
    </Provider>
)

ReactDOM.render(app, document.getElementById('root'));
```
> Layout.js

This example shows how to access the `state` and **actions** defined in the store.
The `connect()` (at the end of the code) receives 2 methods, the **first** is used to map the state to the props of the component of the given .js file that you're on, the **second** is to map the **actions**. Again, note that these can only be called with `dispach()`
In essence, `connect()` is mapping the store's state and actions to the props of the current component.
```jsx
import React from 'react';
import { Layout, Menu, Breadcrumb } from 'antd';
import { Link } from 'react-router-dom';

import { connect } from 'react-redux';
import * as actions from '../store/actions/auth'; //this works like a namespace

const { Header, Content, Footer } = Layout;

const CustomLayout = (props) => {
    return (
        <Layout className="layout">
            <Header>
                <div className="logo" />
                <Menu
                    theme="dark"
                    mode="horizontal"
                    defaultSelectedKeys={['2']}
                    style={{ lineHeight: '64px' }}
                >
                    <Menu.Item key="1"><Link to="/">Posts</Link></Menu.Item>
                    {

                        props.isAuthenticated ?

                            <Menu.Item key="2" onClick={props.logout}>Logout</Menu.Item>

                            :

                            <Menu.Item key="2"><Link to="/login">Login</Link></Menu.Item>
                    }
                </Menu>
            </Header>
            <Content style={{ padding: '0 50px' }}>
                <Breadcrumb style={{ margin: '16px 0' }}>
                    <Breadcrumb.Item><Link to='/'>Home</Link></Breadcrumb.Item>
                    <Breadcrumb.Item>List</Breadcrumb.Item>
                    <Breadcrumb.Item>App</Breadcrumb.Item>
                </Breadcrumb>
                <div style={site_layout_content}>
                    {props.children}
                </div>
            </Content>
            <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
        </Layout>
    );
}

const site_layout_content = {
    background: '#fff',
    padding: '24px',
    minHeight: '280px',
}

const mapStateToProps = state => {    //these become props in the app
    return {
        isAuthenticated: state.token !== null
    }
}

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.logout()),
        onTryAutoSignup: () => dispatch(actions.authCheckState())
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(CustomLayout);
```

## Preview Samples:
![Previe1](./img/Preview1.png)
![Previe2](./img/Preview2.png)