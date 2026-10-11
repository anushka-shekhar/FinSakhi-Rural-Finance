/**
 * FinSakhi - Business Finance Calculator Script
 * Provides instant client-side preview for rural entrepreneurs.
 */

document.addEventListener('DOMContentLoaded', () => {
    const incomeInput = document.getElementById('monthly_income');
    const expenseInput = document.getElementById('monthly_expenses');
    const savingsInput = document.getElementById('monthly_savings');

    const liveProfit = document.getElementById('live-profit');
    const liveProfitPct = document.getElementById('live-profit-pct');
    const liveSavingsPct = document.getElementById('live-savings-pct');
    const liveRemaining = document.getElementById('live-remaining');

    function updateLiveCalculation() {
        if (!incomeInput || !expenseInput) return;

        const income = parseFloat(incomeInput.value) || 0;
        const expenses = parseFloat(expenseInput.value) || 0;
        const savings = parseFloat(savingsInput ? savingsInput.value : 0) || 0;

        const profit = income - expenses;
        const remaining = profit - savings;

        const profitPct = income > 0 ? ((profit / income) * 100).toFixed(1) : 0;
        const savingsPct = income > 0 ? ((savings / income) * 100).toFixed(1) : 0;

        if (liveProfit) liveProfit.textContent = '₹ ' + profit.toLocaleString('en-IN');
        if (liveProfitPct) liveProfitPct.textContent = profitPct + '%';
        if (liveSavingsPct) liveSavingsPct.textContent = savingsPct + '%';
        if (liveRemaining) liveRemaining.textContent = '₹ ' + remaining.toLocaleString('en-IN');
    }

    if (incomeInput && expenseInput) {
        incomeInput.addEventListener('input', updateLiveCalculation);
        expenseInput.addEventListener('input', updateLiveCalculation);
        if (savingsInput) savingsInput.addEventListener('input', updateLiveCalculation);
    }
});
