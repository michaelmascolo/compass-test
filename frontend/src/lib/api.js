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
  const res = await fetch(`${API}/sessions/${id}/interact`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok || !res.body) {
    let detail = "The developmental engine could not respond.";
    try {
      const j = await res.json();
      detail = j.detail || detail;
    } catch (_) {}
    const err = new Error(detail);
    err.detail = detail;
    throw err;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let result = null;
  let errorDetail = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let sep;
    while ((sep = buffer.indexOf("\n\n")) !== -1) {
      const rawEvent = buffer.slice(0, sep);
      buffer = buffer.slice(sep + 2);

      let eventName = "message";
      let data = "";
      for (const line of rawEvent.split("\n")) {
        if (line.startsWith(":")) continue; // heartbeat comment
        if (line.startsWith("event:")) eventName = line.slice(6).trim();
        else if (line.startsWith("data:")) data += line.slice(5).trim();
      }
      if (eventName === "done" && data) result = JSON.parse(data);
      else if (eventName === "error" && data) errorDetail = JSON.parse(data).detail;
    }
  }

  if (errorDetail) {
    const err = new Error(errorDetail);
    err.detail = errorDetail;
    throw err;
  }
  if (!result) throw new Error("No response from the developmental engine.");
  return result;
};

export const editTelos = async (id, payload) => {
  const { data } = await axios.patch(`${API}/sessions/${id}/telos`, payload);
  return data;
};
