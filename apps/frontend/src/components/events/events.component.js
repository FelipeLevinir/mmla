import React, { useState, useRef, useEffect } from 'react';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import { useParams } from 'react-router-dom';
import ReactPlayer from 'react-player';
import { v4 as uuidv4 } from 'uuid';
import { Container, Table, Button, Row, Col, Card, ButtonGroup, Modal } from 'react-bootstrap';
import ConfirmModal from './modals/ConfirmModale'
import CreateMarkModal from './modals/CreateMarkModal'
import VideoClip from '../videoClip/videoClip';
import ReactDOM from 'react-dom';
import EventService from '../../services/event.service';
import ActivityService from '../../services/activities.service';
import MarkService from '../../services/mark.service';
import MarkTypeService from '../../services/marktypes.service';
import MarkLevelService from '../../services/marklevels.service'

const VideoMarker = () => {
  const { id_activity } = useParams();
  const playerRef = useRef(null);
  const intervalRef = useRef(null);
  const [marks, setMarks] = useState([]);
  const [marking, setMarking] = useState(false);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [experimentId, setExperimentId] = useState("");
  const [markData, setMarkData] = useState({});
  const [currentEventId, setCurrentEventId] = useState(null);

  const [selectedMarkOptions, setSelectedMarkOptions] = useState([]);

  const [showCreateMarkModal, setShowCreateMarkModal] = useState(false);
  const [markOptions, setMarkOptions] = useState([]);

  const [comment, setComment] = useState("");
  const [timeInVideo, setTimeInVideo] = useState(null);

  const [showModal, setShowModal] = useState(false);
  const [currentInterval, setCurrentInterval] = useState({ start: null, end: null });
  const [clips, setClips] = useState([]);

  const fetchEvents = async () => {
    try {
      const response = await EventService.getAll(id_activity);
      setMarks(response.data);
    } catch (error) {
      console.error('Hubo un error al obtener los eventos:', error);
    }
  };

  useEffect(() => {
    ActivityService.getById(id_activity)
      .then(({ data }) => {
        setExperimentId(data.experiment.$oid);
      })
      .catch((error) => {
        console.log(error);
      });

    fetchEvents();
  }, [id_activity]);

  useEffect(() => {
    if (intervalRef.current !== null) {
      setCurrentInterval(intervalRef.current);
      setShowModal(true);
      intervalRef.current = null;
    }
  }, [marks]);

  const handleGetMarkTypeLevel = async (eventId) => {
    try {
        const response = await MarkTypeService.getAll(experimentId);
        const markTypeDataResponse = response.data;

        let tempMarkData = {};
        let options = [];

        for (let markTypeObj of markTypeDataResponse) {
            const markLevelIds = markTypeObj.marklevel;
            const markTypeName = markTypeObj.name;

            let markLevelNames = [];
            let markLevelValues = [];

            for (let obj of markLevelIds) {
                const id = obj.$oid;
                try {
                    const markLevelData = await MarkLevelService.get(id);
                    markLevelNames.push(markLevelData.data.name);
                    markLevelValues.push(markLevelData.data.value);
                    options.push({
                        label: `${markTypeName}: ${markLevelData.data.name}: `+` ${markLevelData.data.value}`,
                        value: id
                    });
                } catch (error) {
                    console.log('Error al obtener markLevelData:', error);
                }
            }

            tempMarkData[markTypeName] = markLevelNames;
        }

        setMarkData(tempMarkData);
        setMarkOptions(options);
        setShowCreateMarkModal(true);
    } catch (error) {
        console.log('Error en MarkTypeService:', error);
    }
    setCurrentEventId(eventId);
};
  
const handleCreateMark = async () => {
  const eventId = currentEventId;

  // Asegúrate de que selectedMarkOptions contenga los IDs correctos de mark_type
  const markTypeIds = selectedMarkOptions.map(option => option.value);
  console.log(markTypeIds);

  try {
    // Crear FormData para enviar los datos como x-www-form-urlencoded
    let formData = new FormData();
    formData.append('comment', comment);
    formData.append('time_in_video', timeInVideo);
    formData.append('mark_type', JSON.stringify(markTypeIds));
    //formData.append('mark_type',[markTypeIds]);

    // Añadir cada mark_type_id al formData
    // markTypeIds.forEach(markTypeId => formData.append('mark_type', markTypeId));

    // Llamar al servicio para crear la marca
    await MarkService.create(experimentId, eventId, formData);
    console.log('Marca creada exitosamente');
    setShowCreateMarkModal(false);
  } catch (error) {
    console.error('Hubo un error al crear la Marca:', error);
  }
};

  
  const showMarkData = () => {
    console.log("Mark Data: ", markData);
  };

  const handleConfirm = async () => {
    const data = new FormData();
    data.append('start_time', currentInterval.start);
    data.append('end_time', currentInterval.end);

    try {
      await EventService.create(id_activity, data);
      console.log('Intervalo creado exitosamente');

      fetchEvents();

      setShowModal(false);
    } catch (error) {
      console.error('Hubo un error al crear el intervalo:', error);
    }
  };

  const handleDeleteClip = (id) => {
    setMarks(marks.filter(mark => mark.id !== id));
    setClips(clips.filter(clip => clip.id !== id));
  };

  const handleCancel = () => {
    setMarks((prevMarks) =>
      prevMarks.filter(
        (mark) =>
          mark.start !== currentInterval.start || mark.end !== currentInterval.end
      )
    );
    setShowModal(false);
  };

  const handleStartMark = () => {
    const currentTime = playerRef.current.getCurrentTime();
    setMarks((prevMarks) => [...prevMarks, { id: uuidv4(), start: currentTime, end: null }]);
    setMarking(true);
  };

  const handleEndMark = () => {
    const currentTime = playerRef.current.getCurrentTime();
    setMarks((prevMarks) => {
      const newMarks = prevMarks.map((mark) =>
        mark.end === null ? { ...mark, end: currentTime } : mark
      );
      intervalRef.current = newMarks[newMarks.length - 1];
      return newMarks;
    });
    setMarking(false);
  };

  const secondsToMinutes = (seconds) => {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
  };

  const handleVideoSelect = (e) => {
    const file = e.target.files[0];
    const videoUrl = URL.createObjectURL(file);
    setSelectedVideo(videoUrl);
  };

  const handleViewClip = (start, end) => {
    if (end <= start) {
      alert('El tiempo de fin del clip debe ser mayor que el tiempo de inicio.');
      return;
    }
    const clipWindow = window.open('', '_blank');
    clipWindow.document.write('<!DOCTYPE html><html><head><title>Video Clip</title></head><body></body></html>');
    clipWindow.document.title = 'Video Clip';
    clipWindow.document.body.style.display = 'flex';
    clipWindow.document.body.style.justifyContent = 'center';
    clipWindow.document.body.style.alignItems = 'center';
    clipWindow.document.body.style.height = '100vh';
    clipWindow.document.body.style.margin = '0';

    const container = clipWindow.document.createElement('div');
    clipWindow.document.body.appendChild(container);

    ReactDOM.render(
      <React.StrictMode>
        <VideoClip videoUrl={selectedVideo} start={start} end={end} />
      </React.StrictMode>,
      container
    );
  };

  const handleVideoError = () => {
    alert('Hubo un error al cargar el archivo de video. Por favor, intenta de nuevo con un archivo diferente.');
  };

  const handleCloseCreateMarkModal = () => {
    setShowCreateMarkModal(false);
  };

  return (
    <Container fluid="md text-start">
      <Row className="p-2">
        <Col>
          <Card>
            <Card.Header>Activity</Card.Header>
            <Card.Body>
              <Card.Title>Activity to Analyze</Card.Title>
              <input type="file" accept="video/mp4" onChange={handleVideoSelect} onError={handleVideoError} />
              {selectedVideo && (
                <>
                  <ReactPlayer ref={playerRef} url={selectedVideo} controls />
                  <br />
                  <ButtonGroup aria-label="Basic example">
                    <Button
                      variant={`${marking ? 'secondary' : 'outline-primary'}`}
                      onClick={handleStartMark}
                      disabled={marking}
                    >
                      Mark start of interval
                    </Button>
                    <Button
                      variant={`${marking ? 'outline-primary' : 'secondary'}`}
                      onClick={handleEndMark}
                      disabled={!marking}
                    >
                      Mark end of interval
                    </Button>
                  </ButtonGroup>
                </>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="p-2">
        <Col>
          <Card>
            <Card.Header>Events</Card.Header>
            <Card.Body>
              <Card.Title>List of Selected Events</Card.Title>
              <Table>
                <thead>
                  <tr>
                    <th>Start</th>
                    <th>End</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {marks
                    .filter((mark) => mark.start !== null && mark.end !== null)
                    .map((mark) => (
                      <tr key={mark.id}>
                        <td>{secondsToMinutes(mark.start_time)}</td>
                        <td>{secondsToMinutes(mark.end_time)}</td>
                        <td>
                          <div>
                            <ButtonGroup aria-label="Basic example">
                              <Button onClick={() => handleViewClip(mark.start, mark.end)} variant="outline-primary">
                                Clip
                              </Button>
                              <Button onClick={() => handleGetMarkTypeLevel(mark._id.$oid)} variant="outline-primary">
                                Marks
                              </Button>
                              <Button variant="outline-primary">
                                Edit
                              </Button>
                              <Button variant="outline-primary" onClick={showMarkData}>
                                <i className="bi bi-eye"></i>
                              </Button>
                              <Button onClick={() => handleDeleteClip(mark.id)} variant="outline-danger">
                                Delete
                              </Button>
                            </ButtonGroup>
                          </div>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {showModal && (
        <ConfirmModal
          start={secondsToMinutes(currentInterval.start)}
          end={secondsToMinutes(currentInterval.end)}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}

      <CreateMarkModal
        show={showCreateMarkModal}
        onHide={handleCloseCreateMarkModal}
        markOptions={markOptions}
        handleCreateMark={handleCreateMark}
        setComment={setComment}
        setTimeInVideo={setTimeInVideo}
        setSelectedMarkOptions={setSelectedMarkOptions}
      />

    </Container>
  );
};

export default VideoMarker;