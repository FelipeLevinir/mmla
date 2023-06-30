import { Button, Modal } from 'react-bootstrap';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';

const animatedComponents = makeAnimated();

const CreateMarkModal = ({
  show,
  onHide,
  markOptions,
  handleCreateMark,
  setComment,
  setTimeInVideo,
  setSelectedMarkOptions
}
) => {
  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Create Mark</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <form>
          <div className="form-group">
            <label htmlFor="comment">Comment</label>
            <input
              type="text"
              className="form-control"
              id="comment"
              onChange={(e) => setComment(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="timeInVideo">Time in Video</label>
            <input
              type="number"
              className="form-control"
              id="timeInVideo"
              onChange={(e) => setTimeInVideo(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="markTypeAndLevel">Mark Type and Level</label>
            <Select
              components={animatedComponents}
              isMulti
              options={markOptions}
              className="basic-multi-select"
              classNamePrefix="select"
              onChange={setSelectedMarkOptions}
            />
          </div>
        </form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
        <Button variant="primary" onClick={handleCreateMark}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
export default CreateMarkModal;