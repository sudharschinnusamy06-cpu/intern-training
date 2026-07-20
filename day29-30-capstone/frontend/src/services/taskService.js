import api from "./api";

export const getTasks = async (projectId, params = {}) => {
  const response = await api.get(`/projects/${projectId}/tasks/`, { params });
  return response.data;
};

export const createTask = async (projectId, data) => {
  const response = await api.post(`/projects/${projectId}/tasks/`, data);
  return response.data;
};

export const updateTask = async (projectId, taskId, data) => {
  const response = await api.put(`/projects/${projectId}/tasks/${taskId}`, data);
  return response.data;
};

export const deleteTask = async (projectId, taskId) => {
  const response = await api.delete(`/projects/${projectId}/tasks/${taskId}`);
  return response.data;
};

export const getMyAssignedTasks = async (projects, userId) => {
  const results = await Promise.all(
    projects.map((p) => getTasks(p.id).catch(() => []))
  );
  const allTasks = results.flat();
  return allTasks.filter((t) => t.assigned_to === userId);
};