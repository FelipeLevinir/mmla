import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Alert from "react-bootstrap/Alert";
import FormGroup from "react-bootstrap/FormGroup";
import Form from "react-bootstrap/Form";
import Spinner from "react-bootstrap/Spinner";
import MarkLevelService from "../../services/marklevels.service";


export default function CreateMarkLevel() {
    const [name, setName] = useState("");
    const [value, setValue] = useState("");
    const { id_marktype } = useParams();
    const [alert, setAlert] = useState({
      message: "",
      variant: "primary",
      show: false,
    });
    const [spinner, setSpinner] = useState(true);
    const navigate = useNavigate();
  
    const handleName = (event) => {
      setName(event.target.value);
    };
    const handleValue = (event) => {
      setValue(event.target.value);
    };
  
    const MarkLevelList = () => {
      navigate(`/marktypes/${id_marktype}/marklevel`);
    };
  
    const upload = (event) => {
      event.preventDefault();
    
      if (!name) {
        setAlert({
          variant: "danger",
          show: true,
          message: "Please enter a name.",
        });
        return;
      }
    
      setSpinner(false);
      let formData = new FormData();
      formData.append("name", name);
      formData.append("value", value);
      MarkLevelService.create(id_marktype, formData)
        .then((result) => {
          setAlert({
            variant: "success",
            show: true,
            message: result.data.message,
          });
          setSpinner(true);
          setName("");
          setValue("");
        })
        .catch((error) => {
          console.log(error);
          setAlert({
            variant: "danger",
            show: true,
            message: error.response.data.error,
          });
          setSpinner(true);
          setName("");
          setValue("");
        });
    };
  
    return (
      <Container fluid="md text-start">
        <Row className="p-2">
          <Col>
            <Card>
              <Card.Header>New Mark Level</Card.Header>
              <Card.Body>
                <Card.Title>Create level type:</Card.Title>
                <ButtonGroup aria-label="Basic example">
                  <Button
                    className="my-2"
                    onClick={MarkLevelList}
                    variant="outline-primary"
                  >
                    <i className="bi bi-folder-plus"> Mark Level list</i>
                  </Button>
                </ButtonGroup>
                <Alert variant={alert.variant} show={alert.show}>
                  {alert.message}
                </Alert>
                <div className="form-wrapper">
                  <form>
                    <FormGroup className="p-2">
                      <Form.Control
                        type="text"
                        value={name}
                        onChange={handleName}
                        placeholder="Name*"
                      />
                    </FormGroup>
                    <FormGroup className="p-2">
                      <Form.Control
                        type="text"
                        value={value}
                        onChange={handleValue}
                        placeholder="Value"
                      />
                    </FormGroup>
                    <FormGroup className="p-2">
                      <Button
                        variant="primary"
                        onClick={upload}
                        disabled={!spinner}
                      >
                        Save
                      </Button>
                    </FormGroup>
                    {!spinner && (
                      <FormGroup className="p-2">
                        <Spinner
                          animation="border"
                          role="status"
                          variant="primary"
                        >
                          <span className="visually-hidden">Loading...</span>
                        </Spinner>
                      </FormGroup>
                    )}
                  </form>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    );
  }
  