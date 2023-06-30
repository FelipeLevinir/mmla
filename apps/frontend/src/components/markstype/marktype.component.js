import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import MarkTypeRow from "./marktypesRow.component"
import MarkTypeService from "../../services/marktypes.service";
import ExperimentService from "../../services/experiments.service"


export default function MarkTypes() {
  const [marktypes, setMarktype] = useState([]);
  const [experimentName, setExperimentName] = useState("");
  const { id_experiment } = useParams();
  let navigate = useNavigate();

  useEffect(() => {
    MarkTypeService.getAll(id_experiment)
      .then(({ data }) => {
        //console.log(id_experiment)
        setMarktype(data);
      })
      .catch((error) => {
        console.log(error);
      });

      ExperimentService.get_by_id(id_experiment)
      .then(({ data }) => {
        setExperimentName(data.name);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [id_experiment]);

  const newMarkType = () => {
    navigate(`/experiment/${id_experiment}/marktypes/create-marktype`);
  };

  const returnExperimentList = () => {
    navigate("/experiments");
  };

  const DataElements = () => {
    return marktypes.map((res, i) => {
      //console.log(res)
      return <MarkTypeRow obj={res} key={i} />;
    });
  };

  return (
    <>
      <Container fluid="md text-start">
        <Row className="p-2">
          <Col>
            <Card>
              <Card.Header>Types of Marks of the Experiment: <b>{experimentName}</b> </Card.Header>
              <Card.Body>
                <Card.Title>Types of Marks list:</Card.Title>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={newMarkType}
                    variant="outline-primary"
                  >
                    <i className="bi bi-folder-plus"> New Types of Marks</i>
                  </Button>
                </ButtonGroup>
                <ListGroup as="ol" numbered>
                  {DataElements()}
                </ListGroup>
              </Card.Body>
              <Card.Footer className="text-muted">
                  <Button
                    className="my-2"
                    onClick={returnExperimentList}
                    variant="outline-primary"
                  >
                    <i className="bi bi-arrow-left-square"> Return</i>
                  </Button>
                </Card.Footer>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}
