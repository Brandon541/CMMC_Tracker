document.addEventListener("DOMContentLoaded", () => {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');
    navLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            sections.forEach(s => s.classList.remove('active'));
            target.classList.add('active');
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Charts
    const complianceCtx = document.getElementById('complianceChart').getContext('2d');
    const domainCtx = document.getElementById('domainChart').getContext('2d');
    let complianceChart, domainChart;

    // Data
    let allControls = [];
    let allPoams = [];

    // Fetch and render data
    const fetchData = async () => {
        try {
            const [controlsRes, poamsRes] = await Promise.all([
                fetch('/api/controls'),
                fetch('/api/poams'),
            ]);
            allControls = await controlsRes.json();
            allPoams = await poamsRes.json();
            renderDashboard();
            renderControls();
            renderPoams();
        } catch (error) {
            console.error("Failed to fetch data:", error);
        }
    };

    const renderDashboard = () => {
        // Calculate accurate statistics
        const implemented = allControls.filter(c => c.status === 'implemented').length;
        const total = allControls.length;
        const compliance = total > 0 ? (implemented / total) * 100 : 0;
        
        // Active POAMs (not completed)
        const activePoams = allPoams.filter(p => p.status !== 'completed').length;
        
        // High Priority Issues (high and critical POAMs that are not completed)
        const highPriorityIssues = allPoams.filter(p => 
            (p.priority === 'high' || p.priority === 'critical') && p.status !== 'completed'
        ).length;
        
        // Update dashboard statistics
        document.querySelector('.progress-text').textContent = `${Math.round(compliance)}%`;
        document.getElementById('activePoamsCount').textContent = activePoams;
        document.getElementById('controlsImplementedCount').textContent = `${implemented}/${total}`;
        document.getElementById('highPriorityCount').textContent = highPriorityIssues;

        // Compliance Chart
        if (complianceChart) complianceChart.destroy();
        complianceChart = new Chart(complianceCtx, {
            type: 'doughnut',
            data: { datasets: [{ data: [compliance, 100 - compliance], backgroundColor: ['#27ae60', '#ecf0f1'] }] },
            options: { cutout: '70%', plugins: { legend: { display: false } } },
        });

        // Domain Chart
        const domains = [...new Set(allControls.map(c => c.domain))].sort();
        const domainData = domains.map(domain => {
            const domainControls = allControls.filter(c => c.domain === domain);
            const domainImplemented = domainControls.filter(c => c.status === 'implemented').length;
            return domainControls.length > 0 ? (domainImplemented / domainControls.length) * 100 : 0;
        });

        if (domainChart) domainChart.destroy();
        domainChart = new Chart(domainCtx, {
            type: 'bar',
            data: { 
                labels: domains, 
                datasets: [{ 
                    label: 'Compliance %', 
                    data: domainData, 
                    backgroundColor: '#3498db',
                    borderColor: '#2980b9',
                    borderWidth: 1
                }] 
            },
            options: { 
                responsive: true,
                scales: { 
                    y: { 
                        beginAtZero: true, 
                        max: 100,
                        title: { display: true, text: 'Compliance %' }
                    },
                    x: {
                        title: { display: true, text: 'CMMC Domains' }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.y.toFixed(1)}% compliant`;
                            }
                        }
                    }
                }
            },
        });
    };

const renderControls = () => {
        const list = document.getElementById('controlsList');
        list.innerHTML = allControls.map(control => `
            <div class="control-item">
                <div class="control-header">
                    <span class="control-id">${control.id}</span>
                    <select data-control-id="${control.id}" class="status-select">
                        <option value="implemented" ${control.status === 'implemented' ? 'selected' : ''}>Implemented</option>
                        <option value="partial" ${control.status === 'partial' ? 'selected' : ''}>Partial</option>
                        <option value="not-implemented" ${control.status === 'not-implemented' ? 'selected' : ''}>Not Implemented</option>
                    </select>
                </div>
                <p class="control-description">${control.description}</p>
                
                <h4>Objectives</h4>
                <ul class="objectives-list">
                    ${control.objectives.map((obj, idx) => `<li>
                        <div class="objective-item">
                            <strong>${obj.objective}:</strong>
                            <textarea 
                                data-control-id="${control.id}" 
                                data-obj-idx="${idx}" 
                                class="note-input" 
                                placeholder="Add notes for this objective...">${obj.notes}</textarea>
                        </div>
                    </li>`).join('')}
                </ul>
            </div>
        `).join('');

        // Handle status changes
        document.querySelectorAll('.status-select').forEach(select => {
            select.addEventListener('change', async (e) => {
                const controlId = e.target.getAttribute('data-control-id');
                const newStatus = e.target.value;
                const control = allControls.find(c => c.id === controlId);
                if (control) {
                    control.status = newStatus;
                    console.log(`Updated status for ${controlId} to ${newStatus}`);
                    
                    // Save to database
                    try {
                        await fetch(`/api/controls/${controlId}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(control)
                        });
                        // Update the dashboard charts
                        renderDashboard();
                    } catch (error) {
                        console.error('Error saving control status:', error);
                        alert('Error saving control status. Please try again.');
                    }
                }
            });
        });

        // Handle note saving
        document.querySelectorAll('.note-input').forEach(input => {
            input.addEventListener('change', async (e) => {
                const controlId = e.target.getAttribute('data-control-id');
                const objIdx = parseInt(e.target.getAttribute('data-obj-idx'), 10);
                const control = allControls.find(c => c.id === controlId);
                if (control) {
                    const newNotes = e.target.value;
                    control.objectives[objIdx].notes = newNotes;
                    console.log(`Updated notes for ${controlId} objective ${objIdx + 1}:`, newNotes);
                    
                    // Save changes to the server
                    try {
                        await fetch(`/api/controls/${controlId}/notes`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                objective_index: objIdx,
                                notes: newNotes
                            })
                        });
                    } catch (error) {
                        console.error('Error saving notes:', error);
                        alert('Error saving notes. Please try again.');
                    }
                }
            });
        });
    };

    const renderPoams = () => {
        const list = document.getElementById('poamsList');
        list.innerHTML = allPoams.map(poam => `
            <div class="poam-item">
                <div class="poam-header">
                    <span class="poam-title">${poam.title}</span>
                    <span class="poam-priority priority-${poam.priority}">${poam.priority}</span>
                </div>
                <p>${poam.description}</p>
                <div class="poam-meta">
                    <span><strong>Control:</strong> ${poam.control}</span>
                    <span><strong>Due:</strong> ${poam.dueDate}</span>
                    <span><strong>Assignee:</strong> ${poam.assignee}</span>
                    <span><strong>Status:</strong> ${poam.status}</span>
                </div>
                <div class="poam-actions">
                    <button class="btn btn-sm btn-secondary" onclick="editPoam(${poam.id})">Edit</button>
                    <button class="btn btn-sm btn-danger" onclick="deletePoam(${poam.id})">Delete</button>
                </div>
            </div>
        `).join('');
    };

    // Add POAM functionality
    const addPoamBtn = document.getElementById('addPoamBtn');
    const poamModal = document.getElementById('poamModal');
    const closeModal = document.querySelector('.modal .close');
    const cancelPoamBtn = document.getElementById('cancelPoam');
    const poamForm = document.getElementById('poamForm');
    let editingPoamId = null;

    // Populate control dropdown when modal opens
    const populateControlDropdown = () => {
        const controlSelect = document.getElementById('poamControl');
        controlSelect.innerHTML = '<option value="">Select Control</option>' + 
            allControls.map(control => `<option value="${control.id}">${control.id} - ${control.name}</option>`).join('');
    };

    // Show modal for adding new POAM
    if (addPoamBtn) {
        addPoamBtn.addEventListener('click', () => {
            editingPoamId = null;
            poamForm.reset();
            populateControlDropdown();
            document.querySelector('#poamModal h2').textContent = 'Add New POA&M';
            poamModal.style.display = 'block';
        });
    }

    // Close modal handlers
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            poamModal.style.display = 'none';
        });
    }

    if (cancelPoamBtn) {
        cancelPoamBtn.addEventListener('click', () => {
            poamModal.style.display = 'none';
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === poamModal) {
            poamModal.style.display = 'none';
        }
    });

    // Handle POAM form submission
    if (poamForm) {
        poamForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(poamForm);
            const poamData = {
                title: formData.get('title'),
                control: formData.get('control'),
                description: formData.get('description'),
                priority: formData.get('priority'),
                dueDate: formData.get('dueDate'),
                assignee: formData.get('assignee'),
                status: formData.get('status') || 'not-started'
            };

            try {
                if (editingPoamId) {
                    // Update existing POAM
                    await fetch(`/api/poams/${editingPoamId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(poamData)
                    });
                } else {
                    // Add new POAM
                    await fetch('/api/poams', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(poamData)
                    });
                }
                
                // Refresh data from database
                await fetchData();
                poamModal.style.display = 'none';
                poamForm.reset();
            } catch (error) {
                console.error('Error saving POAM:', error);
                alert('Error saving POA&M. Please try again.');
            }
        });
    }

    // Global functions for POAM operations
    window.editPoam = (id) => {
        const poam = allPoams.find(p => p.id === id);
        if (poam) {
            editingPoamId = id;
            populateControlDropdown();
            
            // Populate form with existing data
            document.getElementById('poamTitle').value = poam.title;
            document.getElementById('poamControl').value = poam.control;
            document.getElementById('poamDescription').value = poam.description;
            document.getElementById('poamPriority').value = poam.priority;
            document.getElementById('poamDueDate').value = poam.dueDate;
            document.getElementById('poamAssignee').value = poam.assignee;
            document.getElementById('poamStatus').value = poam.status || 'not-started';
            
            document.querySelector('#poamModal h2').textContent = 'Edit POA&M';
            poamModal.style.display = 'block';
        }
    };

    window.deletePoam = async (id) => {
        if (confirm('Are you sure you want to delete this POA&M?')) {
            try {
                await fetch(`/api/poams/${id}`, {
                    method: 'DELETE'
                });
                await fetchData(); // Refresh data
            } catch (error) {
                console.error('Error deleting POAM:', error);
                alert('Error deleting POA&M. Please try again.');
            }
        }
    };

    // Update dashboard statistics
    const updateDashboardStats = () => {
        const activePoamsCount = allPoams.length;
        const highPriorityCount = allPoams.filter(p => p.priority === 'high' || p.priority === 'critical').length;
        
        // Update the dashboard cards
        const activePoamsElement = document.querySelector('.stat-card:nth-child(2) .stat-number');
        const highPriorityElement = document.querySelector('.stat-card:nth-child(4) .stat-number');
        
        if (activePoamsElement) activePoamsElement.textContent = activePoamsCount;
        if (highPriorityElement) highPriorityElement.textContent = highPriorityCount;
    };

    // Add filtering functionality
    const domainFilter = document.getElementById('domainFilter');
    const statusFilter = document.getElementById('statusFilter');
    
    const applyFilters = () => {
        const domainValue = domainFilter.value;
        const statusValue = statusFilter.value;
        
        let filteredControls = allControls;
        
        if (domainValue !== 'all') {
            filteredControls = filteredControls.filter(c => c.domain === domainValue);
        }
        
        if (statusValue !== 'all') {
            filteredControls = filteredControls.filter(c => c.status === statusValue);
        }
        
        renderFilteredControls(filteredControls);
    };
    
    const renderFilteredControls = (controlsToRender) => {
        const list = document.getElementById('controlsList');
        list.innerHTML = controlsToRender.map(control => `
            <div class="control-item">
                <div class="control-header">
                    <span class="control-id">${control.id}</span>
                    <select data-control-id="${control.id}" class="status-select">
                        <option value="implemented" ${control.status === 'implemented' ? 'selected' : ''}>Implemented</option>
                        <option value="partial" ${control.status === 'partial' ? 'selected' : ''}>Partial</option>
                        <option value="not-implemented" ${control.status === 'not-implemented' ? 'selected' : ''}>Not Implemented</option>
                    </select>
                </div>
                <p class="control-description">${control.description}</p>
                
                <h4>Objectives</h4>
                <ul class="objectives-list">
                    ${control.objectives.map((obj, idx) => `<li>
                        <div class="objective-item">
                            <strong>${obj.objective}:</strong>
                            <textarea 
                                data-control-id="${control.id}" 
                                data-obj-idx="${idx}" 
                                class="note-input" 
                                placeholder="Add notes for this objective...">${obj.notes}</textarea>
                        </div>
                    </li>`).join('')}
                </ul>
            </div>
        `).join('');

        // Handle status changes for filtered controls
        document.querySelectorAll('.status-select').forEach(select => {
            select.addEventListener('change', async (e) => {
                const controlId = e.target.getAttribute('data-control-id');
                const newStatus = e.target.value;
                const control = allControls.find(c => c.id === controlId);
                if (control) {
                    control.status = newStatus;
                    console.log(`Updated status for ${controlId} to ${newStatus}`);
                    
                    // Save to database
                    try {
                        await fetch(`/api/controls/${controlId}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(control)
                        });
                        // Update the dashboard charts
                        renderDashboard();
                    } catch (error) {
                        console.error('Error saving control status:', error);
                        alert('Error saving control status. Please try again.');
                    }
                }
            });
        });

        // Re-attach event listeners for note inputs
        document.querySelectorAll('.note-input').forEach(input => {
            input.addEventListener('change', (e) => {
                const controlId = e.target.getAttribute('data-control-id');
                const objIdx = parseInt(e.target.getAttribute('data-obj-idx'), 10);
                const control = allControls.find(c => c.id === controlId);
                if (control) {
                    control.objectives[objIdx].notes = e.target.value;
                    console.log(`Updated notes for ${controlId} objective ${objIdx + 1}:`, e.target.value);
                }
            });
        });
    };
    
    if (domainFilter && statusFilter) {
        domainFilter.addEventListener('change', applyFilters);
        statusFilter.addEventListener('change', applyFilters);
    }

    // Dashboard card click handlers
    const activePoamsCard = document.getElementById('activePoamsCard');
    const highPriorityCard = document.getElementById('highPriorityCard');
    
    if (activePoamsCard) {
        activePoamsCard.addEventListener('click', () => {
            // Navigate to POAMs tab and show active POAMs
            document.querySelector('a[href="#poams"]').click();
            // Optionally filter to show only active POAMs
            setTimeout(() => {
                const poamItems = document.querySelectorAll('.poam-item');
                poamItems.forEach(item => {
                    const statusText = item.querySelector('.poam-meta span:last-child').textContent;
                    if (statusText.includes('completed')) {
                        item.style.display = 'none';
                    } else {
                        item.style.display = 'block';
                    }
                });
            }, 100);
        });
    }
    
    if (highPriorityCard) {
        highPriorityCard.addEventListener('click', () => {
            // Navigate to POAMs tab and show high priority POAMs
            document.querySelector('a[href="#poams"]').click();
            // Filter to show only high/critical priority POAMs
            setTimeout(() => {
                const poamItems = document.querySelectorAll('.poam-item');
                poamItems.forEach(item => {
                    const priorityElement = item.querySelector('.poam-priority');
                    const priority = priorityElement.textContent.toLowerCase();
                    const statusText = item.querySelector('.poam-meta span:last-child').textContent;
                    
                    if ((priority === 'high' || priority === 'critical') && !statusText.includes('completed')) {
                        item.style.display = 'block';
                        item.style.border = '2px solid #e74c3c';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }, 100);
        });
    }

    fetchData();
});
