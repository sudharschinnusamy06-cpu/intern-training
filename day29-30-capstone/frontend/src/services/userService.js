import api from "./api";

export const getUsers = async () => {
  const response = await api.get("/users/");
  return response.data;
};

export const updateProfile = async (data) => {
  const response = await api.put("/users/me", data);
  return response.data;
};

export const changePassword = async (data) => {
  const response = await api.put("/users/me/password", data);
  return response.data;
};

export const updateUserRole = async (userId, role) => {
  const response = await api.put(`/users/${userId}/role?role=${role}`);
  return response.data;
};