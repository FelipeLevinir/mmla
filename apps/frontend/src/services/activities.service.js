import http from "./http-common";

const getAll = (id) => {
  return http.get(`/experiment/${id}/activities`);
};

const get = (name) => {
  return http.get(`/activities/${name}`)
};

const getById = (id) => {
  return http.get(`/activitiesById/${id}`)
};

const getFile = (name) => {
    return http.get(`/activities/${name}`, {responseType: 'blob'});
};

const create = (id, data) => {
  return http.post(`/experiment/${id}/activities`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

const raname = (id, data) => {
  return http.put(`/activities/${id}`, data);
};

const remove = name => {
  return http.delete(`/activities/${name}`);
};

const ActivityService = {
  getAll,
  get,
  getFile,
  create,
  raname,
  remove,
  getById
};

export default ActivityService;