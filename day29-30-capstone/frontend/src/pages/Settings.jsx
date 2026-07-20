import { Sun, Moon, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";

export default function Settings() {
  const { logoutUser } = useAuth();
  const { darkMode, toggleDarkMode } = useTheme();

  return (
    <div className="space-y-6 max-w-xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Settings</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage your preferences</p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 space-y-4 border border-[#F0E4DC] dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {darkMode ? <Moon size={18} className="text-gray-300" /> : <Sun size={18} style={{ color: "#D9A05B" }} />}
            <div>
              <p className="text-sm font-medium text-gray-800 dark:text-gray-100">Theme</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">{darkMode ? "Dark Mode" : "Light Mode"}</p>
            </div>
          </div>
          <button
            onClick={toggleDarkMode}
            className="relative w-11 h-6 rounded-full transition-colors"
            style={{ backgroundColor: darkMode ? "#D98C77" : "#E5DDD5" }}
          >
            <span
              className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform"
              style={{ transform: darkMode ? "translateX(20px)" : "translateX(0)" }}
            />
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-[#F0E4DC] dark:border-gray-700">
        <button
          onClick={logoutUser}
          className="flex items-center gap-2 text-sm font-medium px-4 py-2.5 rounded-lg"
          style={{ color: "#B5564A" }}
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </div>
  );
}