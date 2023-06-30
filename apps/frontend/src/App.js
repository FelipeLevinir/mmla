import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Nav, Navbar } from 'react-bootstrap';
import {Route, Routes, Link} from 'react-router-dom';

// import views
import Home from "./components/views/home.component";
import NotFound from "./components/views/notFound.component";
import Activities from "./components/activities/activities.component";
import Files from "./components/files/files.component";
import Analysis from "./components/analysis/analysis.component";
import Indicator from "./components/indicator/indicators.component";
import VideoMarker from "./components/events/events.component";
import Experiments from "./components/experiments/experiments.component"
import MarkTypes from "./components/markstype/marktype.component"
import MarktLevel from "./components/marklevel/marklevel.component"
import CreateExperiment from "./components/experiments/createExperiment.component"
import CreateMarkType from "./components/markstype/createMarktype.component"
import CreateActivities from "./components/activities/createActivities.component";
import CreateMarkLevel from "./components/marklevel/createMarklevel.component";

function App() {
  return (
    <div className="App">
      <header className="header">
        <Navbar bg="light" expand="lg">
          <Container>
            <Navbar.Brand href="/home">
              <img
                alt=""
                src={logo}
                width="30"
                height="30"
                className="d-inline-block align-top"
              />{' '}
              Virtual Device
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
              <Nav className="me-auto">
                <Link to={"/home"} className="nav-link">
                  Home
                </Link>
                <Link to={"/experiments"} className="nav-link">
                  Experiments
                </Link>
                {/* <Link to={"/activities"} className="nav-link">
                  Activities
                </Link> */}
                <Link to={"/analysis"} className="nav-link">
                  Analysis
                </Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </header>
      <section>
        <Container>
          <Routes>
            <Route exact path="/" element={<Home />}/>
            <Route exact path="/home" element={<Home />}/>
            <Route exact path="/experiments" element={<Experiments />}/>
            <Route exact path="/create-experiment" element={<CreateExperiment />}/>
            <Route exact path="/experiment/:id_experiment/marktypes" element={<MarkTypes />}/>
            <Route exact path="/experiment/:id_experiment/marktypes/create-marktype" element={<CreateMarkType />}/>
            <Route exact path="/marktypes/:id_marktype/marklevel" element={<MarktLevel />}/>
            <Route exact path="/marktypes/:id_marktype/marklevel/create-marktype" element={<CreateMarkLevel />}/>
            <Route exact path="/experiment/:id_experiment/activities" element={<Activities />}/>
            <Route exact path="/activities/:id_activity/events" element={<VideoMarker />}/>
            <Route exact path="/activity/files/:name" element={<Files />}/>
            <Route exact path="/experiment/:id_experiment/activities/create-activity" element={<CreateActivities />}/>
            <Route exact path="/analysis" element={<Analysis />}/>
            <Route exact path="/indicator/:id_analysis" element={<Indicator />}/>
            <Route path='*' element={<NotFound />}/>
          </Routes>
        </Container>
      </section>
      <footer className='mt-auto py-3 bg-light'>
      <Navbar bg="light">
        <Container>
          <Navbar.Brand href="#home">© uv.cl</Navbar.Brand>
        </Container>
      </Navbar>
      </footer>
    </div>
  );
}

export default App;
