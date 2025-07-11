// Global variables
let currentSymbol = '';
let portfolioData = {};

// Utility functions
function showAlert(title, message, type = 'info') {
    document.getElementById('alertModalTitle').textContent = title;
    document.getElementById('alertModalBody').innerHTML = message;
    
    // Try to use Bootstrap modal, fallback to browser alert if not available
    try {
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            const modal = new bootstrap.Modal(document.getElementById('alertModal'));
            modal.show();
        } else {
            // Fallback to browser alert
            alert(title + ': ' + message);
        }
    } catch (error) {
        console.error('Error showing modal:', error);
        // Fallback to browser alert
        alert(title + ': ' + message);
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(num, decimals = 2) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(num);
}

function showLoading(elementId) {
    document.getElementById(elementId).innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
}

// Market analysis functions
async function analyzeSymbol() {
    const symbol = document.getElementById('symbolInput').value.trim();
    if (!symbol) {
        showAlert('Error', 'Please enter a symbol');
        return;
    }
    
    currentSymbol = symbol;
    showLoading('analysisResult');
    showLoading('agentDecision');
    
    try {
        // Get technical analysis
        const analysisResponse = await fetch(`/api/analysis/${symbol}`);
        const analysisData = await analysisResponse.json();
        
        if (analysisData.error) {
            throw new Error(analysisData.error);
        }
        
        displayAnalysis(analysisData);
        
        // Get agent decision
        const agentResponse = await fetch(`/api/agents/decision/${symbol}`);
        const agentData = await agentResponse.json();
        
        if (agentData.error) {
            throw new Error(agentData.error);
        }
        
        displayAgentDecision(agentData);
        
    } catch (error) {
        document.getElementById('analysisResult').innerHTML = `<div class="error">Error: ${error.message}</div>`;
        document.getElementById('agentDecision').innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

function displayAnalysis(data) {
    const signals = data.signals || {};
    const indicators = data.technical_indicators || {};
    
    let html = `
        <div class="mb-3">
            <span class="recommendation-badge recommendation-${signals.recommendation?.toLowerCase() || 'hold'}">
                ${signals.recommendation || 'HOLD'}
            </span>
            <div class="confidence-bar">
                <div class="confidence-fill confidence-${getConfidenceLevel(signals.strength)}" 
                     style="width: ${(signals.strength || 0) * 100}%"></div>
            </div>
            <small class="text-muted">Confidence: ${formatNumber((signals.strength || 0) * 100, 0)}%</small>
        </div>
    `;
    
    if (signals.signals && signals.signals.length > 0) {
        html += '<div class="mb-3"><strong>Signals:</strong>';
        signals.signals.forEach(signal => {
            html += `<div class="signal-item">${signal}</div>`;
        });
        html += '</div>';
    }
    
    if (Object.keys(indicators).length > 0) {
        html += '<div class="technical-indicators">';
        for (const [key, value] of Object.entries(indicators)) {
            if (value !== null && value !== undefined) {
                html += `
                    <div class="indicator-item">
                        <div class="indicator-label">${key.replace(/_/g, ' ').toUpperCase()}</div>
                        <div class="indicator-value">${formatNumber(value)}</div>
                    </div>
                `;
            }
        }
        html += '</div>';
    }
    
    document.getElementById('analysisResult').innerHTML = html;
}

function displayAgentDecision(data) {
    const finalDecision = data.final_decision || {};
    const summary = data.summary || {};
    
    let html = `
        <div class="agent-decision">
            <h4>AI Recommendation</h4>
            <span class="recommendation-badge recommendation-${finalDecision.final_recommendation?.toLowerCase() || 'hold'}">
                ${finalDecision.final_recommendation || 'HOLD'}
            </span>
            <div class="confidence-bar">
                <div class="confidence-fill confidence-${getConfidenceLevel(finalDecision.confidence)}" 
                     style="width: ${(finalDecision.confidence || 0) * 100}%"></div>
            </div>
            <small class="text-muted">Consensus Confidence: ${formatNumber((finalDecision.confidence || 0) * 100, 0)}%</small>
        </div>
    `;
    
    if (finalDecision.reasoning && finalDecision.reasoning.length > 0) {
        html += '<div class="agent-reasoning"><strong>Reasoning:</strong><ul>';
        finalDecision.reasoning.forEach(reason => {
            html += `<li>${reason}</li>`;
        });
        html += '</ul></div>';
    }
    
    // Add individual agent decisions
    if (data.individual_agents && data.individual_agents.length > 0) {
        html += '<div class="mt-3"><small class="text-muted"><strong>Agent Breakdown:</strong></small>';
        data.individual_agents.forEach(agent => {
            html += `
                <div class="mt-1">
                    <small><strong>${agent.agent}:</strong> ${agent.recommendation} 
                    (${formatNumber((agent.confidence || 0) * 100, 0)}%)</small>
                </div>
            `;
        });
        html += '</div>';
    }
    
    document.getElementById('agentDecision').innerHTML = html;
}

function getConfidenceLevel(confidence) {
    if (confidence >= 0.7) return 'high';
    if (confidence >= 0.4) return 'medium';
    return 'low';
}

// Portfolio functions
async function loadPortfolio() {
    try {
        const response = await fetch('/api/portfolio');
        portfolioData = await response.json();
        
        if (portfolioData.error) {
            throw new Error(portfolioData.error);
        }
        
        displayPortfolio();
        
    } catch (error) {
        console.error('Error loading portfolio:', error);
        showAlert('Error', `Failed to load portfolio: ${error.message}`);
    }
}

function displayPortfolio() {
    const portfolio = portfolioData.portfolio || {};
    
    // Update summary cards
    document.getElementById('cashBalance').textContent = formatCurrency(portfolio.cash || 0);
    document.getElementById('totalPL').textContent = formatCurrency(portfolio.profit_loss || 0);
    document.getElementById('totalTrades').textContent = portfolio.total_positions || 0;
    
    // Update holdings table
    const holdings = portfolio.holdings || {};
    let holdingsHtml = '';
    
    if (Object.keys(holdings).length === 0) {
        holdingsHtml = '<p class="text-muted">No current holdings</p>';
    } else {
        holdingsHtml = `
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Quantity</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        for (const [symbol, quantity] of Object.entries(holdings)) {
            holdingsHtml += `
                <tr>
                    <td><strong>${symbol}</strong></td>
                    <td>${formatNumber(quantity, 4)}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-danger" onclick="quickSell('${symbol}', ${quantity})">
                            Quick Sell
                        </button>
                    </td>
                </tr>
            `;
        }
        
        holdingsHtml += '</tbody></table>';
    }
    
    document.getElementById('holdingsTable').innerHTML = holdingsHtml;
    
    // Update recent trades
    displayRecentTrades();
}

function displayRecentTrades() {
    const recentPositions = portfolioData.recent_positions || [];
    let html = '';
    
    if (recentPositions.length === 0) {
        html = '<p class="text-muted">No recent trades</p>';
    } else {
        recentPositions.reverse().forEach(position => {
            html += `
                <div class="trade-item trade-${position.action.toLowerCase()}">
                    <div class="d-flex justify-content-between">
                        <div>
                            <strong>${position.action}</strong> ${formatNumber(position.quantity)} ${position.symbol}
                        </div>
                        <div>
                            ${formatCurrency(position.price)}
                        </div>
                    </div>
                    <small class="text-muted">${new Date(position.timestamp).toLocaleString()}</small>
                </div>
            `;
        });
    }
    
    document.getElementById('recentTrades').innerHTML = html;
}

// Trading functions
async function executeTrade(event) {
    event.preventDefault();
    
    const symbol = document.getElementById('tradeSymbol').value.trim();
    const action = document.getElementById('tradeAction').value;
    const quantity = parseFloat(document.getElementById('tradeQuantity').value);
    const price = parseFloat(document.getElementById('tradePrice').value);
    
    if (!symbol || !action || !quantity || !price) {
        showAlert('Error', 'Please fill in all fields');
        return;
    }
    
    try {
        const response = await fetch('/api/execute-trade', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: symbol,
                action: action,
                quantity: quantity,
                price: price
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Success', result.message);
            document.getElementById('tradeForm').reset();
            loadPortfolio(); // Refresh portfolio
        } else {
            showAlert('Error', result.error);
        }
        
    } catch (error) {
        showAlert('Error', `Failed to execute trade: ${error.message}`);
    }
}

function quickSell(symbol, quantity) {
    document.getElementById('tradeSymbol').value = symbol;
    document.getElementById('tradeAction').value = 'SELL';
    document.getElementById('tradeQuantity').value = quantity;
    document.getElementById('tradePrice').focus();
    
    // Scroll to trading section
    document.getElementById('trading').scrollIntoView({ behavior: 'smooth' });
}

// Logs functions
async function loadLogs() {
    showLoading('logsTable');
    
    try {
        const response = await fetch('/api/logs');
        const logs = await response.json();
        
        if (logs.error) {
            throw new Error(logs.error);
        }
        
        displayLogs(logs);
        
    } catch (error) {
        document.getElementById('logsTable').innerHTML = `<div class="error">Error loading logs: ${error.message}</div>`;
    }
}

function displayLogs(logs) {
    if (!logs || logs.length === 0) {
        document.getElementById('logsTable').innerHTML = '<p class="text-muted">No logs available</p>';
        return;
    }
    
    let html = `
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Level</th>
                    <th>Module</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    logs.forEach(log => {
        const levelClass = log.level === 'ERROR' ? 'text-danger' : 
                          log.level === 'WARNING' ? 'text-warning' : 
                          log.level === 'INFO' ? 'text-info' : '';
        
        html += `
            <tr>
                <td><small>${new Date(log.timestamp).toLocaleString()}</small></td>
                <td><span class="badge bg-secondary ${levelClass}">${log.level}</span></td>
                <td><small>${log.module}</small></td>
                <td>${log.message}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    document.getElementById('logsTable').innerHTML = html;
}

// Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    document.getElementById(sectionId).style.display = 'block';
    
    // Update navbar
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`a[href="#${sectionId}"]`).classList.add('active');
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Set up navigation
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            showSection(sectionId);
            
            // Load data for specific sections
            if (sectionId === 'portfolio') {
                loadPortfolio();
            } else if (sectionId === 'logs') {
                loadLogs();
            }
        });
    });
    
    // Set up trade form
    document.getElementById('tradeForm').addEventListener('submit', executeTrade);
    
    // Show dashboard by default
    showSection('dashboard');
    
    // Load initial portfolio data
    loadPortfolio();
    
    // Auto-refresh portfolio every 30 seconds
    setInterval(loadPortfolio, 30000);
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.id === 'symbolInput') {
        analyzeSymbol();
    }
});