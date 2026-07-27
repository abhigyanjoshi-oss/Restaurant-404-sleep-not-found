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
        alert(`Booking form opened for Table ${tableNo}`);
    }
}

// Reserve a table
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".booking-form form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const data = {
                table_no: form.dataset.tableNo || 1,
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

        menu.forEach(item => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <img src="/static/images/${item.item.toLowerCase().replace(/ /g, '')}.jpg" alt="${item.item}">
                <h3>${item.item}</h3>
                <p class="description">Delicious ${item.item} prepared fresh.</p>
                <h4>₹${item.price}</h4>
                <p>Remaining: ${item.remaining}</p>
                <button>Order</button>
            `;

            const btn = card.querySelector("button");
            btn.onclick = () => orderItem(1, item.item);

            container.appendChild(card);
        });
    } catch (err) {
        console.error("Error loading menu:", err);
    }
}

// Place an order
async function orderItem(tableNo, itemName) {
    try {
        const response = await fetch("/order", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({table_no: tableNo, item_name: itemName})
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
