mkdir -p ~/chatgpt-auto-voice
cat > ~/chatgpt-auto-voice/manifest.json << 'EOF'
{
"manifest_version": 3,
"name": "ChatGPT Auto Voice",
"version": "1.0",
"description": "Automatically starts ChatGPT voice after 5 seconds",
"content_scripts": [
{
"matches": ["https://chatgpt.com/*"],
"js": ["content.js"],
"run_at": "document_idle"
}
]
}
EOF

cat > ~/chatgpt-auto-voice/content.js << 'EOF'
// Tries to click the voice/mic button after 5 seconds.
// If not found, retries for a short time.
(function () {
const findAndClick = () => {
const sel = [
'button[aria-label*="Voice" i]',
'button[aria-label*="Hang" i]',
'button[aria-label*="Mikrofon" i]',
'[data-testid*="voice"][role="button"]',
'[data-testid*="microphone"][role="button"]'
].join(', ');
const btn = document.querySelector(sel);
if (btn) {
btn.click();
console.log("Voice autostart: clicked.");
return true;
}
console.log("Voice autostart: mic button not found yet.");
return false;
};

setTimeout(() => {
if (findAndClick()) return;
let tries = 20;
const timer = setInterval(() => {
if (findAndClick() || --tries <= 0) clearInterval(timer);
}, 1000);
}, 5000);
})();
EOF
