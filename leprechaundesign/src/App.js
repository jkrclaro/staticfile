import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from './components/Home';
import Contact from './components/Contact';
import NotFound from './components/NotFound';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faCopyright, faTh } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';

library.add(fab, faCopyright, faTh);


class App extends Component {

    render() {
        return(
            <BrowserRouter basename={process.env.PUBLIC_URL}>
                <Switch>
                    <Route exact path={process.env.PUBLIC_URL + '/'} component={Home} />
                    <Route path={process.env.PUBLIC_URL + '/contact'} component={Contact} />
                    <Route component={NotFound} />
                </Switch>
            </BrowserRouter>
        )
    }
}

export default App;