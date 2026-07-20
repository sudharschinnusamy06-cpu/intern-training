import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../services/authService";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(form);
      navigate("/login");
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map((d) => d.msg).join(", "));
      } else if (typeof detail === "string") {
        setError(detail);
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ backgroundColor: "#FDF6F0" }}>
      <div className="w-full max-w-sm bg-white rounded-xl shadow-sm p-8" style={{ border: "1px solid #F0E4DC" }}>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Create account</h1>
        <p className="text-sm text-gray-500 mb-6">Get started with your free account</p>

        {error && (
          <div className="mb-4 text-sm rounded-lg px-3 py-2" style={{ backgroundColor: "#FBEAE5", color: "#B5564A" }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none"
              style={{ borderColor: "#F0E4DC" }}
              onFocus={(e) => (e.target.style.borderColor = "#D98C77")}
              onBlur={(e) => (e.target.style.borderColor = "#F0E4DC")}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none"
              style={{ borderColor: "#F0E4DC" }}
              onFocus={(e) => (e.target.style.borderColor = "#D98C77")}
              onBlur={(e) => (e.target.style.borderColor = "#F0E4DC")}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none"
              style={{ borderColor: "#F0E4DC" }}
              onFocus={(e) => (e.target.style.borderColor = "#D98C77")}
              onBlur={(e) => (e.target.style.borderColor = "#F0E4DC")}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full text-white text-sm font-medium py-2.5 rounded-lg transition-colors disabled:opacity-50"
            style={{ backgroundColor: "#D98C77" }}
          >
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>

        <p className="text-sm text-gray-500 text-center mt-6">
          Already have an account?{" "}
          <Link to="/login" className="font-medium hover:underline" style={{ color: "#D98C77" }}>
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}