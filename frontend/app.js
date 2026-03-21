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
    document.getElementById('run-cashflow-btn').addEventListener('click', () => executeStep('/api/run/cashflow', 'Cashflow calculation'));
    document.getElementById('run-reporting-btn').addEventListener('click', () => executeStep('/api/run/reporting', 'Reporting Engine'));
    document.getElementById('run-stress-btn').addEventListener('click', () => executeStep('/api/run/stress-testing', 'Stress Testing'));

    // Data Loaders
    async function loadTable(url, tbodyId, cols) {
        try {
            const res = await fetch(url);
            const data = await res.json();
            if(data.error) throw new Error(data.error);
            
            const tbody = document.querySelector(`#${tbodyId} tbody`);
            tbody.innerHTML = '';
            
            data.data.forEach(row => {
                const tr = document.createElement('tr');
                cols.forEach(col => {
                    const td = document.createElement('td');
                    let val = row[col];
                    if(typeof val === 'number') val = val.toFixed(2);
                    td.textContent = val;
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
        } catch(e) {
            console.error('Failed to load table:', e);
        }
    }

    document.getElementById('load-data-btn').addEventListener('click', () => {
        loadTable('/api/data/clean-instruments', 'data-table', 
            ['instrument_id', 'instrument_type', 'notional', 'interest_rate', 'maturity_date', 'customer_segment']);
    });

    document.getElementById('load-cf-btn').addEventListener('click', () => {
        loadTable('/api/data/cashflows', 'cf-table', 
            ['instrument_id', 'date', 'principal_amount', 'interest_amount', 'total_amount']);
    });

    // Reports & Stress Scenarios
    document.getElementById('run-reporting-btn').addEventListener('click', () => {
        setTimeout(async () => {
            const res = await fetch('/api/data/reports');
            const data = await res.json();
            if(!data.error) {
                const lTbody = document.querySelector('#lcr-table tbody');
                lTbody.innerHTML = `<tr><td>${data.lcr[0].Metric}</td><td>${data.lcr[0].Ratio.toFixed(2)}</td></tr>`;
                
                const nTbody = document.querySelector('#nsfr-table tbody');
                nTbody.innerHTML = `<tr><td>${data.nsfr[0].Metric}</td><td>${data.nsfr[0].Ratio.toFixed(2)}</td></tr>`;
            }
        }, 1000);
    });

    document.getElementById('load-stress-btn').addEventListener('click', async () => {
        try {
            const res = await fetch('/api/data/stress-results');
            const data = await res.json();
            
            const cont = document.getElementById('stress-cards-container');
            cont.innerHTML = '';
            
            for(let scenario in data) {
                if(scenario === 'error') continue;
                cont.innerHTML += `
                    <div class="scenario-card">
                        <h4>${scenario}</h4>
                        <p>LCR Proxy: ${data[scenario].lcr_proxy.toFixed(2)}</p>
                        <p>Net Outflows: ${data[scenario].net_outflows.toFixed(2)}</p>
                    </div>
                `;
            }
        } catch (e) {
            console.error(e);
        }
    });
});
