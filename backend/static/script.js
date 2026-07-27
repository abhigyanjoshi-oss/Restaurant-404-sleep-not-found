// ================= STATE =================
// The table the current visitor has reserved. Previously "orderItem"
// hard-coded table_no to 1 for every visitor, which meant everyone's
// orders were logged against Table 1 regardless of which table they
// actually booked.
let currentTableNo = null;

// ================= TABLES =================

// Load all tables dynamically from DB
async function loadTables() {
    try {
        const response = await fetch("/tables");
        const tables = await response.json();
        const container = document.querySelector(".table-container");
        container.innerHTML = "";

        tables.forEach(t => {
            const card = document.createElement("div");
            card.className = `table-card ${t.status}`;
            card.innerHTML = `
                <h3>Table ${t.table_no}</h3>
                <p class="status">
                    ${t.status === "unreserved" ? "🟢 Available" : "🟡 Reserved"}
                </p>
                <button>
                    ${t.status === "unreserved" ? "Book Now" : "Join Waiting List"}
                </button>
            `;

            const btn = card.querySelector("button");
            if (t.status === "unreserved") {
                btn.onclick = () => openBookingForm(t.table_no);
            } else {
                btn.onclick = () => alert(`Table ${t.table_no} is reserved. You joined waiting list.`);
            }

            container.appendChild(card);
        });
    } catch (err) {
        console.error("Error loading tables:", err);
    }
}

// ================= RESERVATIONS =================

// Open booking form with selected table number
function openBookingForm(tableNo) {
    const form = document.querySelector(".booking-form form");
    if (form) {
        form.dataset.tableNo = tableNo;
        document.getElementById("booking").scrollIntoView({ behavior: "smooth" });
    }
}

// Reserve a table
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".booking-form form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            if (!form.dataset.tableNo) {
                alert("Please pick a table from the Live Table Availability section first.");
                return;
            }

            const data = {
                table_no: Number(form.dataset.tableNo),
                name: e.target[0].value,
                email: e.target[1].value,
                phone_no: e.target[2].value,
                time: e.target[3].value
            };

            try {
                const response = await fetch("/reserve", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                alert(result.message || result.error);

                if (result.message) {
                    currentTableNo = data.table_no;
                }

                form.reset();
                form.dataset.tableNo = "";
                loadTables();
            } catch (err) {
                console.error("Error reserving table:", err);
            }
        });
    }
});

// ================= MENU =================

// Load menu items dynamically from DB
async function loadMenu() {
    try {
        const response = await fetch("/menu");
        const menu = await response.json();
        const container = document.querySelector(".menu-container");
        container.innerHTML = "";

        if (menu.length === 0) {
            container.innerHTML = "<p>No menu items available right now.</p>";
            return;
        }

        menu.forEach(item => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <img src="/static/images/${item.item.toLowerCase().replace(/ /g, '')}.jpg" alt="${item.item}"
                     onerror="this.style.display='none'">
                <h3>${item.item}</h3>
                <p class="description">Delicious ${item.item} prepared fresh.</p>
                <h4>₹${item.price}</h4>
                <p>${item.remaining > 0 ? `Remaining: ${item.remaining}` : "Sold out"}</p>
                <button ${item.remaining > 0 ? "" : "disabled"}>Order</button>
            `;

            const btn = card.querySelector("button");
            btn.onclick = () => orderItem(item.item);

            container.appendChild(card);
        });
    } catch (err) {
        console.error("Error loading menu:", err);
    }
}

// Place an order for whichever table the visitor has reserved
async function orderItem(itemName) {
    if (!currentTableNo) {
        alert("Please reserve a table before ordering.");
        return;
    }

    try {
        const response = await fetch("/order", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({table_no: currentTableNo, item_name: itemName})
        });
        const result = await response.json();
        alert(result.message || result.error);
        loadMenu();
    } catch (err) {
        console.error("Error placing order:", err);
    }
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", () => {
    loadTables();
    loadMenu();
});