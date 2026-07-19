import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const createSession = async (payload) => {
  const { data } = await axios.post(`${API}/sessions`, payload);
  return data;
};

export const getSession = async (id) => {
  const { data } = await axios.get(`${API}/sessions/${id}`);
  return data;
};

export const interact = async (id, payload) => {
  const { data } = await axios.post(`${API}/sessions/${id}/interact`, payload);
  return data;
};

export const editTelos = async (id, payload) => {
  const { data } = await axios.patch(`${API}/sessions/${id}/telos`, payload);
  return data;
};
