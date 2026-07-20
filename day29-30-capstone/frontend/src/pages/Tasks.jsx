import { useEffect, useState } from "react";
import { Plus, X, Edit2, Trash2, Download } from "lucide-react";
import toast from "react-hot-toast";
import { getProjects } from "../services/projectService";
import { getTasks, createTask, updateTask, deleteTask } from "../services/taskService";
import { getUsers } from "../services/userService";
import ConfirmModal from "../components/ConfirmModal";
import { exportToExcel } from "../utils/exportToExcel";

function StatusBadge({ status }) {
  const styles = {
    todo: { backgroundColor: "#F0EAE5", color: "#8A8580" },
    in_progress: { backgroundColor: "#F5E9DC", color: "#D9A05B" },
    done: { backgroundColor: "#E8F0E3", color: "#7FA372" },
  };
  const labels = { todo: "Pending", in_progress: "In Progress", done: "Completed" };
  return (
    <span className="text-xs px-2.5 py-1 rounded-full font-medium" style={styles[status] || { backgroundColor: "#F0EAE5", color: "#8A8580" }}>
      {labels[status] || status}
    </span>
  );
}

function PriorityBadge({ priority }) {
  const styles = {
    low: { backgroundColor: "#F0EAE5", color: "#8A8580" },
    medium: { backgroundColor: "#F3E8D9", color: "#C9A468" },
    high: { backgroundColor: "#FBEAE5", color: "#B5564A" },
  };
  return (
    <span className="text-xs px-2.5 py-1 rounded-full font-medium capitalize" style={styles[priority] || { backgroundColor: "#F0EAE5", color: "#8A8580" }}>
      {priority}
    </span>
  );
}

const inputStyle = { borderColor: "#F0E4DC" };
const focusHandlers = {
  onFocus: (e) => (e.target.style.borderColor = "#D98C77"),
  onBlur: (e) => (e.target.style.borderColor = "#F0E4DC"),
};

function TaskModal({ projectId, task, users, onClose, onSaved }) {
  const isEdit = !!task;
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [priority, setPriority] = useState(task?.priority || "medium");
  const [status, setStatus] = useState(task?.status || "todo");
  const [assignedTo, setAssignedTo] = useState(task?.assigned_to || "");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      const payload = {
        title,
        description,
        priority,
        assigned_to: assignedTo ? Number(assignedTo) : null,
      };
      if (isEdit) {
        payload.status = status;
        await updateTask(projectId, task.id, payload);
      } else {
        await createTask(projectId, payload);
      }
      onSaved();
      onClose();
      toast.success(isEdit ? "Task updated!" : "Task created!");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save task");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{isEdit ? "Edit Task" : "Create Task"}</h2>
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
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Title</label>
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2}
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Assign To</label>
            <select value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle}>
              <option value="">Unassigned</option>
              {users.map((u) => (
                <option key={u.id} value={u.id}>{u.username}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Priority</label>
            <select value={priority} onChange={(e) => setPriority(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          {isEdit && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
              <select value={status} onChange={(e) => setStatus(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle}>
                <option value="todo">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="done">Completed</option>
              </select>
            </div>
          )}
          <div className="flex justify-end gap-2 pt-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">Cancel</button>
            <button type="submit" disabled={saving} className="px-4 py-2 text-sm font-medium text-white rounded-lg disabled:opacity-50" style={{ backgroundColor: "#D98C77" }}>
              {saving ? "Saving..." : isEdit ? "Save Changes" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function Tasks() {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    getProjects().then((data) => {
      setProjects(data);
      if (data.length > 0) setSelectedProjectId(data[0].id);
      else setLoading(false);
    });
    getUsers().then(setUsers);
  }, []);

  const loadTasks = () => {
    if (!selectedProjectId) return;
    setLoading(true);
    getTasks(selectedProjectId).then(setTasks).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadTasks();
  }, [selectedProjectId]);

  const confirmDelete = async () => {
    try {
      await deleteTask(selectedProjectId, deletingId);
      loadTasks();
      toast.success("Task deleted!");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to delete task");
    } finally {
      setDeletingId(null);
    }
  };

  const handleExport = () => {
    const data = tasks.map((t) => ({
      Title: t.title,
      Description: t.description || "",
      "Assigned User": t.assigned_username || "Unassigned",
      Status: t.status,
      Priority: t.priority,
    }));
    exportToExcel(data, "tasks", "Tasks");
    toast.success("Exported to Excel!");
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Tasks</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage tasks across your projects</p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleExport} disabled={tasks.length === 0}
            className="flex items-center gap-2 text-sm font-medium px-4 py-2.5 rounded-lg border disabled:opacity-50" style={{ borderColor: "#F0E4DC", color: "#8A8580" }}>
            <Download size={16} /> Export
          </button>
          <button onClick={() => { setEditingTask(null); setShowModal(true); }} disabled={!selectedProjectId}
            className="flex items-center gap-2 text-white text-sm font-medium px-4 py-2.5 rounded-lg disabled:opacity-50" style={{ backgroundColor: "#D98C77" }}>
            <Plus size={16} /> Create Task
          </button>
        </div>
      </div>

      {projects.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Project</label>
          <select value={selectedProjectId || ""} onChange={(e) => setSelectedProjectId(Number(e.target.value))}
            className="px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-800 dark:text-gray-100" style={{ borderColor: "#F0E4DC" }}>
            {projects.map((p) => (<option key={p.id} value={p.id}>{p.name}</option>))}
          </select>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 rounded-xl overflow-hidden border border-[#F0E4DC] dark:border-gray-700">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-[#FBF7F3] dark:bg-gray-900 border-b border-[#F0E4DC] dark:border-gray-700">
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Title</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Description</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Assigned User</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Status</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Priority</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {projects.length === 0 ? (
              <tr><td colSpan={6} className="px-5 py-6 text-center text-gray-400">Create a project first.</td></tr>
            ) : loading ? (
              <tr><td colSpan={6} className="px-5 py-6 text-center text-gray-400">Loading...</td></tr>
            ) : tasks.length === 0 ? (
              <tr><td colSpan={6} className="px-5 py-6 text-center text-gray-400">No tasks yet.</td></tr>
            ) : (
              tasks.map((t, i) => (
                <tr key={t.id} style={{ borderTop: i === 0 ? "none" : "1px solid #F5EDE7" }} className="dark:border-gray-700">
                  <td className="px-5 py-3 font-medium text-gray-800 dark:text-gray-100">{t.title}</td>
                  <td className="px-5 py-3 text-gray-500 dark:text-gray-400">{t.description || "—"}</td>
                  <td className="px-5 py-3 text-gray-600 dark:text-gray-300">{t.assigned_username || "Unassigned"}</td>
                  <td className="px-5 py-3"><StatusBadge status={t.status} /></td>
                  <td className="px-5 py-3"><PriorityBadge priority={t.priority} /></td>
                  <td className="px-5 py-3">
                    <div className="flex items-center gap-2">
                      <button onClick={() => { setEditingTask(t); setShowModal(true); }} className="text-gray-400" onMouseEnter={(e) => (e.target.style.color = "#D98C77")} onMouseLeave={(e) => (e.target.style.color = "#9CA3AF")} title="Edit">
                        <Edit2 size={16} />
                      </button>
                      <button onClick={() => setDeletingId(t.id)} className="text-gray-400" onMouseEnter={(e) => (e.target.style.color = "#B5564A")} onMouseLeave={(e) => (e.target.style.color = "#9CA3AF")} title="Delete">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <TaskModal projectId={selectedProjectId} task={editingTask} users={users} onClose={() => setShowModal(false)} onSaved={loadTasks} />
      )}

      {deletingId && (
        <ConfirmModal
          title="Delete Task"
          message="Are you sure you want to delete this task? This action cannot be undone."
          onConfirm={confirmDelete}
          onCancel={() => setDeletingId(null)}
        />
      )}
    </div>
  );
}