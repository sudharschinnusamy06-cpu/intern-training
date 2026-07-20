import { useEffect, useState } from "react";
import { FolderKanban, ListTodo, CheckCircle2, Clock } from "lucide-react";
import { getDashboardStats } from "../services/dashboardService";
import { getProjects } from "../services/projectService";

function StatCard({ label, value, icon: Icon, bg, iconColor }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 border border-[#F0E4DC] dark:border-gray-700">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-500 dark:text-gray-400">{label}</span>
        <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: bg }}>
          <Icon size={18} style={{ color: iconColor }} />
        </div>
      </div>
      <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getDashboardStats(), getProjects()])
      .then(([statsData, projectsData]) => {
        setStats(statsData);
        setProjects(projectsData);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-gray-500 dark:text-gray-400 text-sm">Loading dashboard...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Dashboard</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Overview of your projects and tasks</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Projects" value={stats?.total_projects ?? 0} icon={FolderKanban} bg="#FBEAE5" iconColor="#D98C77" />
        <StatCard label="Total Tasks" value={stats?.total_tasks ?? 0} icon={ListTodo} bg="#F3E8D9" iconColor="#C9A468" />
        <StatCard label="Completed Tasks" value={stats?.completed_tasks ?? 0} icon={CheckCircle2} bg="#E8F0E3" iconColor="#7FA372" />
        <StatCard label="Pending Tasks" value={stats?.pending_tasks ?? 0} icon={Clock} bg="#F5E9DC" iconColor="#D9A05B" />
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-[#F0E4DC] dark:border-gray-700">
        <div className="px-5 py-4 border-b border-[#F5EDE7] dark:border-gray-700">
          <h2 className="font-semibold text-gray-800 dark:text-gray-100">Recent Projects</h2>
        </div>
        <div>
          {projects.length === 0 ? (
            <p className="px-5 py-6 text-sm text-gray-400 dark:text-gray-500">No projects yet.</p>
          ) : (
            projects.slice(0, 5).map((p, i) => (
              <div
                key={p.id}
                className="px-5 py-3 flex items-center justify-between"
                style={{ borderTop: i === 0 ? "none" : "1px solid #F5EDE7" }}
              >
                <div>
                  <p className="text-sm font-medium text-gray-800 dark:text-gray-100">{p.name}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{p.description || "No description"}</p>
                </div>
                <span className="text-xs px-2.5 py-1 rounded-full font-medium" style={{ backgroundColor: "#E8F0E3", color: "#7FA372" }}>
                  {p.status}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}