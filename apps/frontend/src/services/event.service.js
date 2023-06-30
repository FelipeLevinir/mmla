import http from "./http-common";

const getAll = (id_activity) => {
    return http.get(`/activities/${id_activity}/events`);
  };

  const get = (event_id) => {
    return http.get(`/event/${event_id}`);
  };

const create = (id, data) => {
  return http.post(`/activities/${id}/event`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

const remove = (id) => {
  return http.delete(`/event/${id}`)
}

const EventService = {
    getAll,
    get,
    create,
    remove
};

export default EventService;