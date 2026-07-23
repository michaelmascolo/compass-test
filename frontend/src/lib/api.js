import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const createSession = async (payload) => {
  const { data } = await axios.post(`${API}/sessions`, payload);
  return data;
};

export const startPreview = async (opts) => {
  const { data } = await axios.post(`${API}/sessions/preview`, opts || {});
  return data;
};

export const previewContinue = async (id) => {
  const { data } = await axios.post(`${API}/sessions/${id}/preview-continue`);
  return data;
};

// --- Teacher Configuration + Constitution ---
export const getConstitution = async () => {
  const { data } = await axios.get(`${API}/compass/constitution`);
  return data;
};

export const createTeacherConfig = async (payload) => {
  const { data } = await axios.post(`${API}/teacher-configs`, payload);
  return data;
};

export const updateTeacherConfig = async (id, payload) => {
  const { data } = await axios.patch(`${API}/teacher-configs/${id}`, payload);
  return data;
};

export const validateConfiguration = async (id) => {
  const { data } = await axios.post(`${API}/teacher-configs/${id}/validate`);
  return data;
};

export const activateConfiguration = async (id) => {
  const { data } = await axios.post(`${API}/teacher-configs/${id}/activate`);
  return data;
};

export const getGradeProfile = async (id) => {
  const { data } = await axios.get(`${API}/grade-profiles/${id}`);
  return data;
};

export const createSessionFromConfig = async (id, studentName) => {
  const { data } = await axios.post(`${API}/teacher-configs/${id}/create-session`, {
    student_name: studentName || "",
  });
  return data;
};

// --- Teacher product: assignments (teacher -> assignment -> student sessions) ---
export const listTeacherAssignments = async () => {
  const { data } = await axios.get(`${API}/teacher/assignments`);
  return data;
};

export const listAssignmentSessions = async (configId) => {
  const { data } = await axios.get(`${API}/teacher/assignments/${configId}/sessions`);
  return data;
};

export const startAssignmentByCode = async (code, studentName) => {
  const { data } = await axios.post(`${API}/assignments/${code}/start`, {
    student_name: studentName || "",
  });
  return data;
};

export const validateRequest = async (request) => {
  const { data } = await axios.post(`${API}/compass/validate-request`, { request });
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

export const startTestRun = async (caseIds, label) => {
  const { data } = await axios.post(`${API}/tests/run`, {
    case_ids: caseIds && caseIds.length ? caseIds : null,
    label: label || null,
  });
  return data;
};

export const renameTestRun = async (runId, label) => {
  const { data } = await axios.patch(`${API}/tests/runs/${runId}/label`, { label });
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
