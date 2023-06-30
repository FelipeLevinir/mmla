import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import ExperimentService from "../../services/experiments.service"
import ExperimentRow from "./experimentsRow.component";

export default function Experiments() {
  const [experiments, setExperiments] = useState([]);
  let navigate = useNavigate();

  useEffect(() => {
    ExperimentService.getAll()
      .then(({ data }) => {
        //console.log(data)
        setExperiments(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const newExperiment = () => {
    navigate("/create-experiment/");
  };

  // const editExperiment = () => {
  //   navigate("/edit-experiment/");
  // };

  const DataElements = () => {
    return experiments.map((res, i) => {
      //console.log(res)
      return <ExperimentRow obj={res} key={i} />;
    });
  };
  return (
    <>
      <Container fluid="md text-start">
        <Row className="p-2">
          <Col>
            <Card>
              <Card.Header>Experiments</Card.Header>
              <Card.Body>
                <Card.Title>Experiments list:</Card.Title>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={newExperiment}
                    variant="outline-primary"
                  >
                    <i className="bi bi-folder-plus"> New Experiment</i>
                  </Button>
                </ButtonGroup>
                <ListGroup as="ol" numbered>
                  {DataElements()}
                </ListGroup>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}
