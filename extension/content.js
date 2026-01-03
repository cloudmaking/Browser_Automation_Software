let armed = false;
let captureAction = "click";
let cleanupTimer = null;

function escapeCss(value) {
  if (window.CSS && CSS.escape) {
    return CSS.escape(value);
  }
  return String(value)
    .replace(/([!"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~])/g, "\\$1")
    .replace(/\s+/g, "\\ ");
}

function isUniqueId(id) {
  try {
    return document.querySelectorAll(`#${escapeCss(id)}`).length === 1;
  } catch (error) {
    return false;
  }
}

function getCssSelector(element) {
  if (!element || element.nodeType !== 1) return "";
  if (element.id && isUniqueId(element.id)) {
    return `#${escapeCss(element.id)}`;
  }

  const parts = [];
  let current = element;

  while (current && current.nodeType === 1 && current !== document.documentElement) {
    let part = current.tagName.toLowerCase();

    const classList = Array.from(current.classList || []).filter(Boolean).slice(0, 3);
    if (classList.length) {
      part += `.${classList.map(escapeCss).join(".")}`;
    }

    const parent = current.parentElement;
    if (parent) {
      const siblings = Array.from(parent.children).filter(
        (child) => child.tagName === current.tagName
      );
      if (siblings.length > 1) {
        const index = siblings.indexOf(current) + 1;
        part += `:nth-of-type(${index})`;
      }
    }

    if (current.id && isUniqueId(current.id)) {
      parts.unshift(`#${escapeCss(current.id)}`);
      break;
    }

    parts.unshift(part);
    current = current.parentElement;
  }

  return parts.join(" > ");
}

function getXPath(element) {
  if (!element || element.nodeType !== 1) return "";
  if (element.id) {
    return `//*[@id=\"${element.id}\"]`;
  }

  const parts = [];
  let current = element;

  while (current && current.nodeType === 1) {
    const tag = current.tagName.toLowerCase();
    const parent = current.parentNode;
    if (!parent) break;

    const siblings = Array.from(parent.children).filter(
      (child) => child.tagName === current.tagName
    );
    const index = siblings.indexOf(current) + 1;
    parts.unshift(`${tag}[${index}]`);

    if (tag === "html") break;
    current = parent;
  }

  return `/${parts.join("/")}`;
}

function normalizeText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function captureElement(element, action) {
  const css = getCssSelector(element);
  const xpath = getXPath(element);
  const text = normalizeText(element.innerText || element.textContent);

  const meta = {
    tag: element.tagName.toLowerCase(),
    id: element.id || "",
    classes: Array.from(element.classList || []).filter(Boolean),
    name: element.getAttribute("name") || "",
    type: element.getAttribute("type") || "",
    placeholder: element.getAttribute("placeholder") || "",
    ariaLabel: element.getAttribute("aria-label") || "",
    role: element.getAttribute("role") || "",
  };

  return {
    action,
    selectors: {
      css,
      xpath,
      text: text.slice(0, 160),
    },
    meta,
    url: window.location.href,
    capturedAt: new Date().toISOString(),
  };
}

function highlight(element) {
  const previous = element.style.outline;
  element.style.outline = "2px solid #ff6a00";
  clearTimeout(cleanupTimer);
  cleanupTimer = setTimeout(() => {
    element.style.outline = previous;
  }, 1200);
}

function handleClick(event) {
  if (!armed) return;
  armed = false;

  event.preventDefault();
  event.stopPropagation();
  event.stopImmediatePropagation();

  document.removeEventListener("click", handleClick, true);

  const element = event.target;
  highlight(element);

  const capture = captureElement(element, captureAction);
  chrome.storage.local.set({
    lastCapture: capture,
    captureStatus: "captured",
    captureAction: captureAction,
    captureStartedAt: Date.now(),
  });

  chrome.runtime.sendMessage({ type: "ac8-capture", capture });
}

function armCapture(action) {
  if (armed) {
    document.removeEventListener("click", handleClick, true);
  }

  armed = true;
  captureAction = action;
  document.addEventListener("click", handleClick, true);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "ac8-start-capture") {
    armCapture(message.action || "click");
    sendResponse({ ok: true });
  }
});
