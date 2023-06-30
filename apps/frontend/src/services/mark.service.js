import http from "./http-common";

const getAll = (experiment_id,event_id) => {
    return http.get(`/get_marks/${experiment_id}/${event_id}`);
  };

const create = (experiment_id,event_id, data) => {
  return http.post(`/create_mark/${experiment_id}/${event_id}`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};


const MarkService = {
    getAll,
    create
};

export default MarkService;