import { useState, useEffect } from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { LayoutDashboard, FolderKanban, ListTodo, Users, User, Settings as SettingsIcon, LogOut, Bell, Menu, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { getProjects } from "../services/projectService";
import { getMyAssignedTasks } from "../services/taskService";

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/tasks", label: "Tasks", icon: ListTodo },
  { to: "/team", label: "Team Members", icon: Users },
  { to: "/profile", label: "Profile", icon: User },
  { to: "/settings", label: "Settings", icon: SettingsIcon },
];

export default function DashboardLayout() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [assignedTasks, setAssignedTasks] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!user) return;
    getProjects().then((projects) => {
      getMyAssignedTasks(projects, user.id).then(setAssignedTasks);
    });
  }, [user]);

  return (
    <div className="flex min-h-screen bg-[#FDF6F0] dark:bg-gray-900">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/30 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 flex flex-col border-r border-[#F0E4DC] dark:border-gray-700 transition-transform duration-200 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        }`}
      >
        <div className="h-16 flex items-center justify-between px-6 font-bold text-lg text-[#D98C77]">
          ProjectMgr
          <button className="md:hidden text-gray-400" onClick={() => setSidebarOpen(false)}>
            <X size={20} />
          </button>
        </div>
        <nav className="flex-1 px-3 space-y-1">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-[#FBEAE5] text-[#B5564A] dark:bg-gray-700 dark:text-[#E8A48F]"
                    : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-3 border-t border-[#F0E4DC] dark:border-gray-700">
          <button
            onClick={logoutUser}
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-[#B5564A] hover:bg-[#FBEAE5] dark:hover:bg-gray-700 w-full"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className="h-16 bg-white dark:bg-gray-800 border-b border-[#F0E4DC] dark:border-gray-700 flex items-center justify-between px-4 md:px-6 relative">
          <div className="flex items-center gap-3">
            <button className="md:hidden text-gray-500 dark:text-gray-300" onClick={() => setSidebarOpen(true)}>
              <Menu size={22} />
            </button>
            <span className="font-semibold text-gray-800 dark:text-gray-100 text-sm md:text-base">Employee/Project Management</span>
          </div>
          <div className="flex items-center gap-4">
            {/* Notification bell */}
            <div className="relative">
              <button onClick={() => { setShowNotifications((v) => !v); setShowProfileMenu(false); }} className="relative">
                <Bell size={20} className="text-gray-400 dark:text-gray-300" />
                {assignedTasks.length > 0 && (
                  <span
                    className="absolute -top-1 -right-1 w-4 h-4 rounded-full text-white text-[10px] flex items-center justify-center font-semibold"
                    style={{ backgroundColor: "#B5564A" }}
                  >
                    {assignedTasks.length}
                  </span>
                )}
              </button>
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-[#F0E4DC] dark:border-gray-700 z-50 max-h-72 overflow-y-auto">
                  <div className="px-4 py-3 border-b border-[#F0E4DC] dark:border-gray-700 text-sm font-medium text-gray-700 dark:text-gray-200">
                    My Open Tasks
                  </div>
                  {assignedTasks.length === 0 ? (
                    <p className="px-4 py-4 text-sm text-gray-500 dark:text-gray-400">You have no open tasks right now.</p>
                  ) : (
                    assignedTasks.map((t) => (
                      <div key={t.id} className="px-4 py-3 border-b border-[#F5EDE7] dark:border-gray-700 last:border-0">
                        <p className="text-sm font-medium text-gray-800 dark:text-gray-100">{t.title}</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">Status: {t.status.replace("_", " ")}</p>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>

            {/* Profile dropdown */}
            <div className="relative">
              <button
                onClick={() => { setShowProfileMenu((v) => !v); setShowNotifications(false); }}
                className="flex items-center gap-2"
              >
                <div className="w-8 h-8 rounded-full bg-[#D98C77] text-white flex items-center justify-center text-sm font-semibold">
                  {user?.username?.[0]?.toUpperCase() || "U"}
                </div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-200 hidden sm:inline">{user?.username}</span>
              </button>
              {showProfileMenu && (
                <div className="absolute right-0 mt-2 w-44 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-[#F0E4DC] dark:border-gray-700 py-1 z-50">
                  <button
                    onClick={() => { setShowProfileMenu(false); navigate("/profile"); }}
                    className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-[#FBF7F3] dark:hover:bg-gray-700"
                  >
                    View Profile
                  </button>
                  <button
                    onClick={logoutUser}
                    className="w-full text-left px-4 py-2 text-sm text-[#B5564A] hover:bg-[#FBEAE5] dark:hover:bg-gray-700"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-4 md:p-6 overflow-x-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}