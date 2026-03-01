import { useEffect, useState } from "react";
import API from "../services/api";
import { Link } from "react-router-dom";

function Dashboard() {
  const [todaySales, setTodaySales] = useState(null);
  const [totalItems, setTotalItems] = useState(null);
  const [lowStock, setLowStock] = useState([]);
  const [recentSales, setRecentSales] = useState([]);
  const [purchaseSummary, setPurchaseSummary] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const today = await API.get("/dashboard/today-sales");
        const total = await API.get("/dashboard/total-items-sold");
        const low = await API.get("/dashboard/low-stock");
        const recent = await API.get("/dashboard/recent-sales");
        const purchase = await API.get("/dashboard/purchase-summary");

        setTodaySales(today.data);
        setTotalItems(total.data);
        setLowStock(low.data);
        setRecentSales(recent.data);
        setPurchaseSummary(purchase.data);
      } catch (err) {
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading)
    return (
      <div className="container">
        <h3>Loading dashboard...</h3>
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
      <h1>Dashboard</h1>

      <Link to="/inventory">Go to Inventory</Link>

      {/*  CARD GRID  */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        {[
          {
            title: "Today's Sales",
            content: (
              <>
                <p>Total: ₹{todaySales?.total || 0}</p>
                <p>Transactions: {todaySales?.transactions || 0}</p>
              </>
            ),
          },
          {
            title: "Total Items Sold",
            content: (
              <p>{totalItems?.total_items_sold || 0}</p>
            ),
          },
          {
            title: "Low Stock",
            content: <p>{lowStock?.length || 0} items</p>,
          },
          {
            title: "Purchase Summary",
            content: (
              <p>
                ₹{purchaseSummary?.total_purchase_amount || 0}
              </p>
            ),
          },
        ].map((card, index) => (
          <div
            key={index}
            style={{
              background: "white",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
              transition: "transform 0.2s ease",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.transform =
                "translateY(-5px)")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.transform =
                "translateY(0px)")
            }
          >
            <h3 style={{ marginBottom: "10px" }}>
              {card.title}
            </h3>
            {card.content}
          </div>
        ))}
      </div>

      {/*  RECENT SALES  */}
      <h2 style={{ marginTop: "40px" }}>
        Recent Sales
      </h2>

      {recentSales.length === 0 ? (
        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "12px",
            boxShadow:
              "0 4px 12px rgba(0,0,0,0.05)",
          }}
        >
          No recent sales
        </div>
      ) : (
        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "12px",
            boxShadow:
              "0 4px 12px rgba(0,0,0,0.05)",
          }}
        >
          {recentSales.map((sale, index) => (
            <div
              key={index}
              style={{ marginBottom: "10px" }}
            >
              Medicine ID: {sale.medicine_id} |
              Qty: {sale.quantity_sold} |
              ₹{sale.total_amount}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;