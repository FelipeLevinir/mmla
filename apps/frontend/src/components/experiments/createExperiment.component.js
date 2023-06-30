import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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
import ExperimentService from "../../services/experiments.service";

export default function CreateExperiment() {
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [description, setDescription] = useState("");
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

  const handleCode = (event) => {
    setCode(event.target.value);
  };

  const handleDescription = (event) => {
    setDescription(event.target.value);
  };

  const experimentsList = () => {
    navigate("/experiments");
  };

  const upload = (event) => {
    event.preventDefault();

    if (!name || !code) {
      setAlert({
        variant: "danger",
        show: true,
        message: "Please enter a name and code.",
      });
      return;
    }

    setSpinner(false);
    let formData = new FormData();
    formData.append("name", name);
    formData.append("code", code);
    formData.append("description", description);

    ExperimentService.create(formData)
      .then((result) => {
        setAlert({
          variant: "success",
          show: true,
          message: result.data.message,
        });
        setSpinner(true);
        setName("");
        setCode("");
        setDescription("");
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
        setCode("");
        setDescription("");
      });
  };

  return (
    <Container fluid="md text-start">
      <Row className="p-2">
        <Col>
          <Card>
            <Card.Header>New experiments</Card.Header>
            <Card.Body>
              <Card.Title>Create new experiments:</Card.Title>
              <ButtonGroup aria-label="Basic example">
                <Button
                  className="my-2"
                  onClick={experimentsList}
                  variant="outline-primary"
                >
                  <i className="bi bi-folder-plus"> Experiments list</i>
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
                      value={code}
                      onChange={handleCode}
                      placeholder="Code*"
                    />
                  </FormGroup>
                  <FormGroup className="p-2">
                    <Form.Control
                      type="text"
                      value={description}
                      onChange={handleDescription}
                      placeholder="Detail"
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
