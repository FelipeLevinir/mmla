import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import ListGroup from 'react-bootstrap/ListGroup';
import ExperimentService from "../../services/experiments.service";
import ButtonGroup from 'react-bootstrap/ButtonGroup';

const ExperimentRow = (props) => {
    const { name, code } = props.obj;
    const [res, setRes] = useState({});
    const [experimentId, setExperimentId] = useState(null);
    let navigate = useNavigate();

    useEffect(() => {
        getExperimentID(code)
            .then((id) => setExperimentId(id))
            .catch((error) => console.log(error));
    }, [code]);

    const getExperimentID = (experimentCode) => {
        return new Promise((resolve, reject) => {
            ExperimentService.get(experimentCode)
                .then((response) => {
                    const experimentId = response.data._id.$oid;
                    resolve(experimentId);
                })
                .catch((error) => {
                    console.log(error);
                    reject(error);
                });
        });
    };

    const goToMarkType = () => {
        if (experimentId) {
            navigate(`/experiment/${experimentId}/marktypes`);
        } else {
            console.log("Experiment ID is undefined");
        }
    };

    const showExperimentDetail = async () => {
        try {
            const response = await ExperimentService.get(code);
            setRes(response.data);
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const deleteExperiment = () => {
        ExperimentService.remove(code)
            .then((res) => {
                if (res.status === 200) {
                    alert("Experiment successfully deleted");
                    window.location.reload();
                } else Promise.reject();
            })
            .catch((err) => {
                alert("Something went wrong");
                console.log(err);
            });
    };

    const goToActivies = () => {
        navigate(`/experiment/${experimentId}/activities`);
    }

    return (
        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
                <div className="fw-bold">{name}</div>
            </div>
            <div className="ms-2 me-auto">
                <div className="fw-bold">{code}</div>
            </div>
            <ButtonGroup aria-label="actions">
                <Button onClick={showExperimentDetail} variant="outline-primary">
                    <i className="bi bi-file-earmark-plus"> Detail</i>
                </Button>
                <Button onClick={goToMarkType} variant="outline-primary">
                    <i className="bi bi-bookmark-star"> Mark Type</i>
                </Button>
                <Button onClick={goToActivies} variant="outline-primary">
                    <i className="bi bi-calendar2-event"> Activities</i>
                </Button>
                <Button variant="outline-primary">
                    <i className="bi bi-card-list"> Edit</i>
                </Button>
                <Button onClick={deleteExperiment} variant="outline-danger">
                    <i className="bi bi-trash"> Remove</i>
                </Button>
            </ButtonGroup>
        </ListGroup.Item>
    );
};

export default ExperimentRow;
