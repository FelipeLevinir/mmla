import http from "./http-common";

const getAll = (id) => {
    return http.get(`/marktype/${id}/marklevel`);
  };

const get = (id) => {
    return http.get(`/marklevel/${id}`);
  };

const create = (id, data) => {
  return http.post(`/marktype/${id}/marklevel`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

const remove = (id) => {
  return http.delete(`/marklevel/${id}`)
}

const MarkLevelService = {
    getAll,
    get,
    create,
    remove
};

export default MarkLevelService;