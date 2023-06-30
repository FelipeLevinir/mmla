import React, { useState } from "react";
import { Button } from "react-bootstrap";
import { useNavigate  } from "react-router-dom";
import ListGroup from 'react-bootstrap/ListGroup';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import MarkLevelService from "../../services/marklevels.service";

const MarkTypeRow = (props) => {
    const { name, value ,_id } = props.obj;
    const idValue = _id.$oid;
//console.log(_id);

const DeleteMarkLevel = () => {
    MarkLevelService.remove(idValue).then((res) => {
        if (res.status === 200) {
            alert("Mark Level successfully deleted");
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

    return (
        <ListGroup.Item as="li" className="d-flex justify-content-between align-items-start">
            <div className="ms-2 me-auto">
                <div className="fw-bold">{name}</div>
            </div>
            <div className="ms-2 me-auto">
                <div className="fw-bold">{value}</div>
            </div>
            <ButtonGroup aria-label="actions">
                <Button variant="outline-primary">
                    <i className="bi bi-card-list"> Edit</i>
                </Button>
                <Button onClick={DeleteMarkLevel} variant="outline-danger">
                    <i className="bi bi-trash"> Remove</i>
                </Button>
            </ButtonGroup>
        </ListGroup.Item>
        );
    };

export default MarkTypeRow;