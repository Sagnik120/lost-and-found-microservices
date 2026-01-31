const ITEM_BASE_URL = "http://127.0.0.1:8001"; // replace with VM IP later

async function submitItem() {
  const user = JSON.parse(localStorage.getItem("user"));
  if (!user) {
    window.location.href = "login.html";
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const type = params.get("type");

  const item = {
    item_name: document.getElementById("item_name").value,
    description: document.getElementById("description").value,
    location: document.getElementById("location").value,
    user_id: user.user_id
  };

  const endpoint = type === "found" ? "found-item" : "lost-item";

  const res = await fetch(`${ITEM_BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item)
  });

  const data = await res.json();
  document.getElementById("msg").innerText = data.message || "Submitted";
}

async function loadMyItems() {
  const user = JSON.parse(localStorage.getItem("user"));
  if (!user) {
    window.location.href = "login.html";
    return;
  }

  const res = await fetch(`http://127.0.0.1:8001/items/user/${user.user_id}`);
  const items = await res.json();

  const table = document.getElementById("itemsTable");
  table.innerHTML = "";

  for (const item of items) {
    let actionBtn = "";
    let contactInfo = "-";

    if (item.status === "MATCHED") {
  actionBtn = `
    <button class="btn btn-sm btn-success"
      onclick="markReturned(${item.id})">
      Mark as Returned
    </button>
  `;

  const res = await fetch(`http://127.0.0.1:8000/user/${item.user_id}`);
  const userData = await res.json();

  contactInfo = `
    ${userData.name}<br>
    ${userData.email}
  `;
}


    table.innerHTML += `
      <tr>
        <td>${item.item_name}</td>
        <td>${item.location}</td>
        <td>${item.status}</td>
        <td>${new Date(item.created_at).toLocaleString()}</td>
        <td>${contactInfo}</td>
        <td>${actionBtn}</td>
      </tr>
    `;
  }
}


async function markReturned(itemId) {
  await fetch(`http://127.0.0.1:8001/items/${itemId}/returned`, {
    method: "PUT"
  });

  loadMyItems();
}

if (document.getElementById("itemsTable")) {
  loadMyItems();
}



async function markReturned(itemId) {
  await fetch(`http://127.0.0.1:8001/items/${itemId}/returned`, {
    method: "PUT"
  });

  loadMyItems(); // refresh table
}

