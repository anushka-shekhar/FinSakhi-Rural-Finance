/**
 * FinSakhi - Budget Planner Client-Side Script
 * Computes live sum of expense categories and remaining surplus.
 */

document.addEventListener('DOMContentLoaded', () => {
    const incomeInput = document.getElementById('monthly_income');
    const targetSavingsInput = document.getElementById('target_savings');
    const expenseFields = document.querySelectorAll('.expense-item');

    const liveTotalExpenses = document.getElementById('live-total-expenses');
    const liveNetBalance = document.getElementById('live-net-balance');

    function calculateBudgetLive() {
        if (!incomeInput) return;

        const income = parseFloat(incomeInput.value) || 0;
        const targetSavings = parseFloat(targetSavingsInput ? targetSavingsInput.value : 0) || 0;

        let totalExp = 0;
        expenseFields.forEach(field => {
            totalExp += parseFloat(field.value) || 0;
        });

        const netBalance = income - totalExp - targetSavings;

        if (liveTotalExpenses) liveTotalExpenses.textContent = '₹ ' + totalExp.toLocaleString('en-IN');
        if (liveNetBalance) {
            liveNetBalance.textContent = '₹ ' + netBalance.toLocaleString('en-IN');
            liveNetBalance.style.color = netBalance >= 0 ? '#1b4332' : '#c9184a';
        }
    }

    if (incomeInput) {
        incomeInput.addEventListener('input', calculateBudgetLive);
        if (targetSavingsInput) targetSavingsInput.addEventListener('input', calculateBudgetLive);
        expenseFields.forEach(f => f.addEventListener('input', calculateBudgetLive));
    }
});
