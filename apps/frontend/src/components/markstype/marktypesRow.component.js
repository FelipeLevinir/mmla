import React, { useState } from "react";
import { Button } from "react-bootstrap";
import { useNavigate  } from "react-router-dom";
import ListGroup from 'react-bootstrap/ListGroup';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import MarkTypeService from "../../services/marktypes.service";

const MarkTypeRow = (props) => {
    const { name, _id } = props.obj;
    let navigate = useNavigate();
    const idValue = _id.$oid;
    //console.log(_id);

const DeleteMarkType = () => {
    MarkTypeService.remove(idValue).then((res) => {
        if (res.status === 200) {
            alert("Mark Type successfully deleted");
            window.location.reload();
        } else {
            Promise.reject();
        }
    })
    .catch((err) => {
        alert("Something went wrong");
        console.log(err);
    });
};

const ListMarkLevel = () =>{
    navigate(`/marktypes/${idValue}/marklevel`);
}

    return (
        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
                <div className="fw-bold">{name}</div>
            </div>
            <ButtonGroup aria-label="actions">
                <Button onClick={ListMarkLevel} variant="outline-primary">
                    <i className="bi bi-bar-chart-steps"> Levels</i>
                </Button>
                <Button variant="outline-primary">
                    <i className="bi bi-card-list"> Edit</i>
                </Button>
                <Button onClick={DeleteMarkType} variant="outline-danger">
                    <i className="bi bi-trash"> Remove</i>
                </Button>
            </ButtonGroup>
        </ListGroup.Item>
        );
    };

export default MarkTypeRow;