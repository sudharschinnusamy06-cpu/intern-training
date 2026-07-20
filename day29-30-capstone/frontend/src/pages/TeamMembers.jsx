import { useEffect, useState } from "react";
import { Plus, X } from "lucide-react";
import toast from "react-hot-toast";
import { getUsers, updateUserRole } from "../services/userService";
import { register } from "../services/authService";
import { useAuth } from "../context/AuthContext";

const inputStyle = { borderColor: "#F0E4DC" };
const focusHandlers = {
  onFocus: (e) => (e.target.style.borderColor = "#D98C77"),
  onBlur: (e) => (e.target.style.borderColor = "#F0E4DC"),
};

function AddMemberModal({ onClose, onCreated }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      await register({ username, email, password });
      onCreated();
      onClose();
      toast.success("Member added!");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add member");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Add Team Member</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
            <X size={20} />
          </button>
        </div>

        {error && (
          <div className="mb-4 text-sm rounded-lg px-3 py-2" style={{ backgroundColor: "#FBEAE5", color: "#B5564A" }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Temporary Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">Cancel</button>
            <button type="submit" disabled={saving} className="px-4 py-2 text-sm font-medium text-white rounded-lg disabled:opacity-50" style={{ backgroundColor: "#D98C77" }}>
              {saving ? "Adding..." : "Add Member"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function TeamMembers() {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [savingId, setSavingId] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const loadUsers = () => {
    setLoading(true);
    getUsers().then(setUsers).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleRoleChange = async (userId, newRole) => {
    setSavingId(userId);
    try {
      await updateUserRole(userId, newRole);
      loadUsers();
      toast.success("Role updated!");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update role");
    } finally {
      setSavingId(null);
    }
  };

  const isAdmin = currentUser?.role === "admin";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Team Members</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Everyone with access to the system</p>
        </div>
        {isAdmin && (
          <button onClick={() => setShowModal(true)}
            className="flex items-center gap-2 text-white text-sm font-medium px-4 py-2.5 rounded-lg" style={{ backgroundColor: "#D98C77" }}>
            <Plus size={16} /> Add Team Member
          </button>
        )}
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl overflow-hidden border border-[#F0E4DC] dark:border-gray-700">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-[#FBF7F3] dark:bg-gray-900 border-b border-[#F0E4DC] dark:border-gray-700">
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Username</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Email</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Role</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Projects</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={4} className="px-5 py-6 text-center text-gray-400">Loading...</td></tr>
            ) : users.length === 0 ? (
              <tr><td colSpan={4} className="px-5 py-6 text-center text-gray-400">No users found.</td></tr>
            ) : (
              users.map((u, i) => (
                <tr key={u.id} style={{ borderTop: i === 0 ? "none" : "1px solid #F5EDE7" }} className="dark:border-gray-700">
                  <td className="px-5 py-3 font-medium text-gray-800 dark:text-gray-100">{u.username}</td>
                  <td className="px-5 py-3 text-gray-600 dark:text-gray-300">{u.email}</td>
                  <td className="px-5 py-3">
                    {isAdmin ? (
                      <select
                        value={u.role}
                        disabled={savingId === u.id}
                        onChange={(e) => handleRoleChange(u.id, e.target.value)}
                        className="text-xs px-2 py-1 rounded-lg border font-medium capitalize dark:bg-gray-700"
                        style={{ borderColor: "#F0E4DC", backgroundColor: "#FBEAE5", color: "#D98C77" }}
                      >
                        <option value="user">User</option>
                        <option value="manager">Manager</option>
                        <option value="admin">Admin</option>
                      </select>
                    ) : (
                      <span className="text-xs px-2.5 py-1 rounded-full font-medium capitalize" style={{ backgroundColor: "#FBEAE5", color: "#D98C77" }}>
                        {u.role}
                      </span>
                    )}
                  </td>
                  <td className="px-5 py-3 text-gray-600 dark:text-gray-300">{u.project_count}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <AddMemberModal onClose={() => setShowModal(false)} onCreated={loadUsers} />
      )}
    </div>
  );
}