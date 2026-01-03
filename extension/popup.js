const actionSelect = document.getElementById("action");
const selectorTypeSelect = document.getElementById("selectorType");
const matchRow = document.getElementById("matchRow");
const matchSelect = document.getElementById("matchMode");
const valueRow = document.getElementById("valueRow");
const fillValueInput = document.getElementById("fillValue");
const recordBtn = document.getElementById("recordBtn");
const statusBadge = document.getElementById("status");
const summary = document.getElementById("summary");
const selectorValue = document.getElementById("selectorValue");
const textValue = document.getElementById("textValue");
const copyJsonBtn = document.getElementById("copyJsonBtn");
const copyCliBtn = document.getElementById("copyCliBtn");
const output = document.getElementById("output");

let currentCapture = null;
let outputMode = "json";

function setStatus(text, variant) {
  statusBadge.textContent = text;
  statusBadge.className = `status status-${variant}`;
}

function updateVisibility() {
  const selectorType = selectorTypeSelect.value;
  matchRow.classList.toggle("hidden", selectorType !== "text");

  const action = actionSelect.value;
  valueRow.classList.toggle("hidden", action !== "fill");
}

function truncate(value, maxLength = 60) {
  if (!value) return "-";
  if (value.length <= maxLength) return value;
  return `${value.slice(0, maxLength)}...`;
}

function buildSummary(capture) {
  if (!capture || !capture.meta) return "No capture yet.";
  const meta = capture.meta;
  const tag = meta.tag || "element";
  const id = meta.id ? `#${meta.id}` : "";
  const classes = Array.isArray(meta.classes) && meta.classes.length
    ? `.${meta.classes.slice(0, 3).join(".")}`
    : "";
  return `${tag}${id}${classes}`;
}

function shellQuote(value) {
  const safe = String(value).replace(/\s+/g, " ").trim();
  if (safe.includes("'")) {
    return `"${safe.replace(/"/g, "\\\"")}"`;
  }
  return `'${safe}'`;
}

function buildStep() {
  if (!currentCapture) return null;
  const selectorType = selectorTypeSelect.value;
  const selector = currentCapture.selectors?.[selectorType];
  if (!selector) throw new Error(`No ${selectorType} selector captured.`);

  const action = currentCapture.action;
  const key = action === "wait" ? "wait_for" : action;
  const payload = { [selectorType]: selector };

  if (selectorType === "text") {
    payload.match = matchSelect.value;
  }

  if (action === "fill") {
    payload.value = fillValueInput.value || "YOUR_VALUE";
  }

  return { [key]: payload };
}

function buildCliLine() {
  if (!currentCapture) return "";
  const selectorType = selectorTypeSelect.value;
  const selector = currentCapture.selectors?.[selectorType];
  if (!selector) throw new Error(`No ${selectorType} selector captured.`);

  const action = currentCapture.action;
  const parts = [action, `${selectorType}=${shellQuote(selector)}`];

  if (selectorType === "text") {
    parts.push(`match=${matchSelect.value}`);
  }

  if (action === "fill") {
    const value = fillValueInput.value || "YOUR_VALUE";
    parts.push(`value=${shellQuote(value)}`);
  }

  return parts.join(" ");
}

function updateOutput() {
  if (!currentCapture) {
    output.value = "";
    return;
  }

  const step = buildStep();
  const jsonText = JSON.stringify(step, null, 2);
  const cliText = buildCliLine();

  output.value = outputMode === "cli" ? cliText : jsonText;
}

function updateCapture(capture) {
  currentCapture = capture;
  if (capture?.action) {
    actionSelect.value = capture.action;
  }

  summary.textContent = buildSummary(capture);
  selectorValue.textContent = truncate(capture?.selectors?.[selectorTypeSelect.value]);
  textValue.textContent = truncate(capture?.selectors?.text || "-");

  updateVisibility();
  updateOutput();
  setStatus("Captured", "captured");
}

function showError(message) {
  outputMode = "json";
  output.value = message;
  setStatus("Error", "armed");
}

function copyText(text, successLabel) {
  navigator.clipboard.writeText(text).then(() => {
    setStatus(successLabel, "captured");
  });
}

recordBtn.addEventListener("click", () => {
  updateVisibility();
  const action = actionSelect.value;

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    if (!tab?.id) {
      showError("No active tab found.");
      return;
    }

    chrome.tabs.sendMessage(
      tab.id,
      {
        type: "ac8-start-capture",
        action,
      },
      () => {
        if (chrome.runtime.lastError) {
          showError("Cannot capture on this page.");
          return;
        }

        chrome.storage.local.set({
          captureStatus: "armed",
          captureAction: action,
          captureStartedAt: Date.now(),
        });

        setStatus("Armed", "armed");
      }
    );
  });
});

copyJsonBtn.addEventListener("click", () => {
  try {
    outputMode = "json";
    updateOutput();
    copyText(output.value, "JSON copied");
  } catch (error) {
    showError(error.message);
  }
});

copyCliBtn.addEventListener("click", () => {
  try {
    outputMode = "cli";
    updateOutput();
    copyText(output.value, "CLI copied");
  } catch (error) {
    showError(error.message);
  }
});

selectorTypeSelect.addEventListener("change", () => {
  selectorValue.textContent = truncate(currentCapture?.selectors?.[selectorTypeSelect.value]);
  updateVisibility();
  updateOutput();
});

matchSelect.addEventListener("change", updateOutput);
fillValueInput.addEventListener("input", updateOutput);

actionSelect.addEventListener("change", () => {
  updateVisibility();
  updateOutput();
});

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "ac8-capture") {
    updateCapture(message.capture);
  }
});

chrome.storage.local.get(["lastCapture", "captureStatus"], (result) => {
  if (result.lastCapture) {
    updateCapture(result.lastCapture);
  }

  if (result.captureStatus === "armed") {
    setStatus("Armed", "armed");
  }
});

updateVisibility();
