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

// --- Developer-only Automated Instructional Testing ---
export const listTestCases = async () => {
  const { data } = await axios.get(`${API}/tests/cases`);
  return data.cases || [];
};

export const startTestRun = async (caseIds) => {
  const { data } = await axios.post(`${API}/tests/run`, {
    case_ids: caseIds && caseIds.length ? caseIds : null,
  });
  return data;
};

export const getTestRun = async (runId) => {
  const { data } = await axios.get(`${API}/tests/runs/${runId}`);
  return data;
};

export const listTestRuns = async () => {
  const { data } = await axios.get(`${API}/tests/runs`);
  return data.runs || [];
};

export const exportTestRunUrl = (runId, format) =>
  `${API}/tests/runs/${runId}/export?format=${format}`;
