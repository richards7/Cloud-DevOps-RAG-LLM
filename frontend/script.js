/**
 * Cloud & DevOps RAG Assistant — chat frontend logic.
 * Talks to the FastAPI backend at API_BASE (/health, /chat).
 */

const API_BASE = window.API_BASE || "";

const messagesEl = document.getElementById("messages");
const emptyStateEl = document.getElementById("empty-state");
const inputEl = document.getElementById("query-input");
const sendBtn = document.getElementById("send-btn");
const apiStatusEl = document.getElementById("api-status");

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function addUserMessage(text) {
  if (emptyStateEl) emptyStateEl.remove();

  const msg = document.createElement("div");
  msg.className = "msg user";
  msg.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
  messagesEl.appendChild(msg);
  scrollToBottom();
}

function addTypingIndicator() {
  const msg = document.createElement("div");
  msg.className = "msg assistant";
  msg.id = "typing-msg";
  msg.innerHTML = `
    <div class="bubble">
      <div class="typing"><span></span><span></span><span></span></div>
    </div>`;
  messagesEl.appendChild(msg);
  scrollToBottom();
  return msg;
}

function addAssistantMessage({ answer, provider, sources, latency_ms }) {
  const typingMsg = document.getElementById("typing-msg");
  if (typingMsg) typingMsg.remove();

  const sourceChips = (sources || [])
    .map((s) => `<span class="source-chip">${escapeHtml(s.source)}</span>`)
    .join("");

  const msg = document.createElement("div");
  msg.className = "msg assistant";
  msg.innerHTML = `
    <div class="bubble">${escapeHtml(answer)}</div>
    <div class="msg-meta">
      <span class="tag provider">${escapeHtml(provider)}</span>
      <span class="tag">${latency_ms}ms</span>
    </div>
    ${sourceChips ? `<div class="sources">${sourceChips}</div>` : ""}
  `;
  messagesEl.appendChild(msg);
  scrollToBottom();
}

function addErrorMessage(text) {
  const typingMsg = document.getElementById("typing-msg");
  if (typingMsg) typingMsg.remove();

  const msg = document.createElement("div");
  msg.className = "msg assistant";
  msg.innerHTML = `
    <div class="bubble" style="border-color:#e8735d55;color:#e8b3a8;">
      ${escapeHtml(text)}
    </div>`;
  messagesEl.appendChild(msg);
  scrollToBottom();
}

async function sendQuery(query) {
  addUserMessage(query);
  addTypingIndicator();
  sendBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!res.ok) {
      throw new Error(`Server responded with ${res.status}`);
    }

    const data = await res.json();
    addAssistantMessage(data);
  } catch (err) {
    addErrorMessage(
      `Couldn't reach the assistant (${err.message}). Confirm the backend is running at ${API_BASE}.`
    );
  } finally {
    sendBtn.disabled = false;
  }
}

function handleSend() {
  const text = inputEl.value.trim();
  if (!text) return;
  inputEl.value = "";
  autoGrow();
  sendQuery(text);
}

function autoGrow() {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 140) + "px";
}

sendBtn.addEventListener("click", handleSend);

inputEl.addEventListener("input", autoGrow);

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});

document.querySelectorAll(".suggestion-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    sendQuery(chip.dataset.q);
  });
});

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) {
      apiStatusEl.textContent = "online";
      apiStatusEl.classList.add("status-ok");
    } else {
      throw new Error();
    }
  } catch {
    apiStatusEl.textContent = "offline";
    apiStatusEl.classList.remove("status-ok");
    apiStatusEl.style.color = "#e8735d";
  }
}

checkHealth();
