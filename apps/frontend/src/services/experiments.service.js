import http from "./http-common";

const getAll = () => {
    return http.get("/experiments");
  };

const get = (code) => {
    return http.get(`/experiment/${code}`);
}

const get_by_id = (id) => {
  return http.get(`/experimentID/${id}`);
}

const create = (data) => {
    return http.post("/experiments", data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  };

const remove = code => {
  return http.delete(`/experiment/${code}`);
};


  const ExperimentService = {
    getAll,
    get,
    create,
    remove,
    get_by_id
  };

  export default ExperimentService;