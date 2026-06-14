// Lattice Web Client
let world = null;
let activeBlock = 1; // Default: Stone
let isDrawing = false;
let isPanning = false;

// Camera state
let zoom = 12; // pixels per cell
let offsetX = 50; // pixels
let offsetY = 50; // pixels
let lastMouseX = 0;
let lastMouseY = 0;

// Simulation loop state
let isPlaying = false;
let tickTimer = null;

// DOM Elements
const canvas = document.getElementById('world-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');
const coordInfo = document.getElementById('coord-info');
const blockSelector = document.getElementById('block-selector');
const statusSize = document.getElementById('status-size');
const statusChunks = document.getElementById('status-chunks');
const statusLoadedChunks = document.getElementById('status-loaded-chunks');

// Buttons & Form Inputs
const btnStep = document.getElementById('btn-step');
const btnPlay = document.getElementById('btn-play');
const speedSlider = document.getElementById('speed-slider');
const speedVal = document.getElementById('speed-val');
const btnFill = document.getElementById('btn-fill');
const fillX1 = document.getElementById('fill-x1');
const fillY1 = document.getElementById('fill-y1');
const fillX2 = document.getElementById('fill-x2');
const fillY2 = document.getElementById('fill-y2');
const btnLoadChunk = document.getElementById('btn-load-chunk');
const btnUnloadChunk = document.getElementById('btn-unload-chunk');
const chunkCx = document.getElementById('chunk-cx');
const chunkCy = document.getElementById('chunk-cy');
const chkGridOverlay = document.getElementById('chk-grid-overlay');
const btnReset = document.getElementById('btn-reset');
const resetW = document.getElementById('reset-w');
const resetH = document.getElementById('reset-h');
const resetCs = document.getElementById('reset-cs');
const btnExport = document.getElementById('btn-export');
const btnImport = document.getElementById('btn-import');
const txtSnapshot = document.getElementById('txt-snapshot');

// Start up
init();

async function init() {
    await fetchWorld();
    setupBlockSelector();
    setupEventListeners();
    centerCamera();
    render();
}

async function fetchWorld() {
    try {
        const res = await fetch('/api/world');
        world = await res.json();
        updateStatusBar();
    } catch (err) {
        console.error("Failed to fetch world state", err);
    }
}

function updateStatusBar() {
    if (!world) return;
    statusSize.textContent = `${world.width}x${world.height}`;
    const cx = Math.ceil(world.width / world.chunk_size);
    const cy = Math.ceil(world.height / world.chunk_size);
    statusChunks.textContent = `${cx * cy} (${cx}x${cy})`;
    statusLoadedChunks.textContent = world.loaded_chunks.length;
}

function setupBlockSelector() {
    if (!world) return;
    blockSelector.innerHTML = '';
    const blockNames = {
        0: 'air',
        1: 'stone',
        2: 'grass',
        3: 'dirt',
        4: 'sand',
        5: 'water'
    };

    Object.keys(world.block_colors).forEach(id => {
        const blockId = parseInt(id);
        const name = blockNames[blockId] || `block ${blockId}`;
        const color = world.block_colors[blockId];

        const option = document.createElement('div');
        option.className = `block-option ${blockId === activeBlock ? 'active' : ''}`;
        option.dataset.id = blockId;
        option.tabIndex = 0;
        option.setAttribute('role', 'radio');
        option.setAttribute('aria-checked', blockId === activeBlock ? 'true' : 'false');

        const preview = document.createElement('div');
        preview.className = 'block-color-preview';
        preview.style.backgroundColor = color;
        
        const text = document.createElement('div');
        text.className = 'block-name';
        text.textContent = name;

        option.appendChild(preview);
        option.appendChild(text);
        
        const selectBlock = () => {
            document.querySelectorAll('.block-option').forEach(el => {
                el.classList.remove('active');
                el.setAttribute('aria-checked', 'false');
            });
            option.classList.add('active');
            option.setAttribute('aria-checked', 'true');
            activeBlock = blockId;
        };

        option.addEventListener('click', selectBlock);
        option.addEventListener('keydown', (e) => {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                selectBlock();
            }
        });

        blockSelector.appendChild(option);
    });
}

function centerCamera() {
    if (!world) return;
    const viewWidth = container.clientWidth;
    const viewHeight = container.clientHeight;
    // Set initial zoom so the entire grid fits
    zoom = Math.floor(Math.min(viewWidth / world.width, viewHeight / world.height) * 0.8);
    zoom = Math.max(4, Math.min(zoom, 40));

    offsetX = (viewWidth - world.width * zoom) / 2;
    offsetY = (viewHeight - world.height * zoom) / 2;
}

// Convert screen coords to grid coords (taking y-axis inversion into account)
function screenToGrid(screenX, screenY) {
    if (!world) return null;
    const rect = canvas.getBoundingClientRect();
    const xOnCanvas = (screenX - rect.left) / zoom;
    const yOnCanvas = (screenY - rect.top) / zoom;

    const x = Math.floor(xOnCanvas);
    const y_inverted = Math.floor(yOnCanvas);
    const y = world.height - 1 - y_inverted; // Invert y-axis to match NumPy coordinate layout

    if (x >= 0 && x < world.width && y >= 0 && y < world.height) {
        return { x, y };
    }
    return null;
}

function render() {
    if (!world) return;

    // Resize canvas based on layout dimensions
    const cWidth = world.width * zoom;
    const cHeight = world.height * zoom;
    
    if (canvas.width !== cWidth || canvas.height !== cHeight) {
        canvas.width = cWidth;
        canvas.height = cHeight;
    }

    // Apply offset placement style
    canvas.style.left = `${offsetX}px`;
    canvas.style.top = `${offsetY}px`;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw blocks
    for (let y = 0; y < world.height; y++) {
        for (let x = 0; x < world.width; x++) {
            const blockId = world.grid[y][x];
            const color = world.block_colors[blockId] || '#FF00FF';
            ctx.fillStyle = color;
            // Draw matching matplotlib output origin='lower' (y=0 at the bottom)
            const drawY = (world.height - 1 - y) * zoom;
            ctx.fillRect(x * zoom, drawY, zoom, zoom);
        }
    }

    // Draw grid lines
    if (zoom >= 8) {
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let x = 0; x <= world.width; x++) {
            ctx.moveTo(x * zoom, 0);
            ctx.lineTo(x * zoom, canvas.height);
        }
        for (let y = 0; y <= world.height; y++) {
            ctx.moveTo(0, y * zoom);
            ctx.lineTo(canvas.width, y * zoom);
        }
        ctx.stroke();
    }

    // Draw Chunks Borders
    if (chkGridOverlay.checked) {
        const chunkSize = world.chunk_size;
        const totalChunksX = Math.ceil(world.width / chunkSize);
        const totalChunksY = Math.ceil(world.height / chunkSize);

        for (let cy = 0; cy < totalChunksY; cy++) {
            for (let cx = 0; cx < totalChunksX; cx++) {
                const isLoaded = world.loaded_chunks.some(chunk => chunk[0] === cx && chunk[1] === cy);
                ctx.strokeStyle = isLoaded ? '#10b981' : '#ef4444';
                ctx.lineWidth = isLoaded ? 2 : 1;
                ctx.setLineDash(isLoaded ? [] : [4, 4]);

                const x1 = cx * chunkSize * zoom;
                // Since y increases upwards:
                // chunk top edge starts from the bottom up
                const drawYMin = (world.height - (cy + 1) * chunkSize) * zoom;
                const drawYMax = (world.height - cy * chunkSize) * zoom;
                const y1 = Math.max(0, drawYMin);
                const h = Math.min(canvas.height, drawYMax) - y1;
                const w = Math.min(canvas.width, (cx + 1) * chunkSize * zoom) - x1;

                ctx.strokeRect(x1, y1, w, h);
            }
        }
        ctx.setLineDash([]); // Reset line dash
    }
}

function setupEventListeners() {
    // Mouse paint / interaction
    canvas.addEventListener('mousedown', (e) => {
        if (e.button === 0) { // Left click
            const gridPos = screenToGrid(e.clientX, e.clientY);
            if (gridPos) {
                if (e.shiftKey) {
                    // Shift+Click toggle chunk status
                    const cx = Math.floor(gridPos.x / world.chunk_size);
                    const cy = Math.floor(gridPos.y / world.chunk_size);
                    toggleChunk(cx, cy);
                } else {
                    isDrawing = true;
                    drawBlockAt(gridPos.x, gridPos.y);
                }
            }
        } else if (e.button === 1 || e.button === 2) { // Middle or Right click to pan
            isPanning = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            e.preventDefault();
        }
    });

    window.addEventListener('mouseup', () => {
        isDrawing = false;
        isPanning = false;
    });

    canvas.addEventListener('mousemove', (e) => {
        const gridPos = screenToGrid(e.clientX, e.clientY);
        if (gridPos) {
            const blockId = world.grid[gridPos.y][gridPos.x];
            const cx = Math.floor(gridPos.x / world.chunk_size);
            const cy = Math.floor(gridPos.y / world.chunk_size);
            const isLoaded = world.loaded_chunks.some(chunk => chunk[0] === cx && chunk[1] === cy);
            
            coordInfo.textContent = `Cell: (${gridPos.x}, ${gridPos.y}) | Material: ID ${blockId} | Chunk: (${cx}, ${cy}) [${isLoaded ? 'LOADED' : 'UNLOADED'}]`;

            if (isDrawing) {
                drawBlockAt(gridPos.x, gridPos.y);
            }
        } else {
            coordInfo.textContent = 'Hover canvas to inspect cells';
        }
    });

    // Handle panning using keyboard space + drag, or just dragging the container
    container.addEventListener('mousedown', (e) => {
        if (e.target === container) {
            isPanning = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }
    });

    window.addEventListener('mousemove', (e) => {
        if (isPanning) {
            const dx = e.clientX - lastMouseX;
            const dy = e.clientY - lastMouseY;
            offsetX += dx;
            offsetY += dy;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            render();
        }
    });

    canvas.addEventListener('contextmenu', (e) => e.preventDefault());

    // Zoom event
    container.addEventListener('wheel', (e) => {
        e.preventDefault();
        const rect = container.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Current coordinates relative to canvas
        const canvasX = mouseX - offsetX;
        const canvasY = mouseY - offsetY;

        const zoomFactor = e.deltaY < 0 ? 1.2 : 0.8;
        const newZoom = Math.max(2, Math.min(zoom * zoomFactor, 60));

        if (newZoom !== zoom) {
            // Recenter coordinates around the mouse pointer
            offsetX = mouseX - canvasX * (newZoom / zoom);
            offsetY = mouseY - canvasY * (newZoom / zoom);
            zoom = newZoom;
            render();
        }
    }, { passive: false });

    // Step tick button
    btnStep.addEventListener('click', async () => {
        await tick();
    });

    // Play/Pause button
    btnPlay.addEventListener('click', () => {
        if (isPlaying) {
            pause();
        } else {
            play();
        }
    });

    // Speed slider
    speedSlider.addEventListener('input', () => {
        speedVal.textContent = speedSlider.value;
        if (isPlaying) {
            pause();
            play();
        }
    });

    // Fill tool
    btnFill.addEventListener('click', async () => {
        const x1 = parseInt(fillX1.value);
        const y1 = parseInt(fillY1.value);
        const x2 = parseInt(fillX2.value);
        const y2 = parseInt(fillY2.value);

        if (isNaN(x1) || isNaN(y1) || isNaN(x2) || isNaN(y2)) {
            alert("Enter valid coordinates");
            return;
        }

        try {
            const res = await fetch('/api/fill', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ x1, y1, x2, y2, block: activeBlock })
            });
            if (!res.ok) {
                const err = await res.json();
                alert(`Error: ${err.detail}`);
                return;
            }
            world = await res.json();
            updateStatusBar();
            render();
        } catch (err) {
            alert("Connection error");
        }
    });

    // Chunk load/unload manually
    btnLoadChunk.addEventListener('click', async () => {
        const cx = parseInt(chunkCx.value);
        const cy = parseInt(chunkCy.value);
        if (isNaN(cx) || isNaN(cy)) return;
        
        const res = await fetch('/api/chunk/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cx, cy })
        });
        const data = await res.json();
        world.loaded_chunks = data.loaded_chunks;
        updateStatusBar();
        render();
    });

    btnUnloadChunk.addEventListener('click', async () => {
        const cx = parseInt(chunkCx.value);
        const cy = parseInt(chunkCy.value);
        if (isNaN(cx) || isNaN(cy)) return;
        
        const res = await fetch('/api/chunk/unload', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cx, cy })
        });
        const data = await res.json();
        world.loaded_chunks = data.loaded_chunks;
        updateStatusBar();
        render();
    });

    chkGridOverlay.addEventListener('change', () => {
        render();
    });

    // Reset button
    btnReset.addEventListener('click', async () => {
        const width = parseInt(resetW.value);
        const height = parseInt(resetH.value);
        const chunk_size = parseInt(resetCs.value);

        if (isNaN(width) || isNaN(height) || isNaN(chunk_size)) return;

        const res = await fetch('/api/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ width, height, chunk_size })
        });
        world = await res.json();
        updateStatusBar();
        centerCamera();
        render();
    });

    // Snapshot buttons
    btnExport.addEventListener('click', async () => {
        const res = await fetch('/api/snapshot/save', { method: 'POST' });
        const data = await res.json();
        txtSnapshot.value = data.snapshot;
        txtSnapshot.select();
        document.execCommand('copy');
        alert("Snapshot JSON copied to clipboard!");
    });

    btnImport.addEventListener('click', async () => {
        const json = txtSnapshot.value.trim();
        if (!json) return;

        try {
            const res = await fetch('/api/snapshot/load', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: json })
            });
            if (!res.ok) {
                const err = await res.json();
                alert(`Error: ${err.detail}`);
                return;
            }
            world = await res.json();
            updateStatusBar();
            centerCamera();
            render();
            txtSnapshot.value = '';
            alert("Snapshot loaded successfully!");
        } catch (err) {
            alert("Failed to load snapshot");
        }
    });

    // Resize viewport
    window.addEventListener('resize', () => {
        render();
    });
}

async function drawBlockAt(x, y) {
    if (!world) return;
    // Update local grid state instantly for smooth rendering
    if (world.grid[y][x] === activeBlock) return;
    
    world.grid[y][x] = activeBlock;
    render();

    try {
        await fetch('/api/block', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ x, y, block: activeBlock })
        });
    } catch (err) {
        console.error("Failed to sync block drawing", err);
    }
}

async function toggleChunk(cx, cy) {
    if (!world) return;
    const isLoaded = world.loaded_chunks.some(chunk => chunk[0] === cx && chunk[1] === cy);
    const endpoint = isLoaded ? '/api/chunk/unload' : '/api/chunk/load';

    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cx, cy })
        });
        const data = await res.json();
        world.loaded_chunks = data.loaded_chunks;
        updateStatusBar();
        render();
    } catch (err) {
        console.error("Failed to toggle chunk status", err);
    }
}

async function tick() {
    try {
        const res = await fetch('/api/tick', { method: 'POST' });
        world = await res.json();
        updateStatusBar();
        render();
    } catch (err) {
        console.error("Failed to run tick", err);
    }
}

function play() {
    isPlaying = true;
    btnPlay.textContent = "Pause";
    btnPlay.className = "btn danger-btn";
    const interval = parseInt(speedSlider.value);
    tickTimer = setInterval(tick, interval);
}

function pause() {
    isPlaying = false;
    btnPlay.textContent = "Play";
    btnPlay.className = "btn success";
    clearInterval(tickTimer);
    tickTimer = null;
}
