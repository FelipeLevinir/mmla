import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { useNavigate  } from "react-router-dom";
import ListGroup from 'react-bootstrap/ListGroup';
import ActivityService from "../../services/activities.service";
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ModalAnalyzeActivity from "../analysis/modalAnalyzeActivity";

const ActivityRow = (props) => {
    const { name, audiofile, videofile} = props.obj;
    const [ idActivities ,setIdActivities ] = useState("");
    let navigate = useNavigate();
    const [modalShow, setModalShow] = useState(false);
    // const idValue = _id.$oid;

    // const editActivity = () => {
    //     navigate("/edit-activity/");
    // };
    useEffect(() => {
        ActivityService.get(name)
          .then(({ data }) => {
            //console.log(data)
            setIdActivities(data._id.$oid);
          })
          .catch((error) => {
            console.log(error);
          });

      }, []);
    const goToMarkEvents = () =>{
        //console.log(nameActivities);
        navigate(`/activities/${idActivities}/events`);
    }

    const goTofiles = () => {
        navigate("/activity/files/" + name);
    };

    // const analyzeActivity = () => {
    //     //POR IMPLEMENTAR
    // };

    const deleteActivity = () => {
        ActivityService.remove(name).then((res) => {
            if (res.status === 200) {
                alert("Activity successfully deleted");
                window.location.reload();
            } else Promise.reject();
        })
        .catch((err) => {
            alert("Something went wrong")
        });
    };
    
    return (
        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
                <div className="fw-bold">{name}</div>
            </div>
            <ButtonGroup aria-label="actions">
                <Button onClick={goTofiles} variant="outline-primary">
                    <i className="bi bi-card-list"> Files</i>
                </Button>
                {/* <Button onClick={editActivity} variant="outline-secondary">
                    <i className="bi bi-pencil-square"> Edit</i>
                </Button> */}
                <Button onClick={() => setModalShow(true)} variant="outline-primary">
                    <i className="bi bi-search"> Analyze</i>
                </Button>
                <Button onClick={goToMarkEvents} variant="outline-primary">
                    <i className="bi bi-collection-play"> Events</i>
                </Button>
                <Button onClick={deleteActivity} variant="outline-danger">
                    <i className="bi bi-trash"> Remove</i>
                </Button>
            </ButtonGroup>
            <ModalAnalyzeActivity
                show={modalShow}
                onHide={() => setModalShow(false)}
                activity={name}
            />
        </ListGroup.Item>
    );
  };
    
  export default ActivityRow;