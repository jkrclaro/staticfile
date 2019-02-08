import React from 'react';

import Header from './Header';

const stock1 = require('../imgs/stock1.jpg');
const stock2 = require('../imgs/stock2.jpg');
const stock3 = require('../imgs/stock3.jpg');


class Home extends React.Component {

    state = {
        isDesktop: false,
        settings: {
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 1,
            slidesToScroll: 1
        }
    }
    updatePredicate = this.updatePredicate.bind(this);

    componentDidMount() {
        this.updatePredicate();
        window.addEventListener('resize', this.updatePredicate);
    };

    componentWillUnmount() {
        window.removeEventListener('resize', this.updatePredicate);
    };

    updatePredicate() {
        this.setState({ isDesktop: window.innerWidth > 992 });
    };

    render() {
        return (
            <div>
                {this.state.isDesktop ? (
                    <div className='section-1'>
                        <Header/>
                        <div className='container'>
                            <div className='row'>
                                <div className='col-lg-6' style={{paddingTop: 225}}>
                                    <h1>TAKE A JOURNEY THROUGH DUBLIN'S AND IRELAND'S HISTORY</h1>
                                    <a href='https://www.airbnb.ie/experiences/385040' className='btn btn-custom-primary'>Book now</a>
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div>
                        <div className='section-2'>
                            <Header/>
                        </div>
                        <div className='container'>
                            <div className='row'>
                                <div className='col-lg-6 mt-5'>
                                    <h3 className='h3-heading text-center'>TAKE A JOURNEY THROUGH DUBLIN'S AND IRELAND'S HISTORY</h3>
                                    <a className='btn btn-custom-primary btn-block'>Book now</a>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                <div className='container mt-5 mb-5'>
                    <div className='row'>
                        <div className='col-lg-6 mt-5'>
                            <h3 className='h3-heading'>ABOUT YOUR HOST</h3>
                            <p className='p-content'>
                            How often do you meet a historian who's also a professional beer expert? 
                            I'm Nils and I have created my own tour combining history and beer. 
                            Having established the tour in Berlin (Rated 4.93/5 from 374 reviews),
                            I have now decided to do the same in my hometown.
                            Born and bred in Dublin, I have a degree in Irish history from Trinity College, 
                            and have also worked as a guide in the Guinness Brewery. 
                            All this puts me in a offer position to offer insights on 
                            both Ireland's history and its favourite beer.
                            </p>
                        </div>
                        <div className='col-lg-6 mt-5 mb-5'>
                            <img src={stock2} className='img-fluid'></img>
                        </div>
                    </div>
                </div>
                <div style={{backgroundColor: '#ddd'}}>
                    <div className='container'>
                        <div className='col-lg-12'>
                            <h3 className='h3-heading'>WHAT WE'LL DO</h3>
                            <p className='p-content'>
                            Join me as we take a journey through Dublin’s and Ireland’s history, focussing on the most important figures of the last centuries; from St. Patrick to Queen Elizabeth, from Oscar Wilde to Bono. 
                            As we make our way through the city, we’ll discuss it all - from the first English invasion up to Brexit, from the arrival of St. Patrick up to the abortion referendum of 2018. And everything in between. We’ll see how this history has shaped Dublin, and how its legacy can still be seen all over the city today. 
                            After 2 hours of history, we'll head to one of my favourite pubs and enjoy a pint of Guinness (pint is included in the price of the tour). As we enjoy it, I’ll tell you everything there is to know about the beer, especially important info that you wouldn't necessarily hear at the Guinness Storehouse – Why does it take so long to pour a pint? Why is it so beloved in Ireland? Why is it so smooth and creamy? Why does it taste so much better here than elsewhere? Why does every can of Guinness have a plastic ball in it?
                            Fascinating history followed by a delicious pint. What could be better?
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Home;