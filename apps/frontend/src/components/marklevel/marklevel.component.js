import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import MarkTypeRow from "./marklevelRow.component";
import MarkLevelService from "../../services/marklevels.service";
import MarkTypeService from "../../services/marktypes.service";

export default function MarktLevel() {
  const [marktlevel, setMarktlevel] = useState([]);
  const [experimentId, setExperimentId] = useState(null);
  const [marktypeName, setMarktypeName] = useState(null);
  const { id_marktype } = useParams();
  let navigate = useNavigate();

  useEffect(() => {
    MarkLevelService.getAll(id_marktype)
      .then(({ data }) => {
        //console.log(data)
        setMarktlevel(data);
      })
      .catch((error) => {
        console.log(error);
      });
      MarkTypeService.get(id_marktype)
      .then((response) => {
        const expId = response.data.experiment.$oid;
        const name = response.data.name;
        setExperimentId(expId);
        setMarktypeName(name);
      })
      .catch((error) => {
        console.log("Error fetching mark type details:", error);
      });
  }, []);

  const newMarkLevel = () => {
    navigate(`/marktypes/${id_marktype}/marklevel/create-marktype`);
  };

  const ReturnMarktypeList = () => {
    navigate(`/experiment/${experimentId}/marktypes`);
    // console.log(id_marktype);
    // console.log(experimentId);
  };

  const DataElements = () => {
    return marktlevel.map((res, i) => {
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
              <Card.Header>Levels of Types of Mark: <b>{marktypeName}</b> </Card.Header>
              <Card.Body>
                <Card.Title>Levels of types of Mark list:</Card.Title>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={newMarkLevel}
                    variant="outline-primary"
                  >
                    <i className="bi bi-folder-plus"> New Level of type mark</i>
                  </Button>
                </ButtonGroup>
                <ListGroup as="ol" numbered>
                  {DataElements()}
                </ListGroup>
              </Card.Body>
              <Card.Footer className="text-muted">
                  <Button
                    className="my-2"
                    onClick={ReturnMarktypeList}
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
