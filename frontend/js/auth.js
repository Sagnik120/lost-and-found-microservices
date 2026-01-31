console.log("auth.js loaded");

// expose functions to global scope
window.loginUser = async function () {
  console.log("Login button clicked");

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (!res.ok) {
    document.getElementById("msg").innerText = data.detail || "Login failed";
    return;
  }

  localStorage.setItem("user", JSON.stringify(data));
  window.location.href = "dashboard.html";
};

window.registerUser = async function () {
  console.log("Register button clicked");

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://127.0.0.1:8000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  });

  const data = await res.json();
  document.getElementById("msg").innerText = data.message || data.detail;
};

window.logoutUser = function () {
  localStorage.removeItem("user");
  window.location.href = "login.html";
};
