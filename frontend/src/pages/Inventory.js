import { useEffect, useState } from "react";
import API from "../services/api";

function Inventory() {
  const [medicines, setMedicines] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchMedicines = async () => {
    try {
      const response = await API.get("/inventory", {
        params: { search, status },
      });
      setMedicines(response.data);
    } catch {
      setError("Failed to load inventory.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMedicines();
  }, [search, status]);

  if (loading)
    return (
      <div className="container">
        <h3>Loading inventory...</h3>
      </div>
    );

  if (error)
    return (
      <div className="container">
        <h3 style={{ color: "red" }}>{error}</h3>
      </div>
    );

  return (
    <div className="container">
      <h1>Inventory</h1>

      {/* Search & Filter */}
      <div style={{ marginBottom: "20px", display: "flex", gap: "10px" }}>
        <input
          placeholder="Search by name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: "8px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            width: "250px",
          }}
        />

        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          style={{
            padding: "8px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
        >
          <option value="">All</option>
          <option value="Active">Active</option>
          <option value="Low Stock">Low Stock</option>
          <option value="Out of Stock">Out of Stock</option>
        </select>
      </div>

      {/* Styled Table */}
      <table
        style={{
          width: "100%",
          background: "white",
          borderRadius: "12px",
          overflow: "hidden",
          boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
          borderCollapse: "collapse",
        }}
      >
        <thead style={{ backgroundColor: "#f9fafb" }}>
          <tr>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Generic</th>
            <th style={thStyle}>Manufacturer</th>
            <th style={thStyle}>Qty</th>
            <th style={thStyle}>Price</th>
            <th style={thStyle}>Status</th>
          </tr>
        </thead>
        <tbody>
          {medicines.map((med) => (
            <tr key={med.id}>
              <td style={tdStyle}>{med.name}</td>
              <td style={tdStyle}>{med.generic_name}</td>
              <td style={tdStyle}>{med.manufacturer}</td>
              <td style={tdStyle}>{med.quantity}</td>
              <td style={tdStyle}>₹{med.price}</td>
              <td style={tdStyle}>
                <span
                  style={{
                    padding: "4px 10px",
                    borderRadius: "20px",
                    fontSize: "12px",
                    fontWeight: "500",
                    backgroundColor:
                      med.quantity < 10 ? "#fee2e2" : "#dcfce7",
                    color:
                      med.quantity < 10 ? "#b91c1c" : "#166534",
                  }}
                >
                  {med.quantity < 10 ? "Low Stock" : "Active"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* Table Styles */
const thStyle = {
  padding: "12px",
  textAlign: "left",
  fontWeight: "600",
  fontSize: "14px",
};

const tdStyle = {
  padding: "12px",
  borderTop: "1px solid #f1f5f9",
  fontSize: "14px",
};

export default Inventory;