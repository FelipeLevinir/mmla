import http from "./http-common";

const getAll = (id) => {
    return http.get(`/experiment/${id}/marktypes`);
  };

const get = (id) => {
    return http.get(`/marktype/${id}`);
  };

const create = (id, data) => {
  return http.post(`/experiment/${id}/marktype`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

const remove = (id) => {
  return http.delete(`/marktype/${id}`)
}

const MarkTypeService = {
    getAll,
    create,
    remove,
    get
};

export default MarkTypeService;