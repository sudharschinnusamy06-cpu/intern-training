import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { updateProfile, changePassword } from "../services/userService";

const inputStyle = { borderColor: "#F0E4DC" };
const focusHandlers = {
  onFocus: (e) => (e.target.style.borderColor = "#D98C77"),
  onBlur: (e) => (e.target.style.borderColor = "#F0E4DC"),
};

export default function Profile() {
  const { user } = useAuth();
  const [email, setEmail] = useState(user?.email || "");
  const [profileMsg, setProfileMsg] = useState("");

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [passwordMsg, setPasswordMsg] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setProfileMsg("");
    try {
      await updateProfile({ email });
      setProfileMsg("Profile updated successfully.");
    } catch (err) {
      setProfileMsg(err.response?.data?.detail || "Update failed.");
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPasswordMsg("");
    setPasswordError("");
    try {
      await changePassword({ current_password: currentPassword, new_password: newPassword });
      setPasswordMsg("Password updated successfully.");
      setCurrentPassword("");
      setNewPassword("");
    } catch (err) {
      setPasswordError(err.response?.data?.detail || "Failed to update password.");
    }
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Profile</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage your account details</p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 space-y-4 border border-[#F0E4DC] dark:border-gray-700">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-500 dark:text-gray-400">Username</p>
            <p className="font-medium text-gray-800 dark:text-gray-100">{user?.username}</p>
          </div>
          <div>
            <p className="text-gray-500 dark:text-gray-400">Role</p>
            <p className="font-medium text-gray-800 dark:text-gray-100 capitalize">{user?.role}</p>
          </div>
          <div>
            <p className="text-gray-500 dark:text-gray-400">Account Created</p>
            <p className="font-medium text-gray-800 dark:text-gray-100">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "—"}
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-[#F0E4DC] dark:border-gray-700">
        <h2 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Update Profile</h2>
        {profileMsg && <p className="text-sm mb-3" style={{ color: "#D98C77" }}>{profileMsg}</p>}
        <form onSubmit={handleProfileUpdate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <button type="submit" className="px-4 py-2 text-sm font-medium text-white rounded-lg" style={{ backgroundColor: "#D98C77" }}>
            Save Changes
          </button>
        </form>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-[#F0E4DC] dark:border-gray-700">
        <h2 className="font-semibold text-gray-800 dark:text-gray-100 mb-4">Change Password</h2>
        {passwordMsg && <p className="text-sm mb-3" style={{ color: "#7FA372" }}>{passwordMsg}</p>}
        {passwordError && <p className="text-sm mb-3" style={{ color: "#B5564A" }}>{passwordError}</p>}
        <form onSubmit={handlePasswordChange} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Current Password</label>
            <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">New Password</label>
            <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <button type="submit" className="px-4 py-2 text-sm font-medium text-white rounded-lg" style={{ backgroundColor: "#D98C77" }}>
            Update Password
          </button>
        </form>
      </div>
    </div>
  );
}