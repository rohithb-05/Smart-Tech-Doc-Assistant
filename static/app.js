document.addEventListener('DOMContentLoaded', () => {

    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const chatForm = document.getElementById('chatForm');
    const queryInput = document.getElementById('queryInput');
    const messagesBox = document.getElementById('messagesBox');
    const sendBtn = document.getElementById('sendBtn');

    // Drag and Drop Logic
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false)
    });

    function preventDefaults(e) {
        e.preventDefault()
        e.stopPropagation()
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false)
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false)
    });

    function highlight(e) {
        dropArea.classList.add('dragover')
    }

    function unhighlight(e) {
        dropArea.classList.remove('dragover')
    }

    dropArea.addEventListener('drop', handleDrop, false)
    dropArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            uploadFile(this.files[0]);
        }
    });

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;
        if(files.length > 0) {
            uploadFile(files[0]);
        }
    }

    function showStatus(msg, type) {
        uploadStatus.className = `status-msg ${type}`;
        uploadStatus.innerHTML = msg;
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        showStatus('Uploading and Indexing... Please wait.', 'loading');

        try {
            const res = await fetch('/docs/ingest', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await res.json();
            showStatus(`✅ Successfully indexed!<br><small>Chunks embedded: ${data.chunks_added}</small>`, 'success');
        } catch (error) {
            console.error(error);
            showStatus(`❌ Error: ${error.message}`, 'error');
        }
    }

    // Chat Logic
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        // 1. Add User Message
        appendMessage('User', query, 'user');
        queryInput.value = '';
        sendBtn.disabled = true;

        // 2. Add Loading Bubble
        const loadingId = appendLoading();

        try {
            const res = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            if(!res.ok) throw new Error("Server error fetching response");
            
            const data = await res.json();
            
            // 3. Remove Loading Bubble & Add Assistant Response
            document.getElementById(loadingId).remove();
            
            // Parse Markdown safely
            // Note: `marked` comes from the CDN we included in index.html
            const parsedHtml = marked.parse(data.answer);
            appendMessage('AI', parsedHtml, 'assistant', true);

        } catch (error) {
            document.getElementById(loadingId).remove();
            appendMessage('AI', `<p style="color:var(--error)">Error: ${error.message}</p>`, 'assistant', true);
        }

        sendBtn.disabled = false;
        queryInput.focus();
    });

    function appendMessage(sender, text, type, isHtml=false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}`;
        
        const avatar = `<div class="avatar">${sender === 'User' ? 'You' : 'AI'}</div>`;
        const content = isHtml ? text : `<p>${escapeHTML(text)}</p>`;
        
        msgDiv.innerHTML = `
            ${avatar}
            <div class="bubble">
                ${content}
            </div>
        `;

        messagesBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message assistant`;
        msgDiv.id = id;
        
        msgDiv.innerHTML = `
            <div class="avatar">AI</div>
            <div class="bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;

        messagesBox.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function scrollToBottom() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
});
