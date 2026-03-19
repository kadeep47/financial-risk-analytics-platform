document.addEventListener('DOMContentLoaded', () => {
    
    // Navigation
    const navBtns = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.view-section');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // Logging
    const logger = document.getElementById('global-log');
    function log(msg) {
        const time = new Date().toLocaleTimeString();
        logger.textContent += `\n[${time}] ${msg}`;
        logger.scrollTop = logger.scrollHeight;
    }

    // Node state management
    function setNodeState(id, state) {
        const node = document.getElementById(id);
        if(!node) return;
        node.classList.remove('running', 'success', 'error');
        if(state) node.classList.add(state);
    }

    async function executeStep(url, name, nodeId) {
        if(nodeId) setNodeState(nodeId, 'running');
        log(`Started: ${name}...`);
        
        try {
            const resp = await fetch(url, { method: 'POST' });
            const data = await resp.json();
            
            if(!resp.ok) throw new Error(data.detail || 'Execution Failed');
            
            log(`Success: ${name}\n${data.message}`);
            if(nodeId) setNodeState(nodeId, 'success');
            return true;
        } catch (e) {
            log(`Error: ${name}\n${e.message}`);
            if(nodeId) setNodeState(nodeId, 'error');
            return false;
        }
    }

    // Pipeline Execution
    document.getElementById('run-all-btn').addEventListener('click', async () => {
        log('INITIALIZING STRAT-TO-FINISH PIPELINE RUN...');
        
        // Reset all nodes
        ['node-data-platform', 'node-cashflow-engine', 'node-reporting-engine', 'node-stress-testing']
            .forEach(id => setNodeState(id, ''));

        const s1 = await executeStep('/api/run/data-generation', 'Data Generation', 'node-data-platform');
        if(!s1) return;
        const s2 = await executeStep('/api/run/data-validation', 'Data Validation', 'node-data-platform');
        if(!s2) return;
        const s3 = await executeStep('/api/run/cashflow', 'Cashflow Engine', 'node-cashflow-engine');
        if(!s3) return;
        const s4 = await executeStep('/api/run/reporting', 'Reporting Engine', 'node-reporting-engine');
        if(!s4) return;
        const s5 = await executeStep('/api/run/stress-testing', 'Stress Scenarios', 'node-stress-testing');
        if(!s5) return;
        
        log('PIPELINE COMPLETED SUCCESSFULLY!');
    });

    // Individual Step buttons
    document.getElementById('run-data-gen-btn').addEventListener('click', () => executeStep('/api/run/data-generation', 'Data Gen'));
    document.getElementById('run-data-val-btn').addEventListener('click', () => executeStep('/api/run/data-validation', 'Data Validation'));
