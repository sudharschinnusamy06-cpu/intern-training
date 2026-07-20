import { useEffect, useState } from "react";
import { Plus, X, Edit2, Trash2, Download } from "lucide-react";
import toast from "react-hot-toast";
import { getProjects, createProject, updateProject, deleteProject } from "../services/projectService";
import ConfirmModal from "../components/ConfirmModal";
import { exportToExcel } from "../utils/exportToExcel";

function StatusBadge({ status }) {
  const styles = {
    active: { backgroundColor: "#E8F0E3", color: "#7FA372" },
    completed: { backgroundColor: "#F3E8D9", color: "#C9A468" },
    on_hold: { backgroundColor: "#F5E9DC", color: "#D9A05B" },
  };
  return (
    <span className="text-xs px-2.5 py-1 rounded-full font-medium capitalize" style={styles[status] || { backgroundColor: "#F0EAE5", color: "#8A8580" }}>
      {status?.replace("_", " ")}
    </span>
  );
}

const inputStyle = { borderColor: "#F0E4DC" };
const focusHandlers = {
  onFocus: (e) => (e.target.style.borderColor = "#D98C77"),
  onBlur: (e) => (e.target.style.borderColor = "#F0E4DC"),
};

function ProjectModal({ project, onClose, onSaved }) {
  const isEdit = !!project;
  const [name, setName] = useState(project?.name || "");
  const [description, setDescription] = useState(project?.description || "");
  const [status, setStatus] = useState(project?.status || "active");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      if (isEdit) {
        await updateProject(project.id, { name, description, status });
      } else {
        await createProject({ name, description });
      }
      onSaved();
      onClose();
      toast.success(isEdit ? "Project updated!" : "Project created!");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save project");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{isEdit ? "Edit Project" : "Create Project"}</h2>
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
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Project Name</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3}
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle} {...focusHandlers} />
          </div>
          {isEdit && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
              <select value={status} onChange={(e) => setStatus(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none dark:bg-gray-700 dark:text-gray-100" style={inputStyle}>
                <option value="active">Active</option>
                <option value="on_hold">On Hold</option>
                <option value="completed">Completed</option>
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

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  const loadProjects = () => {
    setLoading(true);
    getProjects().then(setProjects).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const confirmDelete = async () => {
    try {
      await deleteProject(deletingId);
      loadProjects();
      toast.success("Project deleted!");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to delete project");
    } finally {
      setDeletingId(null);
    }
  };

  const handleExport = () => {
    const data = projects.map((p) => ({
      "Project Name": p.name,
      Description: p.description || "",
      Owner: p.owner_username || "",
      Status: p.status,
      "Created Date": new Date(p.created_at).toLocaleDateString(),
    }));
    exportToExcel(data, "projects", "Projects");
    toast.success("Exported to Excel!");
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Projects</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage all your projects</p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleExport}
            className="flex items-center gap-2 text-sm font-medium px-4 py-2.5 rounded-lg border" style={{ borderColor: "#F0E4DC", color: "#8A8580" }}>
            <Download size={16} /> Export
          </button>
          <button onClick={() => { setEditingProject(null); setShowModal(true); }}
            className="flex items-center gap-2 text-white text-sm font-medium px-4 py-2.5 rounded-lg" style={{ backgroundColor: "#D98C77" }}>
            <Plus size={16} /> Create Project
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl overflow-hidden border border-[#F0E4DC] dark:border-gray-700">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-[#FBF7F3] dark:bg-gray-900 border-b border-[#F0E4DC] dark:border-gray-700">
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Project Name</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Description</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Owner</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Status</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Created Date</th>
              <th className="text-left font-medium text-gray-500 dark:text-gray-400 px-5 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="px-5 py-6 text-center text-gray-400">Loading...</td></tr>
            ) : projects.length === 0 ? (
              <tr><td colSpan={6} className="px-5 py-6 text-center text-gray-400">No projects yet.</td></tr>
            ) : (
              projects.map((p, i) => (
                <tr key={p.id} style={{ borderTop: i === 0 ? "none" : "1px solid #F5EDE7" }} className="dark:border-gray-700">
                  <td className="px-5 py-3 font-medium text-gray-800 dark:text-gray-100">{p.name}</td>
                  <td className="px-5 py-3 text-gray-500 dark:text-gray-400">{p.description || "—"}</td>
                  <td className="px-5 py-3 text-gray-600 dark:text-gray-300">{p.owner_username || "—"}</td>
                  <td className="px-5 py-3"><StatusBadge status={p.status} /></td>
                  <td className="px-5 py-3 text-gray-500 dark:text-gray-400">{new Date(p.created_at).toLocaleDateString()}</td>
                  <td className="px-5 py-3">
                    <div className="flex items-center gap-2">
                      <button onClick={() => { setEditingProject(p); setShowModal(true); }} className="text-gray-400" onMouseEnter={(e) => (e.target.style.color = "#D98C77")} onMouseLeave={(e) => (e.target.style.color = "#9CA3AF")} title="Edit">
                        <Edit2 size={16} />
                      </button>
                      <button onClick={() => setDeletingId(p.id)} className="text-gray-400" onMouseEnter={(e) => (e.target.style.color = "#B5564A")} onMouseLeave={(e) => (e.target.style.color = "#9CA3AF")} title="Delete">
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
        <ProjectModal project={editingProject} onClose={() => setShowModal(false)} onSaved={loadProjects} />
      )}

      {deletingId && (
        <ConfirmModal
          title="Delete Project"
          message="Are you sure you want to delete this project? This action cannot be undone."
          onConfirm={confirmDelete}
          onCancel={() => setDeletingId(null)}
        />
      )}
    </div>
  );
}